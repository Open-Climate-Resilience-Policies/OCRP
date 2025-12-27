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
        self.all_policies = list(self.policies_dir.glob("*.md"))
        
    def parse_policy(self, filepath: Path) -> tuple[dict, str]:
        """Extract frontmatter and content from policy file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split frontmatter and content
        parts = re.split(r'^---\s*$', content, flags=re.MULTILINE, maxsplit=2)
        if len(parts) < 3:
            return {}, content
        
        frontmatter = yaml.safe_load(parts[1]) or {}
        markdown_content = parts[2].strip()
        
        return frontmatter, markdown_content
    
    def check_frontmatter_consistency(self, review: PolicyReview, frontmatter: dict, filepath: Path):
        """Check 1: Frontmatter Consistency"""
        required_fields = ['date', 'slug', 'keywords', 'official_sources']
        missing = [f for f in required_fields if f not in frontmatter]
        
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
    
    def check_content_structure(self, review: PolicyReview, content: str):
        """Check 2: Content Structure Validation"""
        vague_terms = re.findall(r'\b(encourage|strive to|should consider|may wish to)\b', content, re.IGNORECASE)
        if vague_terms:
            review.add_critical(f"Vague enforcement language detected: {', '.join(set(vague_terms[:3]))} → use 'shall', 'must', 'required'")
        
        # Check for numeric thresholds without units
        nums_without_units = re.findall(r'\b(\d+(?:\.\d+)?)\s*(?![°CFKcmkgmlftsq])', content)
        if len(nums_without_units) > 5:
            review.add_warning("Multiple numeric values may be missing units")
        
        # Check for absolute dates (flag for conversion to relative timelines)
        absolute_dates = re.findall(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b', content)
        if absolute_dates:
            review.add_warning(f"Found {len(absolute_dates)} absolute dates; consider relative timelines (e.g., 'within 12 months of adoption')")
    
    def check_overlap_redundancy(self, review: PolicyReview, frontmatter: dict, filepath: Path):
        """Check 3: Overlap & Redundancy Detection"""
        current_keywords = set(frontmatter.get('keywords', []))
        current_title = frontmatter.get('title', filepath.stem)
        
        for other_policy_path in self.all_policies:
            if other_policy_path == filepath:
                continue
            
            other_fm, _ = self.parse_policy(other_policy_path)
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
        acronyms = re.findall(r'\b[A-Z]{2,}\b', content)
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
        # Basic pattern matching for common vulnerabilities
        if not re.search(r'\b(penalty|fine|enforcement|violation|compliance)\b', content, re.IGNORECASE):
            review.add_critical("No enforcement mechanism or penalty clause detected")
        
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
        review.frontmatter, review.content = self.parse_policy(filepath)
        
        print(f"Reviewing {filepath.name}...")
        
        self.check_frontmatter_consistency(review, review.frontmatter, filepath)
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
