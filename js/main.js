/**
 * MoneyMap Pulse static site — minimal progressive enhancement.
 * Site works fully without JavaScript (navigation links remain in the DOM).
 */

(function () {
  document.documentElement.classList.add('mobile-nav-js');

  var yearEl = document.getElementById('current-year');
  if (yearEl) {
    yearEl.textContent = String(new Date().getFullYear());
  }

  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.getElementById('site-navigation');

  if (!header || !toggle || !menu) {
    return;
  }

  var navLinks = menu.querySelectorAll('.nav a');

  function setOpen(open) {
    header.classList.toggle('is-nav-open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.setAttribute(
      'aria-label',
      open ? 'Close navigation menu' : 'Open navigation menu'
    );
  }

  function closeMenu() {
    setOpen(false);
  }

  toggle.addEventListener('click', function () {
    setOpen(!header.classList.contains('is-nav-open'));
  });

  navLinks.forEach(function (link) {
    link.addEventListener('click', closeMenu);
  });

  var ctaLink = menu.querySelector('.header-cta a');
  if (ctaLink) {
    ctaLink.addEventListener('click', closeMenu);
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && header.classList.contains('is-nav-open')) {
      closeMenu();
      toggle.focus();
    }
  });
})();
