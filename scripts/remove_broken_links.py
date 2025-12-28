#!/usr/bin/env python3
"""
Remove specific broken links from policy files.
This script removes URLs that return 404/403/500 errors.
"""

import re
from pathlib import Path

# Define broken URLs to remove (exact matches)
BROKEN_URLS = [
    # EU publication links (404)
    "https://op.europa.eu/en/publication-detail/-/publication/3b6b0f4c-8f2a-11ea-9e4e-01aa75ed71a1",
    "https://op.europa.eu/en/publication-detail/-/publication/5d6f0f88-7b6a-11ea-9e4e-01aa75ed71a1",
    "https://op.europa.eu/en/publication-detail/-/publication/8f3c6b3b-2d3a-11ea-8c1f-01aa75ed71a1",
    "https://op.europa.eu/en/publication-detail/-/publication/8b1c6b3b-3e2a-11ea-8c1f-01aa75ed71a1",
    "https://op.europa.eu/en/publication-detail/-/publication/9f3c6b3b-2d3a-11ea-8c1f-01aa75ed71a1",
    "https://op.europa.eu/en/publication-detail/-/publication/1f3c6b3b-2d3a-11ea-8c1f-01aa75ed71a1",
    "https://op.europa.eu/en/publication-detail/-/publication/3a6f0f88-7b6a-11ea-9e4e-01aa75ed71a1",
    # EC topic pages (404)
    "https://commission.europa.eu/publications/circular-economy-package_en",
    "https://commission.europa.eu/publications/smart-finance-smart-buildings_en",
    "https://environment.ec.europa.eu/topics/climate-change-adaptation_en",
    "https://commission.europa.eu/publications/social-europe_en",
    "https://ec.europa.eu/transport/themes/urban/urban_mobility_en",
    # Gov sites (unreachable/moved)
    "https://www.tokyo-co2tcap.jp/en/",
    "https://www.boston.gov/departments/environment/building-emissions-reduction-and-disclosure-ordinance",
    "https://www.denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Department-of-Climate-Action-Sustainability-and-Resiliency/Cutting-Denvers-Carbon-Pollution/Energize-Denver",
    "https://www.energy.gov.au/energy-efficiency/commercial-buildings/commercial-building-disclosure",
    "https://www.energy.ca.gov/programs-and-topics/programs/building-energy-benchmarking",
    # Right to repair (404)
    "https://single-market-economy.ec.europa.eu/sectors/retail/eu-right-repair_en",
    # Placeholder PMCID
    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMCXXXXX",
]

def remove_source_entry(content, url):
    """Remove an official_sources entry containing the specified URL."""
    # Pattern to match source entry with this URL (multi-line)
    # Handles both formats:
    #   - url: "URL"\n    title: "..."\n    accessed: "..."
    #   - title: "..."\n    url: "URL"\n    note: "..."
    
    # First try: url comes first
    pattern1 = r'  - url: "' + re.escape(url) + r'"\n(?:    .*\n)*?(?=  - |official_sources:|improvements:|summary:|hazard_type:|^---$)'
    content = re.sub(pattern1, '', content, flags=re.MULTILINE)
    
    # Second try: title comes first
    pattern2 = r'  - title: ".*?"\n    url: "' + re.escape(url) + r'"\n(?:    .*\n)*?(?=  - |official_sources:|improvements:|summary:|hazard_type:|^---$)'
    content = re.sub(pattern2, '', content, flags=re.MULTILINE)
    
    return content

def main():
    policies_dir = Path("_policies")
    removed_count = 0
    
    for policy_file in sorted(policies_dir.glob("*.md")):
        content = policy_file.read_text(encoding="utf-8")
        original_content = content
        
        # Remove each broken URL
        for url in BROKEN_URLS:
            if url in content:
                content = remove_source_entry(content, url)
                if content != original_content:
                    print(f"  Removed {url} from {policy_file.name}")
                    removed_count += 1
                    original_content = content
        
        # Write back if changed
        if content != policy_file.read_text(encoding="utf-8"):
            policy_file.write_text(content, encoding="utf-8")
            print(f"✓ Updated {policy_file.name}")
    
    print(f"\nTotal URLs removed: {removed_count}")

if __name__ == "__main__":
    main()
