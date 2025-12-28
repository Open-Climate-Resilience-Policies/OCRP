#!/usr/bin/env python3
"""
Agent D: The Consistency Guardian
Run adversarial quality checks on policy files to ensure consistency and best practices.

Usage:
    python scripts/consistency_guardian.py _policies/solar-parking.md
    python scripts/consistency_guardian.py --all
    python scripts/consistency_guardian.py --changed
    python scripts/consistency_guardian.py --llm ollama --model llama3
"""

import os
import sys
import argparse
import yaml
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from urllib.parse import urlparse
import requests
from difflib import SequenceMatcher

# Configure for local LLM support
LLM_PROVIDERS = {
    'ollama': 'http://localhost:11434',
    'llama-cpp': 'http://localhost:8080',
    'lm-studio': 'http://localhost:1234',
}


class PolicyReview:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.passed = []
        self.warnings = []
        self.critical = []
        self.recommendations = []
        self.frontmatter = {}
        self.content = ""
        
    def add_pass(self, check: str):
        self.passed.append(check)
    
    def add_warning(self, issue: str):
        self.warnings.append(issue)
    
    def add_critical(self, issue: str):
        self.critical.append(issue)
    
    def add_recommendation(self, rec: str):
        self.recommendations.append(rec)
    
    def should_escalate(self) -> bool:
        return len(self.critical) > 2
    
    def format_report(self) -> str:
        filename = Path(self.filepath).name
        report = [f"\n## Policy Review: {filename}\n"]
        
        if self.passed:
            report.append("### ✅ PASSED")
            for item in self.passed:
                report.append(f"- {item}")
            report.append("")
        
        if self.warnings:
            report.append("### ⚠️ WARNINGS")
            for item in self.warnings:
                report.append(f"- {item}")
            report.append("")
        
        if self.critical:
            report.append("### 🚫 CRITICAL ISSUES")
            for item in self.critical:
                report.append(f"- {item}")
            report.append("")
        
        if self.recommendations:
            report.append("### RECOMMENDATIONS")
            for item in self.recommendations:
                report.append(f"- {item}")
            report.append("")
        
        if self.should_escalate():
            report.append("⚠️ **ESCALATION REQUIRED**: >2 critical issues detected\n")
        
        return "\n".join(report)


