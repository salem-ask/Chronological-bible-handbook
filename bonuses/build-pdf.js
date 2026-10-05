// Print a bonus HTML document to an A4 PDF with a full-page cover image.
//
//   node bonuses/build-pdf.js <document.html> <cover-image> <output.pdf> "<footer title>"
//
// Needs Playwright (Chromium) and pdfunite (poppler-utils).
const path = require('path');
const fs = require('fs');
const os = require('os');
const { execFileSync } = require('child_process');

let chromium;
try { ({ chromium } = require('playwright')); }
catch (e) { ({ chromium } = require('/opt/node-tools/node_modules/playwright')); }

(async () => {
  const [docPath, coverPath, outPath, title] = process.argv.slice(2);
  if (!docPath || !coverPath || !outPath) {
    console.error('usage: node build-pdf.js <document.html> <cover-image> <output.pdf> "<footer title>"');
    process.exit(1);
  }
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'bonus-'));
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // 1. Cover: the supplied cover image on its own page, edge to edge, no footer
  const coverUrl = 'file://' + path.resolve(coverPath);
  const coverHtml = path.join(tmp, 'cover.html');
  fs.writeFileSync(coverHtml, `<!DOCTYPE html><html><head><style>
    @page { size: A4; margin: 0; }
    html, body { margin: 0; height: 100%; background: #4A1519; }
    img { display: block; width: 210mm; height: 297mm; object-fit: cover; }
  </style></head><body><img src="${coverUrl}"></body></html>`);
  await page.goto('file://' + coverHtml);
  await page.waitForLoadState('networkidle');
  const coverPdf = path.join(tmp, 'cover.pdf');
  await page.pdf({ path: coverPdf, format: 'A4', printBackground: true, preferCSSPageSize: true });

  // 2. Body with a page-number footer
  await page.goto('file://' + path.resolve(docPath));
  await page.waitForLoadState('networkidle');
  await page.evaluate(() => document.fonts.ready);
  const bodyPdf = path.join(tmp, 'body.pdf');
  await page.pdf({
    path: bodyPdf,
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: `<div style="width:100%;font:7pt sans-serif;color:#8A6A1F;padding:0 16mm;display:flex;justify-content:space-between">
      <span>BOOKLINE &middot; ${title || ''}</span><span class="pageNumber"></span></div>`,
  });
  await browser.close();

  execFileSync('pdfunite', [coverPdf, bodyPdf, path.resolve(outPath)]);
  console.log('wrote', outPath);
})();
