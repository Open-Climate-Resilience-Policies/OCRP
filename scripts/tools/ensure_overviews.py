#!/usr/bin/env python3
import glob, os, shutil, re

POL_DIR = os.path.join(os.path.dirname(__file__), '..', '_policies')

def ensure_overview(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
    orig = s
    front = ''
    body = s
    if s.startswith('---'):
        parts = s.split('---', 2)
        if len(parts) >= 3:
            front = '---' + parts[1] + '---'
            body = parts[2]
    # normalize leading newlines
    body = body.lstrip('\n')

    # find existing Overview block
    overview_re = re.compile(r"^##\s+Overview\b", flags=re.MULTILINE)
    m = overview_re.search(body)
    if m:
        # extract overview block (from m.start to next '## ' or end)
        start = m.start()
        # find next heading
        next_h = re.search(r"\n##\s+", body[m.end():])
        if next_h:
            end = m.end() + next_h.start()
        else:
            end = len(body)
        overview_block = body[start:end].rstrip() + '\n\n'
        # remove the original overview block
        body = body[:start] + body[end:]
        body = body.lstrip('\n')
    else:
        # create overview from summary frontmatter if available
        summary = ''
        fm = front
        msum = re.search(r"summary:\s*\"(.*?)\"", fm, flags=re.S)
        if msum:
            summary = msum.group(1)
        else:
            # fallback: first paragraph of body
            paragraphs = [p.strip() for p in body.split('\n\n') if p.strip()]
            summary = paragraphs[0] if paragraphs else 'Policy overview not yet provided.'
        overview_block = '## Overview\n\n' + summary.strip() + '\n\n'

    # ensure no other Overview remains
    body = re.sub(r"\n##\s+Overview\b[\s\S]*?(?=\n##\s+|\Z)", "\n", body, flags=re.MULTILINE)
    # insert overview at top
    new_body = overview_block + body.lstrip('\n')

    new_content = front + '\n\n' + new_body
    if new_content != orig:
        bak = path + '.bak.overview'
        shutil.copy2(path, bak)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, bak
    return False, None

def main():
    files = sorted(glob.glob(os.path.join(POL_DIR, '*.md')))
    changed = []
    for f in files:
        ok, bak = ensure_overview(f)
        if ok:
            changed.append((f, bak))
    print(f'Processed {len(files)} files, modified {len(changed)} files')
    for f,b in changed:
        print(f'- Modified: {f} (backup: {b})')

if __name__ == '__main__':
    main()
