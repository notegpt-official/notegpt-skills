// competitor-tdk-fetcher.mjs
// Usage: node competitor-tdk-fetcher.mjs
// Fetches Title + meta description from competitor pages using Playwright headless Chromium.
// Designed for page-seo-generator Phase 1.5.

import { chromium } from 'playwright';

// ── CONFIG: Replace with current competitor URLs ──
const COMPETITORS = [
  // ["Name", "https://full-url-to-feature-page"],
  // Example: ["Fotor", "https://www.fotor.com/image-upscaler/"],
];

// ── CHROMIUM PATH: Adjust for your Playwright cache ──
const CHROMIUM_PATH = process.env.PLAYWRIGHT_CHROMIUM_PATH || null;

// Chromium cache locations (macOS):
//   ~/Library/Caches/ms-playwright/chromium-XXXX/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing
// To find yours: ls ~/Library/Caches/ms-playwright/chromium-*/chrome-mac-arm64/

const launchOpts = {
  headless: true,
  args: ['--disable-blink-features=AutomationControlled', '--disable-dev-shm-usage'],
};
if (CHROMIUM_PATH) launchOpts.executablePath = CHROMIUM_PATH;

const browser = await chromium.launch(launchOpts);

for (const [name, url] of COMPETITORS) {
  let ctx;
  try {
    ctx = await browser.newContext({
      locale: 'en-US',
      viewport: { width: 1440, height: 900 },
      userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    });
    const page = await ctx.newPage();

    // Stealth: suppress webdriver detection
    await page.addInitScript(() => {
      Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
      Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
      Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
      window.chrome = { runtime: {} };
    });

    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 35000 });
    await page.waitForTimeout(5000);

    const title = await page.title();
    const desc = await page.$eval('meta[name="description"]', el => el.content).catch(() => null);
    const ogDesc = desc ? null : await page.$eval('meta[property="og:description"]', el => el.content).catch(() => null);
    const descFinal = desc || ogDesc || null;

    // Output in parse-friendly format
    console.log(`RESULT|${name}|${title.length}|${title}|${descFinal ? descFinal.length : 0}|${descFinal || 'NONE'}`);
  } catch (e) {
    const errMsg = e.message?.substring(0, 120) || String(e);
    console.log(`ERROR|${name}|0|${errMsg}|0|NONE`);
  } finally {
    if (ctx) await ctx.close().catch(() => {});
  }
}

await browser.close();