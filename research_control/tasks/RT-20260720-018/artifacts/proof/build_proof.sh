#!/bin/sh
set -eu

if [ "$#" -ne 2 ]; then
  echo "usage: build_proof.sh /absolute/path/to/lean /absolute/path/to/output-dir" >&2
  exit 64
fi

LEAN_BIN=$1
OUTPUT_DIR=$2
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SOURCE_PATH="$SCRIPT_DIR/SelectorKernel.lean"

mkdir -p "$OUTPUT_DIR"
"$LEAN_BIN" --version > "$OUTPUT_DIR/lean-version.txt"
"$LEAN_BIN" --deps "$SOURCE_PATH" > "$OUTPUT_DIR/lean-dependencies.txt"
"$LEAN_BIN" -o "$OUTPUT_DIR/SelectorKernel.olean" "$SOURCE_PATH" > "$OUTPUT_DIR/lean-build.log" 2>&1
shasum -a 256 "$SOURCE_PATH" > "$OUTPUT_DIR/source.sha256"
shasum -a 256 "$OUTPUT_DIR/SelectorKernel.olean" > "$OUTPUT_DIR/proof-object.sha256"