class ConsistencyGuardian:
    def __init__(self, policies_dir: str = "_policies", llm_provider: Optional[str] = None, llm_model: Optional[str] = None):
        self.policies_dir = Path(policies_dir)
        # Allow environment-based defaults
        self.llm_provider = llm_provider or os.getenv('LLM_PROVIDER')
        self.llm_model = llm_model or os.getenv('LLM_MODEL') or "llama3"
        # Base URLs can be overridden via environment
        self.ollama_base = os.getenv('OLLAMA_BASE_URL', LLM_PROVIDERS['ollama'])
        self.llamacpp_base = os.getenv('LLAMACPP_BASE_URL', LLM_PROVIDERS['llama-cpp'])
        self.lmstudio_base = os.getenv('LMSTUDIO_BASE_URL', LLM_PROVIDERS['lm-studio'])
        # Request timeout (seconds)
        self.timeout = int(os.getenv('CG_TIMEOUT_SECONDS', '30'))
        self.min_policy_lines = int(os.getenv('CG_MIN_POLICY_LINES', '120'))
        self.section_keywords = {
            'problem statement': ['problem', 'context', 'overview', 'background'],
            'mandate/requirements': ['mandate', 'policy', 'requirements', 'obligation'],
            'implementation guidance': ['implementation', 'roadmap', 'program', 'steps'],
            'metrics/verification': ['metrics', 'verification', 'monitoring', 'success', 'compliance']
        }
        self.unit_tokens = [
            '°C', '°F', 'celsius', 'fahrenheit', 'kelvin',
            'm³', 'm3', 'liters', 'liter', 'litres', 'litre', 'l',
            'mw', 'mwh', 'kw', 'kwh', 'gw', 'gwh',
            'dba', 'dbc', 'μg/m³', 'ug/m3', 'mg/nm³', '%', 'percent',
            'km', 'm', 'minutes', 'minute', 'hours', 'hour', 'days', 'day', 'months', 'month', 'years', 'year'
        ]
        self.unit_regex = re.compile(r'^\s*(?:' + '|'.join(re.escape(u) for u in self.unit_tokens) + r')', re.IGNORECASE)
        self.acronym_allowlist = {
            'PUE', 'WUE', 'CUE', 'MW', 'MWH', 'KW', 'KWH', 'GW', 'GWH',
            'NOX', 'PM', 'PM25', 'PM2', 'EPA', 'ISO', 'IEC', 'EU', 'KPIS', 'KPI', 'CBA', 'PPA', 'REC', 'IT',
            'LLM', 'KP', 'DBA', 'DBC', 'KWH', 'MWD'
        }
        self.prefix_skip_words = {
            'policy', 'policies', 'phase', 'phases', 'principle', 'principles', 'months', 'month',
            'years', 'year', 'minutes', 'minute', 'days', 'day', 'step', 'stage', 'chapter',
            'appendix', 'section', 'option', 'table', 'row', 'column', 'agent'
        }
        self.range_unit_tokens = {token.lower().strip('%') for token in self.unit_tokens if token}
        self.all_policies = list(self.policies_dir.glob("*.md"))
        
    def parse_policy(self, filepath: Path) -> tuple[dict, str, bool]:
        """Extract frontmatter and content from policy file. Returns (frontmatter, content, is_properly_closed)."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split frontmatter and content
        parts = re.split(r'^---\s*$', content, flags=re.MULTILINE, maxsplit=2)
        if len(parts) < 3:
            return {}, content, False
        
        frontmatter = yaml.safe_load(parts[1]) or {}
        markdown_content = parts[2].strip()
        
        # Check if frontmatter is properly closed (should have exactly 3 parts: opening, content, body)
        is_properly_closed = len(parts) == 3
        
        return frontmatter, markdown_content, is_properly_closed
    
    def check_frontmatter_consistency(self, review: PolicyReview, frontmatter: dict, filepath: Path, is_properly_closed: bool):
        """Check 1: Frontmatter Consistency"""
        required_fields = ['date', 'slug', 'keywords', 'official_sources']
        missing = [f for f in required_fields if f not in frontmatter]
        
        # Check frontmatter delimiters first
        if not is_properly_closed:
            review.add_critical("Frontmatter not properly closed: missing closing '---' delimiter after frontmatter")
            return  # Skip other checks if frontmatter is malformed
        
        if missing:
            review.add_critical(f"Missing required frontmatter fields: {', '.join(missing)}")
        else:
            review.add_pass("All required frontmatter fields present")
        
        # Check keywords
        if 'keywords' in frontmatter:
            keywords = frontmatter['keywords']
            if not isinstance(keywords, list):
                review.add_critical("keywords must be an array")
            elif len(keywords) < 2 or len(keywords) > 5:
                review.add_warning(f"keywords should have 2-5 items (found {len(keywords)})")
            elif any(k in ['climate', 'policy', 'resilience'] for k in keywords):
                review.add_warning("Avoid generic keywords like 'climate', 'policy', 'resilience'")
        
        # Check slug matches filename
        if 'slug' in frontmatter:
            expected_slug = filepath.stem
            if frontmatter['slug'] != expected_slug:
                review.add_critical(f"slug '{frontmatter['slug']}' does not match filename '{expected_slug}'")
            if re.search(r'[A-Z\s]', frontmatter['slug']):
                review.add_critical("slug contains uppercase or spaces")
        
        # Check for summary
        if 'summary' not in frontmatter:
            review.add_warning("Missing 'summary' field (improves discoverability)")

        official_sources = frontmatter.get('official_sources', []) or []
        if official_sources and len(official_sources) < 3:
            review.add_warning(f"official_sources should cite at least 3 authoritative references (found {len(official_sources)})")
        if official_sources:
            domains = set()
            for source in official_sources:
                if isinstance(source, dict) and 'url' in source:
                    parsed = urlparse(source['url'])
                    domain = parsed.netloc or parsed.path.split('/')[0]
                    if domain:
                        domains.add(domain)
            if len(domains) == 1 and len(official_sources) > 1:
                domain = next(iter(domains)) or 'single domain'
                review.add_warning(f"official_sources all point to {domain}; diversify citations per Integrity Engine guidance")
    
    def check_content_structure(self, review: PolicyReview, content: str):
        """Check 2: Content Structure Validation"""
        # Expanded vague language detection
        vague_patterns = {
            'encourage': r'\b(encourage[ds]?|encouraging)\b',
            'strive to': r'\bstrive[sd]?\s+to\b',
            'should consider': r'\bshould\s+consider\b',
            'may wish to': r'\bmay\s+wish\s+to\b',
            'best effort': r'\bbest\s+effort[s]?\b',
            'as soon as feasible': r'\bas\s+soon\s+as\s+(feasible|possible|practicable)\b',
            'whenever possible': r'\bwhenever\s+(possible|practicable|feasible)\b',
            'should': r'\bshould\b(?!\s+(be|have|not))',  # "should" not followed by be/have/not
        }
        
        found_vague = []
        for term, pattern in vague_patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                found_vague.append(term)
        
        if found_vague:
            review.add_critical(f"Vague enforcement language detected: {', '.join(found_vague[:5])} → use 'shall', 'must', 'required'")
        
        # Check for numeric thresholds without units
        nums_without_units = self._find_numbers_without_units(content)
        if len(nums_without_units) > 5:
            review.add_warning("Multiple numeric values may be missing units")
        
        # Check for absolute dates (flag for conversion to relative timelines)
        absolute_dates = re.findall(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b', content)
        if absolute_dates:
            review.add_warning(f"Found {len(absolute_dates)} absolute dates; consider relative timelines (e.g., 'within 12 months of adoption')")

    def check_length_and_sections(self, review: PolicyReview, content: str):
        """Check supplemental structure requirements (line count + section coverage)."""
        non_empty_lines = [line for line in content.splitlines() if line.strip()]
        line_count = len(non_empty_lines)
        if line_count < self.min_policy_lines:
            review.add_warning(
                f"Policy body has {line_count} non-empty lines (<{self.min_policy_lines}); expand problem, mandate, implementation, and metrics sections"
            )

        headings = [title.strip().lower() for _, title in re.findall(r'^(#{1,6})\s+(.*)', content, re.MULTILINE)]
        missing_sections = []
        for label, keywords in self.section_keywords.items():
            if not any(any(keyword in heading for keyword in keywords) for heading in headings):
                missing_sections.append(label)

        if missing_sections:
            review.add_warning(
                "Missing required sections: " + ', '.join(missing_sections) +
                ". Add explicit headings for each step of the Integrity Engine workflow."
            )
    
    def check_overlap_redundancy(self, review: PolicyReview, frontmatter: dict, filepath: Path):
        """Check 3: Overlap & Redundancy Detection"""
        current_keywords = set(frontmatter.get('keywords', []))
        current_title = frontmatter.get('title', filepath.stem)
        
        for other_policy_path in self.all_policies:
            if other_policy_path == filepath:
                continue
            
            other_fm, _, _ = self.parse_policy(other_policy_path)
            other_keywords = set(other_fm.get('keywords', []))
            other_title = other_fm.get('title', other_policy_path.stem)
            
            # Keyword overlap
            shared_keywords = current_keywords & other_keywords
            if len(shared_keywords) >= 3:
                review.add_warning(f"Keyword overlap with '{other_policy_path.name}' ({len(shared_keywords)} shared: {', '.join(list(shared_keywords)[:3])})")
                review.add_recommendation(f"Review '{other_policy_path.stem}' for potential merge or scope differentiation")
            
            # Title similarity
            similarity = SequenceMatcher(None, current_title.lower(), other_title.lower()).ratio()
            if similarity > 0.7:
                review.add_warning(f"Title {similarity*100:.0f}% similar to '{other_title}'")
    
    def check_citation_integrity(self, review: PolicyReview, frontmatter: dict):
        """Check 4: Citation Integrity Audit"""
        official_sources = frontmatter.get('official_sources', [])
        
        if not official_sources:
            review.add_critical("No official_sources provided")
            return
        
        dead_links = []
        old_citations = []
        news_only = []
        
        for i, source in enumerate(official_sources):
            if isinstance(source, dict) and 'url' in source:
                url = source['url']
                # Quick URL check (can be made more robust)
                try:
                    response = requests.head(url, timeout=5, allow_redirects=True)
                    if response.status_code >= 400:
                        dead_links.append(f"official_sources[{i}]: {url} returns {response.status_code}")
                except Exception as e:
                    dead_links.append(f"official_sources[{i}]: {url} unreachable ({str(e)[:50]})")
                
                # Check for news sources
                parsed = urlparse(url)
                news_domains = ['cnn.com', 'bbc.com', 'reuters.com', 'apnews.com', 'theguardian.com', 'nytimes.com']
                if any(nd in parsed.netloc for nd in news_domains):
                    news_only.append(url)
        
        if dead_links:
            for link in dead_links:
                review.add_critical(link)
            review.add_recommendation("Replace dead links with Wayback Machine snapshots or updated URLs")
        else:
            review.add_pass("All official_sources URLs accessible")
        
        if news_only and len(official_sources) == len(news_only):
            review.add_warning("Only news articles as sources; add primary sources (legislation, reports)")
    
    def check_geographic_compatibility(self, review: PolicyReview, content: str, frontmatter: dict):
        """Check 5: Geographic & Legal System Compatibility"""
        # Check for seasonal terms (US-defaultism)
        seasonal_terms = re.findall(r'\b(summer|winter|fall|spring)\b', content, re.IGNORECASE)
        if seasonal_terms:
            review.add_warning(f"Seasonal terms detected ({len(seasonal_terms)} occurrences); consider climate-neutral terms like 'dry season', 'wet season'")
        
        # Check for imperial-only units
        imperial_only = re.findall(r'\b\d+\s*(feet|ft|inches|in|miles|mi|fahrenheit|°F)\b', content, re.IGNORECASE)
        if imperial_only and not re.search(r'\b(meters|metres|m|celsius|°C|kilometers|km)\b', content, re.IGNORECASE):
            review.add_warning("Imperial units only; consider adding metric equivalents")
    
    def check_readability(self, review: PolicyReview, content: str):
        """Check 6: Accessibility & Readability"""
        # Simple Flesch-Kincaid approximation (sentences and syllables)
        sentences = len(re.split(r'[.!?]+', content))
        words = len(content.split())
        
        if words > 0 and sentences > 0:
            avg_words_per_sentence = words / sentences
            if avg_words_per_sentence > 25:
                review.add_warning(f"Average sentence length {avg_words_per_sentence:.1f} words (consider simplifying for readability)")
        
        # Check for undefined acronyms (very basic heuristic)
        acronyms = self._filter_acronyms(content)
        if len(acronyms) > 10:
            review.add_warning(f"Found {len(acronyms)} potential acronyms; ensure all are defined on first use")
        
        # Check heading hierarchy
        headings = re.findall(r'^(#{1,6})\s', content, re.MULTILINE)
        if headings:
            levels = [len(h) for h in headings]
            for i in range(1, len(levels)):
                if levels[i] - levels[i-1] > 1:
                    review.add_warning(f"Heading hierarchy skip detected (h{levels[i-1]} to h{levels[i]})")
    
    def adversarial_stress_test(self, review: PolicyReview, content: str, llm_enabled: bool = False):
        """Check 7: Adversarial Stress Test (Red Team)"""
        # Enhanced enforcement mechanism detection
        enforcement_indicators = {
            'permit_license': r'\b(permit|license|approval|authorization)\s+(required|conditioning|shall\s+be\s+issued|revoked)\b',
            'penalty': r'\b(fine|penalty|sanction|violation|non-compliance)\s*(?:shall|must|of)\b',
            'inspection': r'\b(inspect|verify|audit|monitor|compliance\s+report)\b',
            'bonding': r'\b(bond|guarantee|deposit|escrow)\b',
            'disclosure': r'\b(public\s+registry|disclosure|transparency|notice|display)\b',
            'market_mechanism': r'\b(credits?|offsets?|ineligible|disqualified|subsidy|benefit)\b',
        }
        
        found_mechanisms = []
        for mechanism_type, pattern in enforcement_indicators.items():
            if re.search(pattern, content, re.IGNORECASE):
                found_mechanisms.append(mechanism_type.replace('_', ' '))
        
        if not found_mechanisms:
            review.add_critical("No enforcement mechanism or penalty clause detected")
        elif len(found_mechanisms) == 1 and found_mechanisms[0] == 'penalty':
            review.add_warning("Only penalty-based enforcement found; consider inspection or verification mechanisms")
        
        # Check for enforcement authority
        if not re.search(r'\b(department|authority|municipality|jurisdiction|agency|inspector)\s+(shall|must|responsible)\b', content, re.IGNORECASE):
            review.add_warning("No clear enforcement authority specified")

    def _find_numbers_without_units(self, content: str) -> List[str]:
        text = re.sub(r'https?://\S+', ' ', content)
        text = re.sub(r'ISO/IEC\s+\d[\d\-]*', ' ', text, flags=re.IGNORECASE)
        text = re.sub(r'ISO\s+\d[\d\-]*', ' ', text, flags=re.IGNORECASE)
        text = re.sub(r'IEC\s+\d[\d\-]*', ' ', text, flags=re.IGNORECASE)
        text = re.sub(r'PM\s*\d+(?:\.\d+)?', ' ', text, flags=re.IGNORECASE)
        text = re.sub(r'\b\d{1,2}:\d{2}\b', ' ', text)
        text = re.sub(r'^(#{1,6}\s+)\d+(?:\.\d+)?', r'\1', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)

        nums_without_units = []
        for match in re.finditer(r'\b\d+(?:\.\d+)?\b', text):
            num = match.group()
            if len(num) == 4 and num.startswith(('19', '20')):
                continue  # treat as year
            prefix_idx = max(0, match.start() - 1)
            if text[prefix_idx:match.start()] in {'-', '/', ':'}:
                continue
            following = text[match.end():match.end() + 12]
            if following.startswith(':'):
                continue  # time remaining after cleanup
            prefix_window = text[max(0, match.start() - 25):match.start()].lower()
            last_word = re.findall(r'[a-z]+', prefix_window)
            if last_word and last_word[-1] in self.prefix_skip_words:
                continue
            stripped_following = following.lstrip()
            if stripped_following.startswith(('–', '-')):
                range_tail = stripped_following.lstrip('–-')
                range_match = re.match(r'\s*\d+(?:\.\d+)?\s*([a-zA-Z°µ/%-]+)', range_tail)
                if range_match:
                    fragment = range_match.group(1).lower()
                    if any(fragment.startswith(token) for token in self.range_unit_tokens):
                        continue
            if self.unit_regex.search(following):
                continue
            nums_without_units.append(num)
        return nums_without_units

    def _filter_acronyms(self, content: str) -> List[str]:
        acronyms = re.findall(r'\b[A-Z]{2,}\b', content)
        filtered = []
        for acronym in acronyms:
            token = acronym.strip('.').upper()
            if token in self.acronym_allowlist:
                continue
            filtered.append(acronym)
        return filtered
        
        # Check for sunset clauses
        if re.search(r'\b(sunset|expire|repeal|terminate)\b.*\bautomatically\b', content, re.IGNORECASE):
            review.add_warning("Potential sunset clause vulnerability (automatic expiry)")
        
        if llm_enabled and self.llm_provider:
            # Use local LLM for deeper analysis
            prompt = f"""You are a policy red-team analyst. Review this policy excerpt and identify:
