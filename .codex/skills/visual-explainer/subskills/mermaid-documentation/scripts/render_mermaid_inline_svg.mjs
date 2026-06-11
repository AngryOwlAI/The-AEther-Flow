#!/usr/bin/env node
import { chromium } from "playwright";
import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(SCRIPT_DIR, "../../../../../..");
const MERMAID_VERSION = "11.15.0";
const RENDERER_VERSION = "mermaid-inline-svg-renderer@0.1.0";
const RENDERER_STAMP = `mermaid@${MERMAID_VERSION};${RENDERER_VERSION}`;
const MERMAID_BUNDLE = path.join(SCRIPT_DIR, "node_modules", "mermaid", "dist", "mermaid.min.js");

const DEFAULT_MERMAID_CONFIG = {
  startOnLoad: false,
  theme: "base",
  securityLevel: "strict",
  htmlLabels: false,
  flowchart: {
    htmlLabels: false
  },
  themeVariables: {
    fontFamily: "IBM Plex Sans, Avenir Next, Segoe UI, sans-serif",
    primaryColor: "#dfe8f2",
    primaryBorderColor: "#1e3a5f",
    primaryTextColor: "#1a211d",
    secondaryColor: "#dfeee6",
    secondaryBorderColor: "#2f6f54",
    secondaryTextColor: "#1a211d",
    tertiaryColor: "#f1e0bd",
    tertiaryBorderColor: "#b47718",
    tertiaryTextColor: "#1a211d",
    lineColor: "#68716b"
  }
};

function usage() {
  return [
    "Usage:",
    "  node render_mermaid_inline_svg.mjs html/example.html",
    "  node render_mermaid_inline_svg.mjs --all",
    "  node render_mermaid_inline_svg.mjs --all --check"
  ].join("\n");
}

function parseArgs(argv) {
  const args = {
    all: false,
    check: false,
    files: []
  };
  for (const arg of argv) {
    if (arg === "--all") {
      args.all = true;
    } else if (arg === "--check") {
      args.check = true;
    } else if (arg === "--help" || arg === "-h") {
      console.log(usage());
      process.exit(0);
    } else if (arg.startsWith("--")) {
      throw new Error(`Unknown option: ${arg}`);
    } else {
      args.files.push(arg);
    }
  }
  if (!args.all && args.files.length === 0) {
    throw new Error(`${usage()}\n\nAt least one file path or --all is required.`);
  }
  return args;
}

function relativePath(target) {
  return path.relative(REPO_ROOT, target).split(path.sep).join("/");
}

function resolveRepoPath(input) {
  return path.resolve(REPO_ROOT, input);
}

function parseCsvLine(line) {
  const cells = [];
  let value = "";
  let quoted = false;
  for (let index = 0; index < line.length; index += 1) {
    const char = line[index];
    if (char === '"') {
      if (quoted && line[index + 1] === '"') {
        value += '"';
        index += 1;
      } else {
        quoted = !quoted;
      }
    } else if (char === "," && !quoted) {
      cells.push(value);
      value = "";
    } else {
      value += char;
    }
  }
  cells.push(value);
  return cells;
}

async function readCsv(relative) {
  const text = await fs.readFile(resolveRepoPath(relative), "utf8");
  const lines = text.split(/\r?\n/).filter((line) => line.trim());
  const headers = parseCsvLine(lines.shift() ?? "");
  return lines.map((line) => {
    const cells = parseCsvLine(line);
    return Object.fromEntries(headers.map((header, index) => [header, cells[index] ?? ""]));
  });
}

async function discoverRegisteredHtml() {
  const htmlRows = await readCsv("registries/HTML_EXPLAINER_REGISTRY.csv");
  const markdownRows = await readCsv("registries/MARKDOWN_SOURCE_REGISTRY.csv");
  const markdownById = new Map(markdownRows.map((row) => [row.object_id, row]));
  const paths = [];
  for (const row of htmlRows) {
    const htmlPath = resolveRepoPath(row.path);
    let htmlText = "";
    try {
      htmlText = await fs.readFile(htmlPath, "utf8");
    } catch {
      continue;
    }
    const sourceRow = markdownById.get(row.source_basis);
    let sourceText = "";
    if (sourceRow?.path) {
      try {
        sourceText = await fs.readFile(resolveRepoPath(sourceRow.path), "utf8");
      } catch {
        sourceText = "";
      }
    }
    if (htmlText.includes("diagram-source") || sourceText.includes("mermaid_diagrams:")) {
      paths.push(row.path);
    }
  }
  return paths;
}

function commonIndent(lines) {
  let min = Infinity;
  for (const line of lines) {
    if (!line.trim()) continue;
    const match = line.match(/^[ \t]*/);
    min = Math.min(min, match ? match[0].length : 0);
  }
  return Number.isFinite(min) ? min : 0;
}

