/**
 * MoneyMap Pulse static site — minimal progressive enhancement.
 * Site works fully without JavaScript.
 */

(function () {
  var yearEl = document.getElementById('current-year');
  if (yearEl) {
    yearEl.textContent = String(new Date().getFullYear());
  }
})();
