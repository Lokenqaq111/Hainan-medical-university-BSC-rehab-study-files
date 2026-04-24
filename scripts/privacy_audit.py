#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
import logging
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]

FILENAME_PATTERNS = [
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    re.compile(r"1[3-9]\d{9}"),
    re.compile(r"\b\d{9,12}\b"),
    re.compile(r"Tom Wu|Candy|Eason|武宇翔|WYX|XHQ|WZY", re.IGNORECASE),
]

TEXT_PATTERNS = FILENAME_PATTERNS

TEXT_SUFFIXES = {".md", ".txt", ".rtf"}
DOCX_SUFFIXES = {".docx"}
PDF_SUFFIXES = {".pdf"}
SKIP_DIRS = {".git", "__pycache__"}


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def match_patterns(value: str, patterns: list[re.Pattern[str]]) -> list[str]:
    hits = []
    for pattern in patterns:
        found = pattern.findall(value)
        if not found:
            continue
        if isinstance(found[0], tuple):
            hits.extend("".join(item) for item in found)
        else:
            hits.extend(found)
    return sorted(set(hits))


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def read_docx_metadata(path: Path) -> dict[str, str]:
    metadata: dict[str, str] = {}
    try:
        with ZipFile(path) as zf:
            if "docProps/core.xml" not in zf.namelist():
                return metadata
            root = ET.fromstring(zf.read("docProps/core.xml"))
            for element in root:
                key = element.tag.split("}")[-1]
                value = (element.text or "").strip()
                if value:
                    metadata[key] = value
    except Exception as exc:
        metadata["error"] = str(exc)
    return metadata


def read_docx_text(path: Path, limit: int = 4000) -> str:
    chunks: list[str] = []
    try:
        with ZipFile(path) as zf:
            if "word/document.xml" not in zf.namelist():
                return ""
            root = ET.fromstring(zf.read("word/document.xml"))
            for element in root.iter():
                if element.tag.endswith("}t") and element.text:
                    chunks.append(element.text)
                if len(" ".join(chunks)) >= limit:
                    break
    except Exception:
        return ""
    return " ".join(chunks)[:limit]


def read_pdf_metadata(path: Path) -> dict[str, str]:
    try:
        reader = PdfReader(str(path))
        raw = reader.metadata or {}
        return {str(k): str(v) for k, v in raw.items() if v}
    except Exception as exc:
        return {"error": str(exc)}


def read_pdf_text(path: Path, limit: int = 4000) -> str:
    try:
        reader = PdfReader(str(path))
        chunks: list[str] = []
        for page in reader.pages[:2]:
            text = page.extract_text() or ""
            if text:
                chunks.append(text)
            if len("\n".join(chunks)) >= limit:
                break
        return "\n".join(chunks)[:limit]
    except Exception:
        return ""


def audit(root: Path) -> int:
    findings = 0

    print(f"Scanning: {root}")

    for path in iter_files(root):
        rel = path.relative_to(root)
        name_hits = match_patterns(str(rel), FILENAME_PATTERNS)
        if name_hits:
            findings += 1
            print(f"[filename] {rel}")
            print(f"  hits: {', '.join(name_hits)}")

        suffix = path.suffix.lower()
        if suffix in TEXT_SUFFIXES:
            text_hits = match_patterns(read_text_file(path)[:5000], TEXT_PATTERNS)
            if text_hits:
                findings += 1
                print(f"[text] {rel}")
                print(f"  hits: {', '.join(text_hits)}")

        if suffix in DOCX_SUFFIXES:
            metadata = read_docx_metadata(path)
            meta_blob = " | ".join(f"{k}={v}" for k, v in metadata.items())
            meta_hits = match_patterns(meta_blob, TEXT_PATTERNS)
            if meta_hits:
                findings += 1
                print(f"[docx-meta] {rel}")
                print(f"  hits: {', '.join(meta_hits)}")

            text_hits = match_patterns(read_docx_text(path), TEXT_PATTERNS)
            if text_hits:
                findings += 1
                print(f"[docx-text] {rel}")
                print(f"  hits: {', '.join(text_hits)}")

        if suffix in PDF_SUFFIXES:
            metadata = read_pdf_metadata(path)
            meta_blob = " | ".join(f"{k}={v}" for k, v in metadata.items())
            meta_hits = match_patterns(meta_blob, TEXT_PATTERNS)
            if meta_hits:
                findings += 1
                print(f"[pdf-meta] {rel}")
                print(f"  hits: {', '.join(meta_hits)}")

            text_hits = match_patterns(read_pdf_text(path), TEXT_PATTERNS)
            if text_hits:
                findings += 1
                print(f"[pdf-text] {rel}")
                print(f"  hits: {', '.join(text_hits)}")

    if findings == 0:
        print("No obvious privacy markers found.")
    else:
        print(f"Total findings: {findings}")

    return findings


if __name__ == "__main__":
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    raise SystemExit(1 if audit(target) else 0)