function normalizeMermaidSource(source) {
  const lines = source.replace(/\r\n?/g, "\n").split("\n");
  const indent = commonIndent(lines);
  const dedented = lines.map((line) => line.slice(Math.min(indent, line.length)));
  while (dedented.length && !dedented[0].trim()) dedented.shift();
  while (dedented.length && !dedented[dedented.length - 1].trim()) dedented.pop();
  return dedented.map((line) => line.replace(/[ \t]+$/g, "")).join("\n");
}

function sourceHash(source) {
  return crypto.createHash("sha256").update(normalizeMermaidSource(source), "utf8").digest("hex");
}

function firstSemanticLine(source) {
  for (const line of normalizeMermaidSource(source).split("\n")) {
    const trimmed = line.trim();
    if (trimmed && !trimmed.startsWith("%%")) return trimmed;
  }
  return "";
}

function attrValue(attrs, name) {
  const re = new RegExp(`${name}\\s*=\\s*(?:"([^"]*)"|'([^']*)')`, "i");
  const match = attrs.match(re);
  return match ? match[1] ?? match[2] ?? "" : "";
}

function classHas(attrs, className) {
  return attrValue(attrs, "class").split(/\s+/).includes(className);
}

function htmlUnescape(value) {
  return value
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
}

function htmlEscapeAttr(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function setAttr(attrs, name, value) {
  const escaped = htmlEscapeAttr(value);
  const re = new RegExp(`\\s${name}\\s*=\\s*(?:"[^"]*"|'[^']*')`, "i");
  if (re.test(attrs)) {
    return attrs.replace(re, ` ${name}="${escaped}"`);
  }
  return `${attrs} ${name}="${escaped}"`;
}

function extractDiagramSources(htmlText, filePath) {
  const sources = new Map();
  const scriptRe = /<script\b(?<attrs>[^>]*)>(?<body>[\s\S]*?)<\/script>/gi;
  for (const match of htmlText.matchAll(scriptRe)) {
    const attrs = match.groups.attrs;
    if (!classHas(attrs, "diagram-source")) continue;
    const diagramId = attrValue(attrs, "data-mermaid-diagram-id").trim();
    if (!diagramId) {
      throw new Error(`${filePath}: diagram-source missing data-mermaid-diagram-id`);
    }
    if (sources.has(diagramId)) {
      throw new Error(`${filePath}: duplicate diagram-source for ${diagramId}`);
    }
    const source = htmlUnescape(match.groups.body);
    if (!normalizeMermaidSource(source)) {
      throw new Error(`${filePath}: Mermaid source is empty for ${diagramId}`);
    }
    sources.set(diagramId, source);
  }
  return sources;
}

function extractShells(htmlText, filePath) {
  const shells = new Map();
  const sectionRe = /<section\b(?<attrs>[^>]*)>[\s\S]*?<\/section>/gi;
  for (const match of htmlText.matchAll(sectionRe)) {
    const attrs = match.groups.attrs;
    if (!classHas(attrs, "diagram-shell")) continue;
    const diagramId = attrValue(attrs, "data-mermaid-diagram-id").trim();
    if (!diagramId) continue;
    if (shells.has(diagramId)) {
      throw new Error(`${filePath}: duplicate diagram-shell for ${diagramId}`);
    }
    shells.set(diagramId, {
      start: match.index,
      end: match.index + match[0].length,
      text: match[0]
    });
  }
  return shells;
}

function replaceCanvas(shellText, filePath, diagramId, svg, hash) {
  const canvasRe =
    /<div\b(?<attrs>[^>]*class\s*=\s*(?:"[^"]*\bmermaid-canvas\b[^"]*"|'[^']*\bmermaid-canvas\b[^']*')[^>]*)>[\s\S]*?<\/div>/gi;
  const matches = [...shellText.matchAll(canvasRe)];
  if (matches.length !== 1) {
    throw new Error(`${filePath}: Mermaid ID ${diagramId} must have exactly one .mermaid-canvas`);
  }
  const match = matches[0];
  let nextAttrs = setAttr(match.groups.attrs, "data-renderer", RENDERER_STAMP);
  nextAttrs = setAttr(nextAttrs, "data-render-source-sha256", hash);
  const replacement = `<div${nextAttrs}>${svg}</div>`;
  return shellText.slice(0, match.index) + replacement + shellText.slice(match.index + match[0].length);
}

async function createRenderer() {
  let browser;
  try {
    browser = await chromium.launch({ headless: true });
  } catch (error) {
    throw new Error(
      [
        "Unable to launch Playwright-managed Chromium.",
        `Short error: ${String(error.message || error).split("\n")[0]}`,
        "Setup:",
        "  cd .codex/skills/visual-explainer/subskills/mermaid-documentation/scripts",
        "  npm ci",
        "  npx playwright install chromium"
      ].join("\n")
    );
  }
  const page = await browser.newPage();
  await page.setContent("<!doctype html><html><body><div id=\"mermaid-render-root\"></div></body></html>");
  await page.addScriptTag({ path: MERMAID_BUNDLE });
  await page.evaluate((config) => {
    window.mermaid.initialize(config);
  }, DEFAULT_MERMAID_CONFIG);
  return {
    async render(diagramId, source) {
      return page.evaluate(
        async ({ diagramId: pageDiagramId, source: pageSource }) => {
          const renderId = `mmd-${pageDiagramId}-root`;
          const rendered = await window.mermaid.render(renderId, pageSource);
          const parser = new DOMParser();
          const doc = parser.parseFromString(rendered.svg, "image/svg+xml");
          const parseError = doc.querySelector("parsererror");
          if (parseError) {
            throw new Error(parseError.textContent.trim().slice(0, 240));
          }

          const svg = doc.documentElement;
          const allowedElements = new Set([
            "svg",
            "g",
            "path",
            "rect",
            "polygon",
            "circle",
            "ellipse",
            "line",
            "polyline",
            "text",
            "tspan",
            "marker",
            "defs",
            "filter",
            "fedropshadow",
            "lineargradient",
            "stop",
            "style",
            "title",
            "desc"
          ]);
          const dangerousStyle = /@import|javascript:|url\(\s*(?:["']?https?:|["']?\/\/)/i;
          const localUrlRe = /^url\(\s*["']?#[^)'" ]+["']?\s*\)$/i;
          const localUrlFindRe = /url\(\s*["']?#([^)'" ]+)["']?\s*\)/g;
          const cssIdSelectorRe = /(^|[\s,{>+~}])#([A-Za-z_][A-Za-z0-9_.:-]*)(?=[\s.#:[,{>+~])/g;
          const idMap = new Map();
          const seenIds = new Set();
          const clean = (value) => value.replace(/[^a-zA-Z0-9_-]+/g, "-").replace(/^-+|-+$/g, "");
          const allNodes = Array.from(doc.querySelectorAll("*"));

          const walker = doc.createTreeWalker(doc, NodeFilter.SHOW_COMMENT);
          const comments = [];
          while (walker.nextNode()) comments.push(walker.currentNode);
          for (const comment of comments) comment.remove();

          for (const element of allNodes) {
            const tag = element.tagName.toLowerCase();
            if (tag === "foreignobject") {
              throw new Error("foreignObject is not allowed in governed inline SVG");
            }
            if (!allowedElements.has(tag)) {
              throw new Error(`SVG element <${tag}> is not allowed`);
            }
            if (element.id) {
              if (seenIds.has(element.id)) throw new Error(`duplicate SVG id before rewrite: ${element.id}`);
              seenIds.add(element.id);
              idMap.set(element.id, `mmd-${pageDiagramId}-${clean(element.id) || "id"}`);
            }
          }

          for (const element of allNodes) {
            const id = element.getAttribute("id");
            if (id && idMap.has(id)) {
              element.setAttribute("id", idMap.get(id));
            }
          }

          const rewriteIdRefs = (value, attrName = "") => {
            let next = value;
            next = next.replace(localUrlFindRe, (full, id) => {
              if (!idMap.has(id)) throw new Error(`unmapped local SVG url reference: ${id}`);
              return full.replace(`#${id}`, `#${idMap.get(id)}`);
            });
            if ((attrName === "href" || attrName === "xlink:href") && next.startsWith("#")) {
              const id = next.slice(1);
              if (!idMap.has(id)) throw new Error(`unmapped local SVG href reference: ${id}`);
              next = `#${idMap.get(id)}`;
            }
            if ((attrName === "aria-labelledby" || attrName === "aria-describedby") && next.trim()) {
              next = next
                .split(/\s+/)
                .map((id) => {
                  if (!idMap.has(id)) throw new Error(`unmapped ARIA SVG reference: ${id}`);
                  return idMap.get(id);
                })
                .join(" ");
            }
            return next;
          };
          const rewriteCssIdSelectors = (value) =>
            value.replace(cssIdSelectorRe, (full, prefix, id) => {
              if (!idMap.has(id)) throw new Error(`unmapped CSS SVG id selector: ${id}`);
              return `${prefix}#${idMap.get(id)}`;
            });

          for (const element of allNodes) {
            for (const attr of Array.from(element.attributes)) {
              const name = attr.name.toLowerCase();
              const value = attr.value;
              if (name.startsWith("on")) {
                element.removeAttribute(attr.name);
                continue;
              }
              if (name.startsWith("xmlns")) continue;
              if (/javascript:/i.test(value)) throw new Error(`unsafe javascript URL in ${attr.name}`);
              if ((name === "href" || name === "xlink:href") && value && !value.startsWith("#")) {
                throw new Error(`external href is not allowed in ${attr.name}`);
              }
              if (/url\(/i.test(value) && !localUrlRe.test(value) && !localUrlFindRe.test(value)) {
                throw new Error(`nonlocal URL reference is not allowed in ${attr.name}`);
              }
              if (/https?:\/\//i.test(value) && !name.startsWith("xmlns")) {
                throw new Error(`remote URL is not allowed in ${attr.name}`);
              }
              if (name === "style" && dangerousStyle.test(value)) {
                throw new Error(`unsafe style URL in ${attr.name}`);
              }
              element.setAttribute(attr.name, rewriteIdRefs(value, name));
            }
            if (element.tagName.toLowerCase() === "style") {
              const text = element.textContent || "";
              if (dangerousStyle.test(text) || /font-face|https?:\/\//i.test(text)) {
                throw new Error("unsafe CSS in SVG style block");
              }
              element.textContent = rewriteCssIdSelectors(rewriteIdRefs(text));
            }
          }

          const finalIds = new Set();
          for (const element of allNodes) {
            if (!element.id) continue;
            if (finalIds.has(element.id)) throw new Error(`duplicate SVG id after rewrite: ${element.id}`);
            finalIds.add(element.id);
          }

          svg.setAttribute("data-mermaid-rendered", "true");
          svg.setAttribute("data-mermaid-diagram-id", pageDiagramId);
          if (!svg.getAttribute("viewBox") && !svg.getAttribute("width")) {
            throw new Error("sanitized SVG has no viewBox or width");
          }
          const serialized = new XMLSerializer().serializeToString(svg);
          if (!serialized.includes("<svg") || serialized.length < 100) {
            throw new Error("sanitized SVG is empty or invalid");
          }
          return serialized;
        },
        { diagramId, source: normalizeMermaidSource(source) }
      );
    },
    async close() {
      await browser.close();
    }
  };
}

async function renderFile(renderer, relative, checkOnly) {
  const absolute = resolveRepoPath(relative);
  const original = await fs.readFile(absolute, "utf8");
  const sources = extractDiagramSources(original, relative);
  if (sources.size === 0) {
    return { relative, changed: false, diagrams: 0 };
  }
  const shells = extractShells(original, relative);
  let next = original;
  const replacements = [];

  for (const [diagramId, source] of sources) {
    const shell = shells.get(diagramId);
    if (!shell) {
      throw new Error(`${relative}: missing diagram-shell for ${diagramId}`);
    }
    try {
      const svg = await renderer.render(diagramId, source);
      const hash = sourceHash(source);
      const nextShell = replaceCanvas(shell.text, relative, diagramId, svg, hash);
      replacements.push({ start: shell.start, end: shell.end, text: nextShell });
    } catch (error) {
      throw new Error(
        [
          `${relative}: failed to render Mermaid ID ${diagramId}`,
          `First semantic line: ${firstSemanticLine(source)}`,
          `Short error: ${String(error.message || error).split("\n")[0]}`
        ].join("\n")
      );
    }
  }

  for (const replacement of replacements.sort((a, b) => b.start - a.start)) {
    next = next.slice(0, replacement.start) + replacement.text + next.slice(replacement.end);
  }

  const changed = next !== original;
  if (checkOnly && changed) {
    throw new Error(`${relative}: inline Mermaid SVG is stale; run render_mermaid_inline_svg.mjs ${relative}`);
  }
  if (!checkOnly && changed) {
    await fs.writeFile(absolute, next, "utf8");
  }
  return { relative, changed, diagrams: sources.size };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const files = args.all ? await discoverRegisteredHtml() : args.files.map((file) => relativePath(resolveRepoPath(file)));
  const uniqueFiles = [...new Set(files)].sort();
  const renderer = await createRenderer();
  try {
    const results = [];
    for (const file of uniqueFiles) {
      results.push(await renderFile(renderer, file, args.check));
    }
    for (const result of results) {
      if (result.diagrams === 0) continue;
      const verb = args.check ? "checked" : result.changed ? "rendered" : "unchanged";
      console.log(`${verb}: ${result.relative} (${result.diagrams} diagram${result.diagrams === 1 ? "" : "s"})`);
    }
  } finally {
    await renderer.close();
  }
}

main().catch((error) => {
  console.error(String(error.message || error));
  process.exit(1);
});
