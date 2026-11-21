/* ProductBeacon: the Google Analytics accept or decline choice (email-list plan, row 23).
   Nothing from Google Analytics is requested until the reader presses Accept.
   The choice is kept in this browser's localStorage under "pb-analytics-choice", with its date,
   and the bar asks again 12 months after the choice. Nothing is sent to us or anyone else.
   Texts: email-list-2026-11-15/phase-1/05-texts.md, section 9, word for word, except one change in the bar sentence: "Google" became "Google Analytics" (owner ruling, 19 Nov 2026). */
(function () {
  'use strict';
  var GA_ID = 'G-TC1LMMGQGV';
  var KEY = 'pb-analytics-choice';
  var MONTHS = 12;
  var TEXT = 'We use Google Analytics to count page visits. It sets cookies on your device. Nothing from Google Analytics loads unless you press Accept.';
  var LINK_TEXT = 'Privacy notice';
  var ACCEPT = 'Accept';
  var DECLINE = 'Decline';
  var FOOTER_LINK = 'Analytics choice';
  var NOW_TEXT = 'Your choice now: {choice}. You can change it here.';

  var bar = null, now = null, footerBtn = null, loaded = false, reopened = false;

  function read() {
    try {
      var v = JSON.parse(window.localStorage.getItem(KEY));
      if (!v || (v.choice !== 'accepted' && v.choice !== 'declined')) return null;
      var until = new Date(v.at);
      if (isNaN(until.getTime())) return null;
      until.setMonth(until.getMonth() + MONTHS);
      return new Date() < until ? v.choice : null;
    } catch (e) { return null; }
  }

  function save(choice) {
    try { window.localStorage.setItem(KEY, JSON.stringify({ choice: choice, at: new Date().toISOString() })); } catch (e) { /* storage blocked: the choice holds for this page only */ }
  }

  function loadAnalytics() {
    window['ga-disable-' + GA_ID] = false;
    if (loaded) return;
    loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.length = 0; // drop anything a page queued before the reader said yes
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID);
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  }

  function clearCookies() {
    var host = location.hostname.split('.');
    document.cookie.split(';').forEach(function (c) {
      var name = c.split('=')[0].trim();
      if (name !== '_ga' && name.indexOf('_ga_') !== 0) return;
      document.cookie = name + '=; Max-Age=0; path=/';
      for (var i = 0; i < host.length - 1; i++) {
        document.cookie = name + '=; Max-Age=0; path=/; domain=' + host.slice(i).join('.');
      }
    });
  }

  function stopAnalytics() {
    window['ga-disable-' + GA_ID] = true; // Google's own switch: no further hits from this page
    clearCookies();
  }

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text) e.textContent = text;
    return e;
  }

  function injectStyles() {
    var css =
      '.pb-ac{position:fixed;left:0;right:0;bottom:0;z-index:999;background:var(--surface,#1E293B);border-top:1px solid var(--border,#334155);color:var(--text,#F1F5F9);font-family:var(--font-sans,system-ui,sans-serif);font-size:15px;line-height:1.5}' +
      '.pb-ac:focus{outline:none}' +
      '.pb-ac__inner{display:flex;flex-wrap:wrap;align-items:center;gap:12px 24px;max-width:var(--container,1200px);margin:0 auto;padding:16px 24px}' +
      '.pb-ac__copy{flex:1 1 320px}.pb-ac__copy p{margin:0}' +
      '.pb-ac__copy a{color:inherit;text-decoration:underline;text-underline-offset:3px}.pb-ac__copy a:hover{color:var(--amber,#F59E0B)}' +
      '.pb-ac__now{margin-top:6px!important;color:var(--secondary,#94A3B8)}' +
      '.pb-ac__btns{display:flex;gap:12px}' +
      '.pb-ac__btn{min-width:112px;min-height:44px;padding:10px 20px;border:1px solid var(--secondary,#94A3B8);border-radius:var(--border-radius-xs,6px);background:transparent;color:var(--bright,#F8FAFC);font:inherit;font-weight:600;cursor:pointer}' +
      '.pb-ac__btn:hover{border-color:var(--amber,#F59E0B);color:var(--amber,#F59E0B)}' +
      '.pb-ac__btn:focus-visible,.pb-ac-link:focus-visible{outline:2px solid var(--amber,#F59E0B);outline-offset:2px}' +
      '.pb-ac-link{padding:0;border:0;background:none;font:inherit;cursor:pointer}' +
      '@media(max-width:480px){.pb-ac__inner{padding:16px}.pb-ac__btns{width:100%}.pb-ac__btn{flex:1}}';
    var s = el('style');
    s.textContent = css;
    document.head.appendChild(s);
  }

  function buildBar() {
    bar = el('section', 'pb-ac');
    bar.setAttribute('aria-label', FOOTER_LINK);
    bar.tabIndex = -1;
    var inner = el('div', 'pb-ac__inner');
    var copy = el('div', 'pb-ac__copy');
    var p = el('p', 'pb-ac__text', TEXT + ' ');
    var a = el('a', '', LINK_TEXT);
    a.href = '/privacy/';
    p.appendChild(a);
    now = el('p', 'pb-ac__now');
    now.hidden = true;
    copy.appendChild(p);
    copy.appendChild(now);
    var btns = el('div', 'pb-ac__btns');
    [[ACCEPT, 'accepted'], [DECLINE, 'declined']].forEach(function (b) {
      var btn = el('button', 'pb-ac__btn', b[0]);
      btn.type = 'button';
      btn.addEventListener('click', function () { choose(b[1]); });
      btns.appendChild(btn);
    });
    inner.appendChild(copy);
    inner.appendChild(btns);
    bar.appendChild(inner);
    bar.hidden = true;
    document.body.appendChild(bar);
  }

  function showBar(fromFooter) {
    if (!bar) buildBar();
    reopened = fromFooter;
    var c = read();
    now.hidden = !(fromFooter && c);
    if (c) now.textContent = NOW_TEXT.replace('{choice}', c);
    bar.hidden = false;
    document.body.style.paddingBottom = bar.offsetHeight + 'px';
    if (fromFooter) bar.focus();
  }

  function choose(choice) {
    save(choice);
    bar.hidden = true;
    document.body.style.paddingBottom = '';
    if (reopened && footerBtn) footerBtn.focus();
    if (choice === 'accepted') loadAnalytics(); else stopAnalytics();
  }

  function addFooterLink() {
    footerBtn = el('button', 'footer__privacy pb-ac-link', FOOTER_LINK);
    footerBtn.type = 'button';
    footerBtn.addEventListener('click', function () { showBar(true); });
    var privacy = document.querySelector('footer .footer__privacy');
    if (privacy) {
      privacy.parentNode.insertBefore(footerBtn, privacy.nextSibling);
      privacy.parentNode.insertBefore(document.createTextNode(' · '), footerBtn);
    } else {
      (document.querySelector('footer') || document.body).appendChild(footerBtn);
    }
  }

  function init() {
    injectStyles();
    addFooterLink();
    var c = read();
    if (c === 'accepted') { loadAnalytics(); return; }
    clearCookies(); // also removes cookies set before this choice existed
    if (!c) showBar(false);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
