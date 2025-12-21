"""
Verification harness template (skeleton) - fill with your model/retrieval details.

This script reads `claims.jsonl`, calls a retrieval function to fetch evidence (not implemented), then calls a model verification function (not implemented) with a standard prompt.

You should implement `retrieve_evidence(claim)` and `call_model_for_verification(claim, evidence)` using your chosen stack (OpenAI, Azure, local LLMs, etc.).

Output: `verification_results.jsonl` with entries: {id, file, claim, status, confidence, evidence_url, evidence_snippet, suggestion}

Run:
    python3 tools/verify_harness_template.py claims.jsonl

"""
import sys
import json
import os
import time
from pathlib import Path

try:
    import requests
except Exception:
    requests = None
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except Exception:
    BeautifulSoup = None
    BS4_AVAILABLE = False

try:
    import openai
except Exception:
    openai = None


PROMPT_TEMPLATE = '''
You are a careful verifier. Given the claim and the retrieved evidence documents (URL + excerpt), answer in JSON with keys: status (Supported|Contradicted|Unsubstantiated), confidence (0-100), evidence_url (or null), evidence_snippet (or null), suggestion (optional short edit).

Claim: {claim}

Evidence:
{evidence}

Return only JSON.
'''


def retrieve_evidence(claim):
    # Simple DuckDuckGo HTML search + scrape top result snippets
    # Returns list of {url, snippet}
    try:
        q = claim
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; OCRaP-bot/1.0)'}
        results = []
        seen = set()
        if requests:
            params = {'q': q}
            r = requests.post('https://html.duckduckgo.com/html/', data=params, headers=headers, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, 'lxml')
            anchors = soup.select('a.result__a')
            if not anchors:
                anchors = soup.select('a')
            hrefs = [a.get('href') for a in anchors if a.get('href')][:6]
        else:
            # fallback: simple HTML query via urllib
            import urllib.parse, urllib.request
            data = urllib.parse.urlencode({'q': q}).encode()
            req = urllib.request.Request('https://html.duckduckgo.com/html/', data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read()
            soup = BeautifulSoup(html, 'lxml')
            anchors = soup.select('a.result__a')
            if not anchors:
                anchors = soup.select('a')
            hrefs = [a.get('href') for a in anchors if a.get('href')][:6]

        for href in hrefs:
            if not href or href in seen:
                continue
            seen.add(href)
            snippet = ''
            try:
                # fetch page (requests preferred)
                if requests:
                    pr = requests.get(href, headers=headers, timeout=8)
                    pr.raise_for_status()
                    page_text = pr.text
                else:
                    import urllib.request
                    with urllib.request.urlopen(href, timeout=8) as pr:
                        page_bytes = pr.read()
                        try:
                            page_text = page_bytes.decode('utf-8')
                        except Exception:
                            page_text = str(page_bytes)

                # extract paragraphs
                if BS4_AVAILABLE and BeautifulSoup is not None:
                    psoup = BeautifulSoup(page_text, 'lxml')
                    paras = [p.get_text(' ', strip=True) for p in psoup.find_all('p')[:10]]
                else:
                    import re
                    paras = re.findall(r'<p[^>]*>(.*?)</p>', page_text, flags=re.S|re.I)
                    paras = [re.sub(r'<[^>]+>','',p).strip() for p in paras]
                text = ' '.join(paras[:10])

                # find snippet matching claim
                for word in claim.split()[:8]:
                    if len(word) < 4:
                        continue
                    idx = text.lower().find(word.lower())
                    if idx != -1:
                        start = max(0, idx-80)
                        snippet = text[start:start+300]
                        break
                if not snippet:
                    snippet = text[:300]
            except Exception:
                snippet = ''
            results.append({'url': href, 'snippet': snippet})
            time.sleep(0.2)
        return results
    except Exception:
        return []


def call_model_for_verification(claim, evidence):
    # If OpenAI client is configured, call it; otherwise use a simple heuristic
    api_key = os.getenv('OPENAI_API_KEY')
    if openai and api_key:
        try:
            openai.api_key = api_key
            ev_text = ''
            for i, e in enumerate(evidence):
                ev_text += f"[{i}] {e.get('url','')}\n{e.get('snippet','')}\n\n"
            prompt = PROMPT_TEMPLATE.format(claim=claim, evidence=ev_text)
            resp = openai.ChatCompletion.create(
                model=os.getenv('OPENAI_MODEL','gpt-4o-mini'),
                messages=[{'role':'user','content':prompt}],
                temperature=0,
                max_tokens=512
            )
            text = resp['choices'][0]['message']['content'].strip()
            # Expecting JSON from model; try parse
            try:
                parsed = json.loads(text)
                return parsed
            except Exception:
                return {'status':'Unsubstantiated','confidence':0,'evidence_url':None,'evidence_snippet':None,'suggestion':'Model returned non-JSON.'}
        except Exception:
            pass

    # Heuristic fallback: check overlapping words between claim and snippets
    import re
    claim_words = set(re.findall(r"\w{4,}", claim.lower()))
    best = None
    best_score = 0
    best_url = None
    for e in evidence:
        snippet = (e.get('snippet') or '').lower()
        words = set(re.findall(r"\w{4,}", snippet))
        if not words:
            continue
        score = len(claim_words & words)
        if score > best_score:
            best_score = score
            best = snippet
            best_url = e.get('url')
    if best_score >= 3:
        confidence = min(95, 20 + best_score*10)
        return {'status':'Supported','confidence':confidence,'evidence_url':best_url,'evidence_snippet':best,'suggestion':None}
    elif best_score > 0:
        confidence = min(60, 10 + best_score*10)
        return {'status':'Unsubstantiated','confidence':confidence,'evidence_url':best_url,'evidence_snippet':best,'suggestion':'Weak match; add citation or clarify claim.'}
    else:
        return {'status':'Unsubstantiated','confidence':5,'evidence_url':None,'evidence_snippet':None,'suggestion':'No retrieval matches; run deeper search.'}


def main(argv):
    if len(argv) < 2:
        print('Usage: verify_harness_template.py claims.jsonl')
        return
    claims_file = Path(argv[1])
    out = Path('verification_results.jsonl')
    with claims_file.open('r', encoding='utf-8') as fh, out.open('w', encoding='utf-8') as outfh:
        for line in fh:
            claim = json.loads(line)
            evidence = retrieve_evidence(claim['claim'])
            result = call_model_for_verification(claim['claim'], evidence)
            rec = {
                'id': claim['id'],
                'file': claim['file'],
                'claim': claim['claim'],
                'status': result['status'],
                'confidence': result['confidence'],
                'evidence_url': result.get('evidence_url'),
                'evidence_snippet': result.get('evidence_snippet'),
                'suggestion': result.get('suggestion')
            }
            outfh.write(json.dumps(rec, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main(sys.argv)
