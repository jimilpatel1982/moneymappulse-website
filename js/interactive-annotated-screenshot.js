/**
 * InteractiveAnnotatedScreenshot — responsive product tour for guide pages.
 */
(function () {
  var CIRCLED = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨'];
  var DESKTOP_MIN = 1024;

  function parseTourData(root) {
    var el = root.querySelector('.interactive-tour__data');
    if (!el) return [];
    try {
      return JSON.parse(el.textContent);
    } catch (e) {
      return [];
    }
  }

  function isDesktopLayout() {
    return window.matchMedia('(min-width: ' + DESKTOP_MIN + 'px)').matches;
  }

  function renderPanel(ann, index) {
    var label = CIRCLED[index] || String(index + 1);
    var source = ann.source
      ? '<p class="interactive-tour__meta interactive-tour__meta--source">' +
        '<span class="interactive-tour__meta-label">Source</span>' +
        '<span class="interactive-tour__meta-value">' +
        ann.source +
        '</span></p>'
      : '';
    var example = ann.example
      ? '<p class="interactive-tour__meta interactive-tour__meta--example">' +
        '<span class="interactive-tour__meta-label">Example</span>' +
        '<span class="interactive-tour__meta-value">' +
        ann.example +
        '</span></p>'
      : '';
    var tip = ann.tip
      ? '<div class="interactive-tour__tip">' +
        '<span class="interactive-tour__meta-label">Tip</span>' +
        '<p class="interactive-tour__tip-text">' +
        ann.tip +
        '</p></div>'
      : '';
    return (
      '<div class="interactive-tour__panel-header">' +
      '<span class="interactive-tour__panel-badge" aria-hidden="true">' +
      label +
      '</span>' +
      '<h3 class="interactive-tour__panel-title">' +
      ann.title +
      '</h3>' +
      '</div>' +
      '<p class="interactive-tour__panel-desc">' +
      ann.description +
      '</p>' +
      '<div class="interactive-tour__panel-details">' +
      source +
      example +
      '</div>' +
      tip
    );
  }

  function initTour(root) {
    var annotations = parseTourData(root);
    if (!annotations.length) return;

    var panel = root.querySelector('[data-tour-panel]');
    if (!panel) return;

    var spotlights = root.querySelectorAll('[data-tour-spotlight]');
    var prevBtn = root.querySelector('[data-tour-prev]');
    var nextBtn = root.querySelector('[data-tour-next]');
    var markerGroups = {};

    root.querySelectorAll('[data-tour-marker]').forEach(function (btn) {
      var idx = parseInt(btn.getAttribute('data-tour-marker'), 10);
      if (!markerGroups[idx]) markerGroups[idx] = [];
      markerGroups[idx].push(btn);
    });

    var active = 0;

    function updateNav(index) {
      if (prevBtn) prevBtn.disabled = index <= 0;
      if (nextBtn) nextBtn.disabled = index >= annotations.length - 1;
    }

    function setActive(index) {
      if (index < 0 || index >= annotations.length) return;
      active = index;

      Object.keys(markerGroups).forEach(function (key) {
        var i = parseInt(key, 10);
        var isActive = i === index;
        markerGroups[key].forEach(function (btn) {
          btn.classList.toggle('is-active', isActive);
          btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
        });
      });

      spotlights.forEach(function (spot) {
        var i = parseInt(spot.getAttribute('data-tour-spotlight'), 10);
        spot.classList.toggle('is-active', i === index);
      });

      panel.classList.add('is-updating');
      window.requestAnimationFrame(function () {
        panel.innerHTML = renderPanel(annotations[index], index);
        panel.classList.remove('is-updating');
        updateNav(index);
      });
    }

    root.querySelectorAll('[data-tour-marker]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        setActive(parseInt(btn.getAttribute('data-tour-marker'), 10));
      });
    });

    if (prevBtn) {
      prevBtn.addEventListener('click', function () {
        setActive(active - 1);
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener('click', function () {
        setActive(active + 1);
      });
    }

    root.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        e.preventDefault();
        var next = Math.min(active + 1, annotations.length - 1);
        setActive(next);
        if (markerGroups[next] && markerGroups[next][0]) markerGroups[next][0].focus();
      }
      if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault();
        var prev = Math.max(active - 1, 0);
        setActive(prev);
        if (markerGroups[prev] && markerGroups[prev][0]) markerGroups[prev][0].focus();
      }
    });

    var touchStartX = 0;
    var swipeTarget = root.querySelector('[data-tour-swipe]') || panel;
    swipeTarget.addEventListener(
      'touchstart',
      function (e) {
        if (isDesktopLayout()) return;
        if (!e.changedTouches || !e.changedTouches.length) return;
        touchStartX = e.changedTouches[0].screenX;
      },
      { passive: true }
    );
    swipeTarget.addEventListener('touchend', function (e) {
      if (isDesktopLayout()) return;
      if (!e.changedTouches || !e.changedTouches.length) return;
      var dx = e.changedTouches[0].screenX - touchStartX;
      if (Math.abs(dx) < 48) return;
      if (dx < 0) setActive(Math.min(active + 1, annotations.length - 1));
      else setActive(Math.max(active - 1, 0));
    });

    setActive(0);
  }

  function initAll() {
    document.querySelectorAll('.interactive-tour').forEach(initTour);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }
})();
