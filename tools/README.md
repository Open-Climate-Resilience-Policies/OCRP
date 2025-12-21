Claim extraction and verification tools

1) Extract claims from all policies

   python3 tools/extract_claims.py _policies/*.md > claims.jsonl

2) Implement retrieval and model calls in `tools/verify_harness_template.py`.
   - `retrieve_evidence(claim)` should return a list of {url, snippet} items.
   - `call_model_for_verification(claim, evidence)` should call your chosen LLM and return the verification structure.

3) Run verification (example)

   python3 tools/verify_harness_template.py claims.jsonl

Outputs: `verification_results.jsonl` with one JSON entry per claim.

Notes:
- Use temperature=0 for classification tasks, and an ensemble of models if possible.
- Keep an audit trail: store claims, evidence, model outputs, and final human decisions.
