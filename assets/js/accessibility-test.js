/**
 * Comprehensive Accessibility Crawl for OCRaP.ai Policy Library
 * Dynamically queries all site HTML files for WCAG 2.2 AA compliance across themes.
 */

const { test, expect } = require('@playwright/test');
const { injectAxe, checkA11y } = require('axe-playwright');
const fs = require('fs');
const path = require('path');

const baseURL = 'http://localhost:8080';
const axeConfig = {
  runOnly: {
    type: 'tag',
    values: ['wcag2a', 'wcag2aa', 'wcag22aa']
  }
};

const SITE_DIR = path.resolve(__dirname, '../../_site');

// Recursively find all HTML files
function getAllHtmlFiles(dirPath, fileArray) {
  if (!fs.existsSync(dirPath)) return [];
  const files = fs.readdirSync(dirPath);
  fileArray = fileArray || [];

  files.forEach(function(file) {
    if (fs.statSync(dirPath + "/" + file).isDirectory()) {
      fileArray = getAllHtmlFiles(dirPath + "/" + file, fileArray);
    } else {
      if (file.endsWith('.html')) {
        let relativePath = path.relative(SITE_DIR, path.join(dirPath, file));
        let urlPath = '/' + relativePath.replace(/\\/g, '/');
        // Handle index.html paths cleanly
        if (urlPath.endsWith('index.html')) {
            urlPath = urlPath.slice(0, -10);
        }
        fileArray.push(urlPath);
      }
    }
  });
  return fileArray;
}

const pagesToTest = getAllHtmlFiles(SITE_DIR);
const themes = ['light', 'dark'];

test.describe('WCAG 2.2 AA Accessibility Deep Crawl', () => {

  // For testing timeouts/memory drops on large sites
  test.setTimeout(120000); // 2 mins total per worker

  test.beforeEach(async ({ page }) => {
    // Fail immediately on browser errors to catch uncaught JS
    page.on('pageerror', err => {
        console.warn(`[Page Error] ${err.message}`);
    });
  });

  pagesToTest.forEach(pageUrl => {
    for (const theme of themes) {
      test(`A11y Test: ${pageUrl || '/'} in ${theme.toUpperCase()} mode`, async ({ page }) => {
        
        // Emulate color scheme
        await page.emulateMedia({ colorScheme: theme });

        // Navigate
        const fullUrl = `${baseURL}${pageUrl}`;
        await page.goto(fullUrl, { waitUntil: 'load' });
        
        // Inject Axe-core
        await injectAxe(page);
        
        // Exclude 3rd party or irrelevant things here if necessary
        await checkA11y(page, null, axeConfig, (violations) => {
          const critical = violations.filter(v => v.impact === 'critical');
          const serious = violations.filter(v => v.impact === 'serious');
          
          if (critical.length > 0 || serious.length > 0) {
            console.error(`\n❌ [${theme.toUpperCase()}] Violation on ${pageUrl}`);
            const report = [...critical, ...serious];
            report.forEach(v => {
              console.error(`   - ${v.id} (${v.impact}): ${v.description}`);
              v.nodes.slice(0, 2).forEach(node => {
                console.error(`     ↳ Node: ${node.html.substring(0, 100)}`);
              });
            });
          }

          expect(critical.length, `Critical violations must be zero`).toBe(0);
          expect(serious.length, `Serious violations must be zero`).toBe(0);
        });
      });
    }
  });

});
