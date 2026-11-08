#!/usr/bin/env node
/* Render check for a built handout (Part 7 of the workflow).
 *
 *   node template/render_check.js handouts/2026/47-hosea-joel.html [outDir]
 *
 * For 1000px and 390px widths it: loads the file, waits past the 2.5 s reveal
 * failsafe, takes a full-page screenshot, and reports
 *   - horizontal page overflow (page wider than the viewport)
 *   - elements whose right edge sticks out past the viewport
 *   - .reveal sections still hidden
 *   - the hero SVG's box vs. its container (clipping)
 * Then it prints to PDF (Letter, print CSS) and confirms the print button is
 * hidden and every section is visible in print mode.
 * Screenshots/PDF go to outDir (default: .renders/, which git ignores).
 * Exit code 1 if any check fails. LOOK AT THE SCREENSHOTS anyway.
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const file = process.argv[2];
  if (!file) { console.error('usage: node template/render_check.js <handout.html> [outDir]'); process.exit(2); }
  const outDir = process.argv[3] || path.join(path.dirname(__dirname), '.renders');
  fs.mkdirSync(outDir, { recursive: true });
  const url = 'file://' + path.resolve(file);
  const base = path.basename(file, '.html');
  const browser = await chromium.launch();
  let failures = 0;
  const fail = (m) => { failures++; console.log('  ✗ ' + m); };

  for (const width of [1000, 390]) {
    const page = await browser.newPage({ viewport: { width, height: 900 }, deviceScaleFactor: 1 });
    await page.goto(url, { waitUntil: 'load' });
    await page.waitForTimeout(3000);           // past the 2.5 s reveal failsafe
    const r = await page.evaluate(() => {
      const vw = document.documentElement.clientWidth;
      const over = [];
      document.querySelectorAll('body *').forEach(el => {
        const b = el.getBoundingClientRect();
        if (b.width && b.right > vw + 1 && !el.closest('.stars') && getComputedStyle(el).position !== 'fixed')
          over.push(`${el.tagName.toLowerCase()}.${[...el.classList].join('.')} right=${Math.round(b.right)}`);
      });
      const hidden = [...document.querySelectorAll('.reveal')].filter(e => getComputedStyle(e).opacity < 0.99).length;
      const art = document.querySelector('.hero-art'), svg = art && art.querySelector('svg');
      let svgClip = null;
      if (svg) { const a = art.getBoundingClientRect(), s = svg.getBoundingClientRect();
        svgClip = s.left < a.left - 1 || s.right > a.right + 1 || s.right > vw + 1; }
      return { scrollW: document.documentElement.scrollWidth, vw, over: over.slice(0, 12), overN: over.length,
               hidden, svgClip, sections: document.querySelectorAll('section.block').length,
               h2: [...document.querySelectorAll('h2.sec')].map(h => h.textContent) };
    });
    console.log(`\n${width}px: page ${r.scrollW}px wide, ${r.sections} sections`);
    if (r.scrollW > r.vw + 1) fail(`horizontal scroll: page is ${r.scrollW}px in a ${r.vw}px viewport`);
    if (r.overN) fail(`${r.overN} element(s) overflow the viewport: ${r.over.join('; ')}`);
    if (r.hidden) fail(`${r.hidden} .reveal section(s) still hidden after 3 s`);
    if (r.svgClip) fail('hero SVG is clipped or overflows its container');
    if (r.sections !== 5) fail(`expected 5 sections, found ${r.sections}`);
    const shot = path.join(outDir, `${base}-${width}.png`);
    await page.screenshot({ path: shot, fullPage: true });
    console.log('  screenshot: ' + shot);
    if (width === 1000) console.log('  sections: ' + r.h2.join(' | '));
    await page.close();
  }

  // print / PDF check — load fresh and print immediately, so only the print
  // failsafes (beforeprint + print CSS) can be what makes sections visible
  const page = await browser.newPage({ viewport: { width: 1000, height: 900 } });
  await page.goto(url, { waitUntil: 'load' });
  await page.emulateMedia({ media: 'print' });
  const pr = await page.evaluate(() => ({
    btn: getComputedStyle(document.querySelector('.printbtn')).display,
    hidden: [...document.querySelectorAll('.reveal')].filter(e => getComputedStyle(e).opacity < 0.99).length,
    adjust: getComputedStyle(document.querySelector('.hero')).printColorAdjust ||
            getComputedStyle(document.querySelector('.hero')).webkitPrintColorAdjust }));
  const pdf = path.join(outDir, `${base}.pdf`);
  await page.pdf({ path: pdf, format: 'Letter', printBackground: true, margin: { top: '0.4in', bottom: '0.4in', left: '0.4in', right: '0.4in' } });
  console.log(`\nprint: button display=${pr.btn}, hidden sections=${pr.hidden}, print-color-adjust=${pr.adjust}`);
  if (pr.btn !== 'none') fail('print button visible in print');
  if (pr.hidden) fail(`${pr.hidden} section(s) hidden in print`);
  if (pr.adjust !== 'exact') fail('print-color-adjust is not exact');
  console.log('  pdf: ' + pdf + ` (${Math.round(fs.statSync(pdf).size / 1024)} KB)`);
  await browser.close();
  console.log(failures ? `\n${failures} problem(s) found` : '\nall automated checks passed — now look at the screenshots');
  process.exit(failures ? 1 : 0);
})();
