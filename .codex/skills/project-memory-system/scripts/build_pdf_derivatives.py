#!/usr/bin/env python3
"""Build managed project PDFs from registered TeX sources."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import bootstrap_memory_system as memory_system


REPO_ROOT = memory_system.REPO_ROOT


def load_tex_rows() -> dict[str, dict[str, str]]:
    rows = memory_system.read_csv_rows(
        memory_system.registry_path("TEX_SOURCE_REGISTRY.csv")
    )
    return {row["path"]: row for row in rows}


def run_pdflatex(source_path: Path, output_path: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="aether-pdf-build-", delete=False) as temp_name:
        temp_dir = Path(temp_name)
        staged_source = temp_dir / source_path.name
        shutil.copy2(source_path, staged_source)
        shared_source = REPO_ROOT / "tex_shared"
        if shared_source.exists():
            shutil.copytree(shared_source, temp_dir / "tex_shared", dirs_exist_ok=True)
        command = [
            "pdflatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            staged_source.name,
        ]
        try:
            for _ in range(3):
                subprocess.run(command, cwd=temp_dir, check=True)
        except (OSError, subprocess.CalledProcessError) as exc:
            print(f"PDF build failed. Temporary build directory preserved: {temp_dir}", file=sys.stderr)
            raise SystemExit(1) from exc
        built_pdf = temp_dir / f"{source_path.stem}.pdf"
        if not built_pdf.exists():
            print(f"PDF build did not produce expected output: {built_pdf}", file=sys.stderr)
            print(f"Temporary build directory preserved: {temp_dir}", file=sys.stderr)
            raise SystemExit(1)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(built_pdf, output_path)
        shutil.rmtree(temp_dir)


def build_managed(targets: list[str]) -> int:
    tex_rows = load_tex_rows()
    selected = []
    if targets:
        for target in targets:
            path = Path(target)
            relative = path.as_posix() if not path.is_absolute() else memory_system.rel_path(path)
            row = tex_rows.get(relative)
            if not row:
                print(f"Refusing managed build for unregistered TeX: {target}", file=sys.stderr)
                return 1
            selected.append(row)
    else:
        selected = [row for row in tex_rows.values() if row.get("pdf_required") == "true"]

    rebuilt_pdf_paths = []
    for row in selected:
        source_path = REPO_ROOT / row["path"]
        output_path = REPO_ROOT / memory_system.pdf_path_for_tex_path(row["path"])
        print(f"Building {row['path']} -> {output_path.relative_to(REPO_ROOT).as_posix()}")
        run_pdflatex(source_path, output_path)
        rebuilt_pdf_paths.append(output_path.relative_to(REPO_ROOT).as_posix())

    report = memory_system.bootstrap(
        refresh_existing=False,
        rebuilt_pdf_paths=rebuilt_pdf_paths,
    )
    report.print()
    return 0 if report.ok else 1


def build_scratch(target: str) -> int:
    source_path = Path(target)
    if not source_path.is_absolute():
        source_path = (Path.cwd() / source_path).resolve()
    output_path = REPO_ROOT / ".local" / "pdf_scratch" / f"{source_path.stem}.pdf"
    print(f"Scratch build {source_path} -> {output_path}")
    run_pdflatex(source_path, output_path)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets", nargs="*", help="Registered TeX paths to build.")
    parser.add_argument(
        "--scratch",
        metavar="PATH",
        help="Build an unregistered TeX file under .local/ without registry updates.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.scratch:
        if args.targets:
            print("--scratch does not accept additional managed targets.", file=sys.stderr)
            return 1
        return build_scratch(args.scratch)
    return build_managed(args.targets)


if __name__ == "__main__":
    raise SystemExit(main())
