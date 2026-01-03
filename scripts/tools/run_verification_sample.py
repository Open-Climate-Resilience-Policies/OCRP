#!/usr/bin/env python3
"""
Run a sample verification pass over a limited number of claims to produce verification_results_sample.jsonl
"""
import json
from pathlib import Path
import runpy

ns = runpy.run_path('tools/verify_harness_template.py')
retrieve_evidence = ns.get('retrieve_evidence')
call_model_for_verification = ns.get('call_model_for_verification')

def main():
    claims_file = Path('tools/claims.jsonl')
    out_file = Path('tools/verification_results_sample.jsonl')
    max_items = 80
    with claims_file.open('r', encoding='utf-8') as fh, out_file.open('w', encoding='utf-8') as outfh:
        for i, line in enumerate(fh):
            if i >= max_items:
                break
            claim = json.loads(line)
            evidence = retrieve_evidence(claim['claim'])
            result = call_model_for_verification(claim['claim'], evidence)
            rec = {
                'id': claim['id'],
                'file': claim['file'],
                'claim': claim['claim'],
                'status': result.get('status'),
                'confidence': result.get('confidence'),
                'evidence_url': result.get('evidence_url'),
                'evidence_snippet': result.get('evidence_snippet'),
                'suggestion': result.get('suggestion')
            }
            outfh.write(json.dumps(rec, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    main()
