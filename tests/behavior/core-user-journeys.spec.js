const { test, expect } = require('@playwright/test');

test.describe('Core user journeys (BDD pilot)', () => {
  test('BDD-001: search page supports policy query and results', async ({ page }) => {
    await page.goto('/search/', { waitUntil: 'load' });

    await expect(page.getByRole('heading', { name: 'Search' })).toBeVisible();

    const searchInput = page.locator('.pagefind-ui__search-input');
    await expect(searchInput).toBeVisible();
    await searchInput.fill('solar');

    await expect(page.locator('.pagefind-ui__result').first()).toBeVisible({ timeout: 15000 });
  });

  test('BDD-002: policy detail is reachable from policy library', async ({ page }) => {
    await page.goto('/policies/', { waitUntil: 'load' });

    const firstPolicyLink = page.locator('.policy-list-item h3 a').first();
    await expect(firstPolicyLink).toBeVisible();
    await firstPolicyLink.click();

    await expect(page).toHaveURL(/\/policies\//);
    await expect(page.locator('article.policy-content h1')).toBeVisible();
    await expect(page.getByRole('link', { name: /Back to Policy Library|Back to policies/i }).first()).toBeVisible();
  });

  test('BDD-003: policy library pagination navigates to next page', async ({ page }) => {
    await page.goto('/policies/', { waitUntil: 'load' });

    const pageIndicator = page.locator('#page-indicator');
    await expect(pageIndicator).toContainText('Page 1 of');

    const nextLink = page.locator('#next-link');
    await expect(nextLink).toBeVisible();
    await nextLink.click();

    await expect(page).toHaveURL(/\/policies\/\?page=2/);
    await expect(pageIndicator).toContainText('Page 2 of');
  });
});
