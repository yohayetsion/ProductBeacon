/* ProductBeacon — Main JS
   Nav toggle, scroll animations, active link highlighting */

(function () {
  'use strict';

  // ---- Mobile Nav Toggle ----
  const hamburger = document.querySelector('.nav__hamburger');
  const mobileNav = document.querySelector('.nav__mobile');
  const mobileLinks = document.querySelectorAll('.nav__mobile a');

  if (hamburger && mobileNav) {
    hamburger.addEventListener('click', function () {
      const isOpen = mobileNav.classList.toggle('open');
      hamburger.setAttribute('aria-expanded', isOpen);

      if (isOpen) {
        // Focus first link
        const firstLink = mobileNav.querySelector('a');
        if (firstLink) firstLink.focus();
      }
    });

    // Close on link click
    mobileLinks.forEach(function (link) {
      link.addEventListener('click', function () {
        mobileNav.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
      });
    });

    // Close on Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mobileNav.classList.contains('open')) {
        mobileNav.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
        hamburger.focus();
      }
    });

    // Close on click outside
    document.addEventListener('click', function (e) {
      if (mobileNav.classList.contains('open') &&
        !mobileNav.contains(e.target) &&
        !hamburger.contains(e.target)) {
        mobileNav.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // ---- Smooth Scroll for Anchor Links ----
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var targetId = this.getAttribute('href');
      if (targetId === '#') return;

      var target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        var navHeight = document.querySelector('.nav') ? document.querySelector('.nav').offsetHeight : 0;
        var targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight;
        window.scrollTo({ top: targetPosition, behavior: 'smooth' });
      }
    });
  });

  // ---- Scroll Animations (IntersectionObserver) ----
  var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (!prefersReducedMotion) {
    var fadeElements = document.querySelectorAll('.fade-in');

    if (fadeElements.length > 0 && 'IntersectionObserver' in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target); // Fire once only
          }
        });
      }, {
        threshold: 0.15,
        rootMargin: '0px 0px -40px 0px'
      });

      fadeElements.forEach(function (el) {
        observer.observe(el);
      });
    }
  } else {
    // If reduced motion, make everything visible immediately
    document.querySelectorAll('.fade-in').forEach(function (el) {
      el.classList.add('visible');
    });
  }

  // ---- Active Nav Link Highlighting ----
  var sections = document.querySelectorAll('section[id]');
  var navLinks = document.querySelectorAll('.nav__links a[href^="#"]');

  if (sections.length > 0 && navLinks.length > 0) {
    function updateActiveLink() {
      var scrollPos = window.scrollY + 100;

      sections.forEach(function (section) {
        var top = section.offsetTop;
        var height = section.offsetHeight;
        var id = section.getAttribute('id');

        if (scrollPos >= top && scrollPos < top + height) {
          navLinks.forEach(function (link) {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + id) {
              link.classList.add('active');
            }
          });
        }
      });
    }

    var scrollTimer;
    window.addEventListener('scroll', function () {
      if (scrollTimer) cancelAnimationFrame(scrollTimer);
      scrollTimer = requestAnimationFrame(updateActiveLink);
    });
  }

})();
