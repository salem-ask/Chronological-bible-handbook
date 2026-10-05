# Chronological Bible Handbook — Bookline Sales Funnel

A lightweight, mobile-first sales funnel for the **Chronological Bible Handbook** (illustrated 106-page PDF, KJV), sold by **Bookline** through a **Chariow** checkout.

It is plain HTML, CSS and vanilla JavaScript. There is no framework, no build step and no dependencies apart from one optional Google Font (Cormorant Garamond, headings only).

The page doesn't show a price, testimonials, ratings, countdowns or social proof. All purchase buttons send the visitor straight to the Chariow checkout. This website never handles payment and never delivers the PDF itself.

---

## 1. Project structure

```
/
├── index.html          Sales page
├── thank-you.html      Post-purchase page (set as Chariow's redirect URL, optional)
├── styles.css          All styles (mobile-first)
├── script.js           Timeline viewer, sticky mobile CTA, WhatsApp share link, footer year
├── README.md           This file
└── images/
    ├── poster.jpg / poster.webp                  Hero poster (book cover), 800 × 1191
    ├── page-preview-1.jpg / .webp                Timeline page 1 (Creation → Judges)
    ├── page-preview-2.jpg / .webp                Timeline page 2 (Kings → Exile)
    ├── page-preview-3.jpg / .webp                Timeline page 3 (Restoration → Apostles)
    └── page-preview-4.jpg / .webp                Timeline page 4 (Paul → Revelation)
```

Each image comes in two versions. Browsers that support WebP load the lighter `.webp` file, and the others use the `.jpg` (`<picture>` element).

Sales page sections, in order: Hero → The problem → The solution (+ CTA) → What's inside (+ CTA) → Who it's for → Preview (the 4-page timeline) → Offer recap (+ CTA) → FAQ → Final CTA (+ Share on WhatsApp) → Footer. On mobile there is also a sticky CTA bar.

---

## 2. The poster

The poster is `images/poster.jpg` (with `images/poster.webp`). It was extracted from the supplied `Chronological.pdf`.

To replace it, overwrite both files with an image of the same proportions (800 × 1191). If the ratio changes, update `width`/`height` on the hero `<img>` in `index.html` and `aspect-ratio` on `.poster-frame` in `styles.css`.

The `og:image` and `twitter:image` tags use `[PAGE_URL]images/poster.jpg`. Once `[PAGE_URL]` is replaced (see §8), they become the absolute URL that WhatsApp and Facebook need.

## 3. The preview pages (4-page biblical timeline)

The four preview images are the four pages of the biblical timeline. I rebuilt them from the supplied `ligne_du_temps.pdf`, which contained three overlapping screenshots: I removed the overlaps and the black separator bars, then cut the result back into the four original pages.

The Preview section shows them in a viewer with two modes:

- **Book view** (default): one page at a time on phones, and an open book (two-page spread) on screens 900 px and wider. Visitors turn pages with the Previous/Next buttons, by swiping left/right, or with the keyboard arrow keys.
- **Scroll view**: the four pages are joined into one continuous timeline inside a scrollable frame.

Tapping a page opens it full size, so visitors can zoom in to read the small text. Without JavaScript, the page falls back to scroll view.

To replace a page, overwrite `images/page-preview-N.jpg` **and** `images/page-preview-N.webp` with the same filenames.

## 4. Chariow CTA link

All 7 purchase buttons point to:

```
https://livresenligne.mychariow.shop/prd_2j3myxax/checkout
```

The buttons are: Hero, after "The solution", after "What's inside", after the Free Bonuses, Offer recap, Final CTA, and the mobile sticky bar. They open in the same tab. To change the link, search and replace this URL in `index.html`.

**Optional:** in your Chariow product settings, set the post-purchase redirect URL to `https://your-domain.com/thank-you.html`.

## 5. WhatsApp support number

The support number is **+243 823 226 790**. It is written as `243823226790` in the links (`https://wa.me/243823226790?...`):

