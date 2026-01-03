/**
 * Accessibility Tests for OCRaP.ai Policy Library
 * Per AGENTS.md Section 11: Automated WCAG 2.2 AA compliance checks
 * 
 * Thresholds (from AGENTS.md):
 * - Critical violations: 0 allowed (fail build)
 * - Serious violations: 0 allowed (fail build)
 * - Moderate violations: Warning only (do not fail build)
 * - Minor violations: Informational only
 */

const { test, expect } = require('@playwright/test');
const { injectAxe, checkA11y } = require('axe-playwright');

// Use Playwright's configured baseURL instead of hardcoding
// This allows the test to work with different environments (local, CI, etc.)
const AXE_CONFIG = {
  runOnly: {
    type: 'tag',
    values: ['wcag2a', 'wcag2aa', 'wcag22aa']
  }
};

/**
 * Analyze axe results and categorize violations by impact
 */
function analyzeResults(results) {
  const violations = results.violations || [];
  const critical = violations.filter(v => v.impact === 'critical');
  const serious = violations.filter(v => v.impact === 'serious');
  const moderate = violations.filter(v => v.impact === 'moderate');
  const minor = violations.filter(v => v.impact === 'minor');
  
  return { critical, serious, moderate, minor, total: violations.length };
}

/**
 * Format violation details for reporting
 */
function formatViolations(violations, impact) {
  if (violations.length === 0) return '';
  
  let output = `\n${impact.toUpperCase()} Violations (${violations.length}):\n`;
  violations.forEach(v => {
    output += `  - ${v.id}: ${v.description}\n`;
    output += `    Affects ${v.nodes.length} element(s)\n`;
    v.nodes.slice(0, 3).forEach(node => {
      output += `    → ${node.html.substring(0, 80)}...\n`;
    });
  });
  return output;
}

test.describe('WCAG 2.2 AA Accessibility Tests', () => {
  
  test('Home page accessibility', async ({ page, baseURL }) => {
    await page.goto(baseURL);
    await injectAxe(page);
    
    // Run accessibility check and report violations
    await checkA11y(page, null, {
      runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag22aa'] }
    }, (violations) => {
      const critical = violations.filter(v => v.impact === 'critical');
      const serious = violations.filter(v => v.impact === 'serious');
      
      console.log(`\nHome Page: ${violations.length} total violations`);
      console.log(formatViolations(critical, 'critical'));
      console.log(formatViolations(serious, 'serious'));
      
      expect(critical.length, 'Critical violations must be zero').toBe(0);
      expect(serious.length, 'Serious violations must be zero').toBe(0);
    });
  });
  
  test('Policy index page accessibility', async ({ page, baseURL }) => {
    await page.goto(`${baseURL}/policies/`);
    await injectAxe(page);
    
    await checkA11y(page, null, {
      runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag22aa'] }
    }, (violations) => {
      const critical = violations.filter(v => v.impact === 'critical');
      const serious = violations.filter(v => v.impact === 'serious');
      
      console.log(`\nPolicy Index: ${violations.length} total violations`);
      console.log(formatViolations(critical, 'critical'));
      console.log(formatViolations(serious, 'serious'));
      
      expect(critical.length, 'Critical violations must be zero').toBe(0);
      expect(serious.length, 'Serious violations must be zero').toBe(0);
    });
  });
  
  test('Sample policy page accessibility', async ({ page, baseURL }) => {
    // Test solar-parking as it has full official_sources
    await page.goto(`${baseURL}/policies/solar-parking/`);
    await injectAxe(page);
    
    await checkA11y(page, null, {
      runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag22aa'] }
    }, (violations) => {
      const critical = violations.filter(v => v.impact === 'critical');
      const serious = violations.filter(v => v.impact === 'serious');
      
      console.log(`\nSample Policy: ${violations.length} total violations`);
      console.log(formatViolations(critical, 'critical'));
      console.log(formatViolations(serious, 'serious'));
      
      expect(critical.length, 'Critical violations must be zero').toBe(0);
      expect(serious.length, 'Serious violations must be zero').toBe(0);
    });
  });
});
