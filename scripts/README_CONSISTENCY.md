# Consistency Guardian CLI

Local command-line tool implementing **Agent D: The Consistency Guardian** from [AGENTS.md](../AGENTS.md).

## Setup

```bash
# Create virtual environment (first time only)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```bash
# Review a single policy
python scripts/consistency_guardian.py _policies/solar-parking.md

# Review all policies
python scripts/consistency_guardian.py --all

# Review only changed files (git)
python scripts/consistency_guardian.py --changed

# Save report to file
python scripts/consistency_guardian.py --all --output report.md
```

## LLM-Enhanced Analysis

For deeper adversarial stress testing, enable local LLM support:

### Using Ollama

```bash
# Install Ollama: https://ollama.ai
ollama pull llama3

# Run guardian with LLM analysis
python scripts/consistency_guardian.py --all --llm ollama --model llama3
```

You can also configure via environment variables. Copy `example.env` to `.env` and set:

```
LLM_PROVIDER=ollama            # or lm-studio, llama-cpp
LLM_MODEL=llama3               # model name (ollama or lm-studio)
OLLAMA_BASE_URL=http://localhost:11434
LMSTUDIO_BASE_URL=http://localhost:1234
LLAMACPP_BASE_URL=http://localhost:8080
CG_FAIL_ON_CRITICAL=true       # set to false to avoid exit 1 on criticals
CG_TIMEOUT_SECONDS=30
```

Then run without flags:

```bash
source venv/bin/activate
export $(grep -v '^#' .env | xargs)   # load .env into environment
python scripts/consistency_guardian.py --all
```

### Using LM Studio or llama.cpp

```bash
# LM Studio (default port 1234)
python scripts/consistency_guardian.py --all --llm lm-studio

# llama.cpp server (default port 8080)
python scripts/consistency_guardian.py --all --llm llama-cpp
```

## What It Checks

1. **Frontmatter Consistency** - Required fields, valid slugs, keyword quality
2. **Content Structure** - Specific mandates vs vague language, realistic metrics
3. **Overlap & Redundancy** - Keyword/title collisions with existing policies
4. **Citation Integrity** - URL accessibility, source freshness, primary vs secondary
5. **Geographic Compatibility** - US-defaultism, seasonal terms, unit consistency
6. **Readability** - Sentence length, acronym definitions, heading hierarchy
7. **Adversarial Stress Test** - Loopholes, enforcement gaps, corruption risks (enhanced with LLM)

## Output Format

```markdown
## Policy Review: solar-parking.md

### ✅ PASSED
- All required frontmatter fields present
- All official_sources URLs accessible

### ⚠️ WARNINGS
- Keyword overlap with "balcony-solar-shade.md" (3 shared: solar, renewable, energy)
- Average sentence length 28.3 words (consider simplifying for readability)

### 🚫 CRITICAL ISSUES
- Vague enforcement language detected: encourage, should consider → use 'shall', 'must', 'required'
- Missing enforcement mechanism (no penalty for non-compliance)

### RECOMMENDATIONS
- Review 'balcony-solar-shade' for potential merge or scope differentiation
- Add Section 6: Enforcement & Penalties
```

## Integration with Workflow

### Pre-commit Check

```bash
# Check only modified policies before committing
python scripts/consistency_guardian.py --changed
```

### Monthly Audit

```bash
# Full library audit with LLM analysis
python scripts/consistency_guardian.py --all --llm ollama --output reports/audit-$(date +%Y-%m).md
```

### GitHub Actions (future)

See [AGENTS.md Section 11](../AGENTS.md#11-planned-github-actions-not-yet-enforced) for planned CI automation.

## Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

Edit `LLM_PROVIDERS` in `consistency_guardian.py` to add custom LLM endpoints:

```python
LLM_PROVIDERS = {
    'ollama': 'http://localhost:11434/api/generate',
    'custom': 'http://your-llm-server:port/api',
}
```

## Privacy & Local-First

- All checks run locally
- No data sent to external services
- LLM analysis uses local models only (Ollama, LM Studio, llama.cpp)
- Citation URL checks use HEAD requests (minimal bandwidth)

## Exit Codes

- `0` - All checks passed
- `1` - Critical issues detected (blocks CI when enabled)
