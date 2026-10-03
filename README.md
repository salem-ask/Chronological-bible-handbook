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
├── script.js           Sticky mobile CTA, WhatsApp share link, footer year
├── README.md           This file
└── images/
    ├── poster.jpg            ← add your poster here (recommended name)
    ├── page-preview-1.jpg    ← add
    ├── page-preview-2.jpg    ← add
    ├── page-preview-3.jpg    ← add
    └── page-preview-4.jpg    ← add
```

Until the real images are added, the page shows clearly labelled placeholders in A4 portrait proportions (210 × 297). These are not fake images. When an image file is missing, the page removes the broken image and leaves the placeholder visible.

Sales page sections, in order: Hero → The problem → The solution (+ CTA) → What's inside (+ CTA) → Who it's for → Preview → Offer recap (+ CTA) → FAQ → Final CTA (+ Share on WhatsApp) → Footer. On mobile there is also a sticky CTA bar.

---

## 2. Replacing the poster — `[POSTER_IMAGE]`

1. Export the poster as a **JPG or WebP**, portrait, about **800 × 1131 px** (A4 ratio). Compress it to **under ~150 KB** (for example with [squoosh.app](https://squoosh.app)).
2. Save it as `images/poster.jpg`.
3. In `index.html`, replace `[POSTER_IMAGE]` in **3 places**:
   - **Hero image** (`<img src="[POSTER_IMAGE]" …>`): use the relative path `images/poster.jpg`.
   - **`og:image`** and **`twitter:image`** meta tags: use the **full absolute URL**, for example `https://your-domain.com/images/poster.jpg`. WhatsApp and Facebook previews need an absolute URL.

If your poster has a different ratio, change `width`/`height` on the hero `<img>` and `aspect-ratio` on `.poster-frame` in `styles.css`.

## 3. Replacing the four preview images

Save four sample pages in `images/` with **exactly these names**:

```
images/page-preview-1.jpg
images/page-preview-2.jpg
images/page-preview-3.jpg
images/page-preview-4.jpg
```

You don't need to change any code. They load automatically and are lazy-loaded. Recommended: about 600 × 848 px (A4 portrait), compressed to **60–120 KB each**.

If you want more specific alt text (for example "Page showing the 10 plagues table"), edit the `alt` attributes in the Preview section of `index.html`.

*Optional, WebP:* to serve WebP with a JPG fallback, wrap each image in `<picture>` with a `<source type="image/webp" srcset="images/page-preview-1.webp">`. Only do this if you have created the `.webp` files.

## 4. Inserting the Chariow CTA link — `[CTA_LINK]`

Search and replace **`[CTA_LINK]`** in `index.html` with your exact Chariow product/checkout URL. Do not change the URL itself. There are **6** occurrences:

| # | Location |
|---|----------|
| 1 | Hero button |
| 2 | After "The solution" |
| 3 | After "What's inside" |
| 4 | Offer recap |
| 5 | Final CTA ("Get the Chronological Bible Handbook") |
| 6 | Mobile sticky CTA bar |

All of them open in the same tab, and the JavaScript never rewrites them.

**Optional:** in your Chariow product settings, set the post-purchase redirect URL to `https://your-domain.com/thank-you.html`.

## 5. Inserting the WhatsApp support number — `[WHATSAPP_SUPPORT_NUMBER]`

Replace `[WHATSAPP_SUPPORT_NUMBER]` with your number in **international format, digits only**. Leave out the `+`, spaces and the leading 0. For example, Nigeria `2348012345678` or Kenya `254712345678`.

Occurrences:
- `index.html`: FAQ answer "What if I have difficulty downloading my purchase?" and the footer "WhatsApp support" link (2)
- `thank-you.html`: "WhatsApp Support" button (1)

The number is never displayed as plain text. Visitors reach you through the button only.

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

Once you know your final domain, replace `[PAGE_URL]` in `index.html` (`<link rel="canonical">` and `og:url`) with the full URL of the sales page, for example `https://your-domain.com/`.

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

After deploying, replace `[PAGE_URL]` and the `og:image` / `twitter:image` values with the live URLs. Then test the link preview by pasting the URL into WhatsApp, or by using the [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/).

---

## 10. Performance notes

- Excluding images, the page is about 50 KB of HTML, CSS and JS before compression. The only external request is the Google Font (two weights, `display=swap`). To remove it, delete the three font `<link>` tags; headings then fall back to Georgia/serif.
- The hero poster loads first (`fetchpriority="high"`). All preview images are `loading="lazy"`.
- Icons are inline SVG, so there are no icon fonts and no extra requests.
- The FAQ uses native `<details>`, so it needs no JavaScript.

## 11. Pre-launch test checklist

- [ ] Every "Get the Handbook" button opens the Chariow checkout in the same tab
- [ ] WhatsApp support opens a chat with your number
- [ ] Share on WhatsApp opens WhatsApp with the message and the live URL
- [ ] Poster and four previews display correctly
- [ ] Test on a real Android phone (Chrome), at 360 px width, on mobile data
- [ ] The sticky bar appears after the hero on mobile and is hidden on desktop

---

## Remaining placeholders checklist

```
[CTA_LINK]                  index.html (6×) — Chariow checkout URL
[POSTER_IMAGE]              index.html (3×) — hero img, og:image, twitter:image
[WHATSAPP_SUPPORT_NUMBER]   index.html (2×), thank-you.html (1×)
[PAGE_URL]                  index.html — canonical, og:url (+ encoded in no-JS share fallback links in both files)
```

Also add the image files `images/page-preview-1.jpg` … `images/page-preview-4.jpg` and paste the Meta Pixel and GA4 code at their commented placeholders.
