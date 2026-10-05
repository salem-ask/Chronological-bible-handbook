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

  /* ---------- Timeline viewer: book view / scroll view ---------- */
  (function timelineViewer() {
    var viewer = document.getElementById('tl-viewer');
    if (!viewer) return;
    var pages = viewer.querySelectorAll('.tl-page');
    var modes = viewer.querySelector('.tl-modes');
    var modeButtons = viewer.querySelectorAll('.tl-mode');
    var nav = viewer.querySelector('.tl-nav');
    var prev = viewer.querySelector('.tl-prev');
    var next = viewer.querySelector('.tl-next');
    var status = viewer.querySelector('.tl-status');
    var stage = viewer.querySelector('.tl-stage');
    var wide = window.matchMedia('(min-width: 900px)');
    var total = pages.length;
    var index = 0; // first page shown (0-based)
    var mode = 'book';

    function step() { return wide.matches ? 2 : 1; }

    function render() {
      var s = step();
      index = Math.floor(index / s) * s; // spreads always start on an odd page (1–2, 3–4)
      viewer.classList.toggle('is-spread', s === 2);
      for (var i = 0; i < total; i++) {
        var on = i >= index && i < index + s;
        pages[i].classList.toggle('is-current', on);
        pages[i].classList.toggle('is-left', on && s === 2 && i === index);
        pages[i].classList.toggle('is-right', on && s === 2 && i === index + 1);
        // Load the visible pages and the next ones early so page turns feel instant.
        if (i < index + s * 2) {
          var img = pages[i].querySelector('img');
          if (img) img.loading = 'eager';
        }
      }
      var last = Math.min(index + s, total);
      status.textContent = s === 2 && last > index + 1
        ? 'Pages ' + (index + 1) + '–' + last + ' of ' + total
        : 'Page ' + (index + 1) + ' of ' + total;
      prev.disabled = index === 0;
      next.disabled = index + s >= total;
    }

    function go(dir) {
      var target = index + dir * step();
      if (target < 0 || target >= total) return;
      index = target;
      viewer.classList.toggle('go-back', dir < 0);
      render();
    }

    function setMode(m) {
      mode = m;
      viewer.classList.toggle('is-book', m === 'book');
      viewer.classList.toggle('is-scroll', m === 'scroll');
      nav.hidden = m !== 'book';
      for (var i = 0; i < modeButtons.length; i++) {
        modeButtons[i].setAttribute('aria-pressed', modeButtons[i].getAttribute('data-mode') === m ? 'true' : 'false');
      }
      if (m === 'book') render();
      else for (var j = 0; j < total; j++) pages[j].classList.remove('is-current', 'is-left', 'is-right');
    }

    for (var b = 0; b < modeButtons.length; b++) {
      modeButtons[b].addEventListener('click', function () { setMode(this.getAttribute('data-mode')); });
    }
    prev.addEventListener('click', function () { go(-1); });
    next.addEventListener('click', function () { go(1); });

    stage.addEventListener('keydown', function (e) {
      if (mode !== 'book') return;
      if (e.key === 'ArrowRight') { go(1); e.preventDefault(); }
      if (e.key === 'ArrowLeft') { go(-1); e.preventDefault(); }
    });

    // Swipe left/right to turn pages; a swipe must not open the full-size image.
    var startX = 0, startY = 0, swiped = false;
    stage.addEventListener('touchstart', function (e) {
      startX = e.touches[0].clientX; startY = e.touches[0].clientY; swiped = false;
    }, { passive: true });
    stage.addEventListener('touchend', function (e) {
      if (mode !== 'book') return;
      var dx = e.changedTouches[0].clientX - startX;
      var dy = e.changedTouches[0].clientY - startY;
      if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) { swiped = true; go(dx < 0 ? 1 : -1); }
    });
    stage.addEventListener('click', function (e) {
      if (swiped) { e.preventDefault(); swiped = false; }
    }, true);

    if (wide.addEventListener) wide.addEventListener('change', function () { if (mode === 'book') render(); });

    modes.hidden = false;
    setMode('book');
  })();

  /* ---------- 48-hour offer timer ----------
     Counts down to the end of the current 48-hour period, then starts again.
     All visitors see the same time. Set ENABLED to false to hide every timer. */
  (function offerTimer() {
    var ENABLED = true;
    var PERIOD_HOURS = 48;
    var ANCHOR = Date.UTC(2026, 0, 1, 0, 0, 0); // start of the first period (UTC)

    var timers = document.querySelectorAll('[data-countdown]');
    if (!ENABLED || !timers.length) return;
    var period = PERIOD_HOURS * 3600 * 1000;

    function pad(n) { return (n < 10 ? '0' : '') + n; }
    function tick() {
      var left = period - ((Date.now() - ANCHOR) % period);
      var sec = Math.floor(left / 1000);
      var h = pad(Math.floor(sec / 3600)), m = pad(Math.floor(sec % 3600 / 60)), s = pad(sec % 60);
      for (var i = 0; i < timers.length; i++) {
        timers[i].querySelector('[data-h]').textContent = h;
        timers[i].querySelector('[data-m]').textContent = m;
        timers[i].querySelector('[data-s]').textContent = s;
      }
    }
    for (var i = 0; i < timers.length; i++) timers[i].hidden = false;
    tick();
    setInterval(tick, 1000);
  })();

  /* ---------- Sticky mobile CTA ---------- */
  var sticky = document.getElementById('sticky-cta');
  var hero = document.getElementById('hero');
  if (!sticky || !hero) return;

  var stickyLink = sticky.querySelector('a');
  var finalCta = document.getElementById('final-cta');
  var heroVisible = true;
  var finalVisible = false;
  var endVisible = false;

  function update() {
    var show = !heroVisible && !finalVisible && !endVisible;
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

    var offerEnd = document.getElementById('offer-end');
    if (offerEnd) {
      // Also hide the bar over the bottom offer block, which has its own button.
      new IntersectionObserver(function (entries) {
        endVisible = entries[0].isIntersecting;
        update();
      }).observe(offerEnd);
    }

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
