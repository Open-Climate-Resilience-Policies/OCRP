#!/usr/bin/env python3
"""
Simple claim extraction tool for OCRaP policies.
Output: JSONL with one claim per line: {id, file, paragraph_index, claim, context}

Heuristics:
 - Remove YAML frontmatter
 - Split into paragraphs (blank-line separated)
 - Within each paragraph, split into sentences using a simple regex
 - Keep sentences longer than 40 characters and not list items or headings

Usage:
    python3 tools/extract_claims.py _policies/*.md > claims.jsonl

"""
import sys
import io
import os
import re
import json
from pathlib import Path

SENTENCE_RE = re.compile(r"(?<=[\.\?\!])\s+(?=[A-Z0-9\(\"'])")


def strip_frontmatter(text: str) -> str:
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            return parts[2].lstrip('\n')
        return ''
    return text


def split_paragraphs(text: str):
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return paras


def split_sentences(paragraph: str):
    # fallback: split on sentence boundary regex
    parts = SENTENCE_RE.split(paragraph.strip())
    parts = [p.strip() for p in parts if p.strip()]
    return parts


def is_candidate_sentence(s: str) -> bool:
    if len(s) < 40:
        return False
    if s.startswith('#'):
        return False
    if s.startswith('-') or s.startswith('*') or s.startswith('>'):
        return False
    # skip lines that look like list entries (start with number.
    if re.match(r"^\d+\.", s):
        return False
    # skip code fences
    if s.startswith('```') or s.endswith('```'):
        return False
    return True


def extract_from_file(path: Path, start_id=0):
    text = path.read_text(encoding='utf-8')
    body = strip_frontmatter(text)
    paras = split_paragraphs(body)
    claims = []
    cid = start_id
    for pi, para in enumerate(paras):
        # ignore short paras or paras that are just headers
        if len(para) < 60:
            continue
        sentences = split_sentences(para)
        for s in sentences:
            if is_candidate_sentence(s):
                try:
                    rel = str(path.relative_to(Path.cwd()))
                except Exception:
                    rel = str(path)
                claim = {
                    'id': cid,
                    'file': rel,
                    'paragraph_index': pi,
                    'claim': s,
                    'context': para
                }
                claims.append(claim)
                cid += 1
    return claims


def main(argv):
    if len(argv) < 2:
        print('Usage: extract_claims.py <policy-files...>', file=sys.stderr)
        sys.exit(2)
    files = argv[1:]
    all_claims = []
    cid = 0
    for fp in files:
        p = Path(fp)
        if not p.exists():
            print(f'Warning: {fp} not found', file=sys.stderr)
            continue
        claims = extract_from_file(p, start_id=cid)
        all_claims.extend(claims)
        cid += len(claims)
    out = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    for c in all_claims:
        out.write(json.dumps(c, ensure_ascii=False) + "\n")


if __name__ == '__main__':
    main(sys.argv)