1. Loopholes that could be exploited
2. Missing enforcement mechanisms
3. Cost-shifting to vulnerable populations
4. Corruption risks

Policy excerpt:
{content[:2000]}

Respond in JSON format:
{{
  "loopholes": ["description"],
  "missing_enforcement": ["description"],
  "cost_shifting_risks": ["description"],
  "corruption_risks": ["description"]
}}
"""
            try:
                llm_result = self.query_llm(prompt)
                if llm_result:
                    for risk_type, risks in llm_result.items():
                        for risk in risks:
                            review.add_warning(f"LLM-detected {risk_type.replace('_', ' ')}: {risk}")
            except Exception as e:
                review.add_warning(f"LLM analysis failed: {str(e)}")
    
    def query_llm(self, prompt: str) -> Optional[dict]:
        """Query local LLM for adversarial analysis."""
        if not self.llm_provider or self.llm_provider not in LLM_PROVIDERS:
            return None

        # Build endpoints by provider
        if self.llm_provider == 'ollama':
            endpoint = f"{self.ollama_base.rstrip('/')}/api/generate"
            payload = {"model": self.llm_model, "prompt": prompt, "stream": False}
            response = requests.post(endpoint, json=payload, timeout=self.timeout)
            if response.ok:
                result = response.json().get('response', '')
                try:
                    return json.loads(result)
                except Exception:
                    return None
            return None
        elif self.llm_provider == 'lm-studio':
            endpoint = f"{self.lmstudio_base.rstrip('/')}/v1/completions"
            payload = {"model": self.llm_model, "prompt": prompt}
            response = requests.post(endpoint, json=payload, timeout=self.timeout)
            if response.ok:
                txt = response.json().get('choices', [{}])[0].get('text', '')
                try:
                    return json.loads(txt)
                except Exception:
                    return None
            return None
        elif self.llm_provider == 'llama-cpp':
            endpoint = f"{self.llamacpp_base.rstrip('/')}/completion"
            payload = {"prompt": prompt}
            response = requests.post(endpoint, json=payload, timeout=self.timeout)
            if response.ok:
                txt = response.json().get('content', '') or response.text
                try:
                    return json.loads(txt)
                except Exception:
                    return None
            return None
        
        return None
    
    def review_policy(self, filepath: Path) -> PolicyReview:
        """Run full review on a single policy."""
        review = PolicyReview(str(filepath))
        review.frontmatter, review.content, is_properly_closed = self.parse_policy(filepath)
        
        print(f"Reviewing {filepath.name}...")
        
        self.check_frontmatter_consistency(review, review.frontmatter, filepath, is_properly_closed)
        self.check_length_and_sections(review, review.content)
        self.check_content_structure(review, review.content)
        self.check_overlap_redundancy(review, review.frontmatter, filepath)
        self.check_citation_integrity(review, review.frontmatter)
        self.check_geographic_compatibility(review, review.content, review.frontmatter)
        self.check_readability(review, review.content)
        self.adversarial_stress_test(review, review.content, llm_enabled=bool(self.llm_provider))
        
        return review
    
    def review_all(self) -> List[PolicyReview]:
        """Review all policies in the directory."""
        reviews = []
        for policy_path in self.all_policies:
            reviews.append(self.review_policy(policy_path))
        return reviews


def main():
    parser = argparse.ArgumentParser(description="Agent D: Consistency Guardian - Policy Quality Checker")
    parser.add_argument('policy', nargs='?', help="Path to specific policy file to review")
    parser.add_argument('--all', action='store_true', help="Review all policies")
    parser.add_argument('--changed', action='store_true', help="Review only git-modified policies")
    parser.add_argument('--llm', choices=['ollama', 'llama-cpp', 'lm-studio'], help="Enable LLM-powered adversarial analysis")
    parser.add_argument('--model', default='llama3', help="LLM model name (default: llama3)")
    parser.add_argument('--policies-dir', default='_policies', help="Path to policies directory")
    parser.add_argument('--output', help="Save report to file instead of stdout")
    
    args = parser.parse_args()
    
    guardian = ConsistencyGuardian(
        policies_dir=args.policies_dir,
        llm_provider=args.llm,
        llm_model=args.model
    )
    
    reviews = []
    
    if args.all:
        reviews = guardian.review_all()
    elif args.changed:
        # Get changed files from git
        import subprocess
        result = subprocess.run(['git', 'diff', '--name-only', 'HEAD'], capture_output=True, text=True)
        changed_files = [f for f in result.stdout.split('\n') if f.startswith('_policies/') and f.endswith('.md')]
        for filepath in changed_files:
            reviews.append(guardian.review_policy(Path(filepath)))
    elif args.policy:
        reviews.append(guardian.review_policy(Path(args.policy)))
    else:
        parser.print_help()
        sys.exit(1)
    
    # Generate and output reports
    output = []
    critical_count = 0
    escalation_count = 0
    
    for review in reviews:
        output.append(review.format_report())
        critical_count += len(review.critical)
        if review.should_escalate():
            escalation_count += 1
    
    report = "\n".join(output)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report saved to {args.output}")
    else:
        print(report)
    
    # Summary
    print("\n" + "="*60)
    print(f"Reviewed {len(reviews)} policies")
    print(f"Total critical issues: {critical_count}")
    print(f"Policies requiring escalation: {escalation_count}")
    
    # Allow overriding fail behavior via environment
    fail_on_critical = os.getenv('CG_FAIL_ON_CRITICAL', 'true').lower() in ('1', 'true', 'yes')
    if fail_on_critical and critical_count > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