- `index.html`: the FAQ answer about download difficulties and the footer "WhatsApp support" link
- `thank-you.html`: the "WhatsApp Support" button

The number is never displayed as plain text. To change it, search and replace `243823226790` (international format, digits only, no `+`).

## 5b. Bookline website link

The "Bookline" name in the header and footer, and the copyright line, link to **https://bookline.digital/**. These links open in a new tab, so visitors keep the sales page open. To change the address, search and replace `https://bookline.digital/` in both HTML files.

## 5c. Free bonuses

The sales page presents three bonuses, all **included FREE with the purchase**, with no monetary value shown: the "Free Bonuses" section right after "What's inside", plus the Offer Recap and an FAQ entry.

| Bonus | Sales-page cover | Delivered file |
|---|---|---|
| 1. The Chronological Bible Reading Plan (365 Days) | `images/bonus-reading-plan.*` | `bonuses/Chronological-Bible-Reading-Plan-365-Days.pdf` |
| 2. Biblical Timeline Poster | `images/bonus-timeline-poster.*` | **not produced here; upload your poster file to Chariow** |
| 3. Archaeology and the Bible: 12 Discoveries That Illuminate the Biblical Story | `images/bonus-archaeology.*` | `bonuses/Archaeology-and-the-Bible-12-Discoveries.pdf` |

**Upload the bonus PDFs to your Chariow product** so that buyers receive them with the handbook. This website never delivers files.

### The `bonuses/` folder (production files, never published)

```
bonuses/
├── Chronological-Bible-Reading-Plan-365-Days.pdf   ← upload to Chariow
├── Archaeology-and-the-Bible-12-Discoveries.pdf    ← upload to Chariow
├── covers/          supplied covers + corrected archaeology cover + timeline-poster cover
├── reading-plan/    chronological_order.py, build_plan.py, handbook-pages.json, template.html
├── archaeology/     discoveries.py (all texts), build_archaeology.py, template.html
├── fonts/           Lora and Poppins (SIL Open Font License)
├── print.css        shared print styles
└── build-pdf.js     HTML → A4 PDF (Playwright + pdfunite)
```

The folder is excluded from deployment: `_config.yml` covers GitHub Pages, `netlify.toml` returns a 404 for `/bonuses/*` on Netlify, and `.vercelignore` covers Vercel. Do not remove these files.

### Handbook page numbers in the reading plan

I didn't invent any Handbook page numbers. `bonuses/reading-plan/handbook-pages.json` lists the 66 books with `null` pages, and the PDF shows a blank (`p. ___`) wherever a page is missing. To print the real pages, fill in the numbers from the Handbook's summary tables and rebuild:

```bash
python3 bonuses/reading-plan/build_plan.py
node bonuses/build-pdf.js bonuses/reading-plan/reading-plan.html bonuses/covers/Bonus_Reading_Plan_Cover.jpg bonuses/Chronological-Bible-Reading-Plan-365-Days.pdf "The Chronological Bible Reading Plan"
```

The readings are balanced using the KJV word count of each chapter (`kjv-chapter-words.json`). The 1,189 chapters are each read once. The average day is about 2,170 words, roughly 15 minutes at a comfortable pace.

### Rebuilding the archaeology guide

```bash
python3 bonuses/archaeology/build_archaeology.py
node bonuses/build-pdf.js bonuses/archaeology/archaeology.html bonuses/covers/Bonus_Archaeology_Cover.jpg bonuses/Archaeology-and-the-Bible-12-Discoveries.pdf "Archaeology and the Bible"
```

### About the covers

- **Archaeology cover:** the supplied cover read "12 Discoveries That *Confirm* the Biblical Story". To match the title and the rule that archaeology does not prove the Bible, `Bonus_Archaeology_Cover.jpg` is a copy with the subtitle changed to "*Illuminate*". The original is kept as `Bonus_Archaeology_Cover_original.jpg`.
- **Timeline poster cover:** no cover was supplied, so `Bonus_Timeline_Poster_Cover.png` was made in the same style (source: `covers/timeline-poster-cover.html`). Replace `images/bonus-timeline-poster.jpg` and `.webp` if you have an official cover.

