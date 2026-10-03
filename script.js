/* Bookline — Chronological Bible Handbook
   Minimal vanilla JS: sticky mobile CTA, WhatsApp share link, footer year.
   Purchase CTA links are plain HTML and are never modified by this script. */
(function () {
  'use strict';

  var SHARE_MESSAGE =
    'I found this Chronological Bible Handbook that helps you understand the Bible in chronological order. You can learn more here: ';

  /* ---------- WhatsApp share: use the real page URL ---------- */
  function salesPageUrl() {
    var canonical = document.querySelector('link[rel="canonical"]');
    var href = canonical && canonical.getAttribute('href');
    // Use the canonical URL once the [PAGE_URL] placeholder has been replaced.
    if (href && href.indexOf('[') === -1 && /^https?:\/\//.test(href)) return href;
    // On the thank-you page, share the sales page rather than the thank-you page.
    var target = document.body.getAttribute('data-share-target');
    var url = new URL(target || window.location.href, window.location.href);
    url.hash = '';
    url.search = '';
    return url.href;
  }

  var shareUrl = salesPageUrl();
  var shareLinks = document.querySelectorAll('.js-share');
  for (var i = 0; i < shareLinks.length; i++) {
    shareLinks[i].href = 'https://wa.me/?text=' + encodeURIComponent(SHARE_MESSAGE + shareUrl);
  }

  /* ---------- Footer year ---------- */
  var years = document.querySelectorAll('.js-year');
  for (var y = 0; y < years.length; y++) years[y].textContent = new Date().getFullYear();

  /* ---------- Sticky mobile CTA ---------- */
  var sticky = document.getElementById('sticky-cta');
  var hero = document.getElementById('hero');
  if (!sticky || !hero) return;

  var stickyLink = sticky.querySelector('a');
  var finalCta = document.getElementById('final-cta');
  var heroVisible = true;
  var finalVisible = false;

  function update() {
    var show = !heroVisible && !finalVisible;
    sticky.classList.toggle('is-visible', show);
    sticky.setAttribute('aria-hidden', show ? 'false' : 'true');
    if (stickyLink) stickyLink.tabIndex = show ? 0 : -1;
    // Reserve space at the bottom so the bar never hides page content.
    document.body.classList.toggle('has-sticky', show);
  }

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      heroVisible = entries[0].isIntersecting;
      update();
    }).observe(hero);

    if (finalCta) {
      // Hide the bar while the final CTA section is on screen (avoids two identical buttons).
      new IntersectionObserver(function (entries) {
        finalVisible = entries[0].isIntersecting;
        update();
      }, { threshold: 0.25 }).observe(finalCta);
    }
  } else {
    // Fallback for very old browsers
    var onScroll = function () {
      heroVisible = window.pageYOffset < hero.offsetTop + hero.offsetHeight;
      update();
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }
})();
