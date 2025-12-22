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
const AxeBuilder = require('axe-playwright').default;

// Test configuration
const BASE_URL = 'http://localhost:4000';
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
  
  test('Home page accessibility', async ({ page }) => {
    await page.goto(BASE_URL);
    
    const results = await new AxeBuilder({ page })
      .withTags(AXE_CONFIG.runOnly.values)
      .analyze();
    
    const analysis = analyzeResults(results);
    
    // Log all violations for review
    console.log(`\nHome Page Results: ${analysis.total} total violations`);
    console.log(formatViolations(analysis.critical, 'critical'));
    console.log(formatViolations(analysis.serious, 'serious'));
    console.log(formatViolations(analysis.moderate, 'moderate'));
    console.log(formatViolations(analysis.minor, 'minor'));
    
    // Enforce thresholds (fail on critical or serious)
    expect(analysis.critical.length, 'Critical violations must be zero').toBe(0);
    expect(analysis.serious.length, 'Serious violations must be zero').toBe(0);
  });
  
  test('Policy index page accessibility', async ({ page }) => {
    await page.goto(`${BASE_URL}/policies/`);
    
    const results = await new AxeBuilder({ page })
      .withTags(AXE_CONFIG.runOnly.values)
      .analyze();
    
    const analysis = analyzeResults(results);
    
    console.log(`\nPolicy Index Results: ${analysis.total} total violations`);
    console.log(formatViolations(analysis.critical, 'critical'));
    console.log(formatViolations(analysis.serious, 'serious'));
    console.log(formatViolations(analysis.moderate, 'moderate'));
    console.log(formatViolations(analysis.minor, 'minor'));
    
    expect(analysis.critical.length, 'Critical violations must be zero').toBe(0);
    expect(analysis.serious.length, 'Serious violations must be zero').toBe(0);
  });
  
  test('Sample policy page accessibility', async ({ page }) => {
    // Test solar-parking as it has full official_sources
    await page.goto(`${BASE_URL}/policies/solar-parking/`);
    
    const results = await new AxeBuilder({ page })
      .withTags(AXE_CONFIG.runOnly.values)
      .analyze();
    
    const analysis = analyzeResults(results);
    
    console.log(`\nSample Policy Results: ${analysis.total} total violations`);
    console.log(formatViolations(analysis.critical, 'critical'));
    console.log(formatViolations(analysis.serious, 'serious'));
    console.log(formatViolations(analysis.moderate, 'moderate'));
    console.log(formatViolations(analysis.minor, 'minor'));
    
    expect(analysis.critical.length, 'Critical violations must be zero').toBe(0);
    expect(analysis.serious.length, 'Serious violations must be zero').toBe(0);
  });
});