## 6. Meta Pixel

In both `index.html` and `thank-you.html`, find:

```html
<!-- META PIXEL PLACEHOLDER: Add your Meta Pixel code here -->
```

and paste the base Pixel code from Meta Events Manager directly below it, inside `<head>`. On the sales page you can track CTA clicks as `InitiateCheckout`. A Purchase event is only reliable if Chariow redirects buyers to `thank-you.html`, or if you use Chariow's own Pixel integration, if it offers one.

## 7. Google Analytics 4

In both HTML files, find:

```html
<!-- GOOGLE ANALYTICS 4 PLACEHOLDER: Add your GA4 measurement ID here -->
```

and paste the GA4 `gtag.js` snippet with your own `G-XXXXXXX` ID directly below it.

## 8. Page URL — `[PAGE_URL]`

Once you know your final domain, replace `[PAGE_URL]` in `index.html` with the full URL of the sales page, **ending with a `/`**, for example `https://your-domain.com/`. It appears in `<link rel="canonical">`, `og:url`, `og:image` and `twitter:image`.

The **Share on WhatsApp** buttons don't depend on this. `script.js` inserts the real page address automatically, and on the thank-you page it shares the sales page instead. `[PAGE_URL]` also appears URL-encoded (`%5BPAGE_URL%5D`) in the share links' fallback `href`, which is only used if JavaScript is disabled. You can replace it there too.

---

## 9. Deploying

### Netlify
1. Go to [app.netlify.com](https://app.netlify.com) → **Add new site** → **Deploy manually**, and drag the project folder onto the page.
   *Or* connect the GitHub repository: **Import from Git**, leave the build command **empty**, and set the publish directory to `/`.
2. Optional: **Domain settings** → add your custom domain.

### Vercel
1. Go to [vercel.com/new](https://vercel.com/new) → import the GitHub repository.
2. Framework preset: **Other**. Build command: **none**. Output directory: `./` (root).
3. Click **Deploy**. Add your domain under **Settings → Domains**.

### GitHub Pages
1. Push the files to a GitHub repository, with `index.html` at the root.
2. **Settings → Pages → Build and deployment**: Source = *Deploy from a branch*, Branch = `main` (or your branch), folder `/ (root)`.
3. Your site will be at `https://<username>.github.io/<repository>/`. All paths in this project are relative, so they work in a sub-folder.

After deploying, replace `[PAGE_URL]` with the live URL. Then test the link preview by pasting the URL into WhatsApp, or by using the [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/).

---

## 10. Performance notes

- Excluding images, the page is about 50 KB of HTML, CSS and JS before compression. The only external request is the Google Font (two weights, `display=swap`). To remove it, delete the three font `<link>` tags; headings then fall back to Georgia/serif.
- The hero poster loads first (`fetchpriority="high"`, about 125 KB as WebP). The timeline pages (about 50–80 KB each as WebP) are `loading="lazy"`. In book view, the script loads the next pages just before they are needed.
- Icons are inline SVG, so there are no icon fonts and no extra requests.
- The FAQ uses native `<details>`, so it needs no JavaScript.

## 11. Pre-launch test checklist

- [ ] Every "Get the Handbook" button opens the Chariow checkout in the same tab
- [ ] WhatsApp support opens a chat with your number
- [ ] Share on WhatsApp opens WhatsApp with the message and the live URL
- [ ] Poster displays; the timeline viewer works in Book view and Scroll view
- [ ] Test on a real Android phone (Chrome), at 360 px width, on mobile data
- [ ] The sticky bar appears after the hero on mobile and is hidden on desktop

---

## Remaining placeholders checklist

```
[PAGE_URL]    index.html — canonical, og:url, og:image, twitter:image (+ URL-encoded in the no-JS share fallback links in both files)
```

Also paste the Meta Pixel and GA4 code at their commented placeholders.
