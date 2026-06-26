/**
 * Moving & Storage of Jacksonville — Landing Page Scripts
 * jacksonvillelocalmovers.com
 */

(function () {
  'use strict';

  /* ──────────────────────────────────────────────
     1. DOM References
     ────────────────────────────────────────────── */
  const header       = document.getElementById('header');
  const hamburger    = document.getElementById('hamburger');
  const mobileNav    = document.getElementById('mobile-nav');
  const quoteModal   = document.getElementById('quote-modal');
  const modalClose   = document.getElementById('modal-close');
  const quoteTriggers = document.querySelectorAll('.quote-trigger');
  const faqItems     = document.querySelectorAll('.faq-item');
  const navLinks     = document.querySelectorAll('.header__nav a, .mobile-nav a:not(.mobile-nav__phone):not(.btn)');

  /* ──────────────────────────────────────────────
     2. Mobile Hamburger Menu
     ────────────────────────────────────────────── */
  if (hamburger && mobileNav) {
    hamburger.addEventListener('click', function () {
      const isOpen = mobileNav.classList.toggle('mobile-nav--open');
      hamburger.classList.toggle('hamburger--open', isOpen);
      hamburger.setAttribute('aria-expanded', isOpen);
      hamburger.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
      // Prevent body scroll when menu is open
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });
  }

  // Close mobile nav when a link is clicked
  navLinks.forEach(function (link) {
    link.addEventListener('click', function () {
      if (mobileNav && mobileNav.classList.contains('mobile-nav--open')) {
        mobileNav.classList.remove('mobile-nav--open');
        hamburger.classList.remove('hamburger--open');
        hamburger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    });
  });

  /* ──────────────────────────────────────────────
     3. Quote Form Modal (Popout)
     ────────────────────────────────────────────── */
  function openQuoteModal() {
    if (quoteModal) {
      quoteModal.classList.add('modal-overlay--open');
      document.body.style.overflow = 'hidden';
      // Focus the first input inside the modal
      const firstInput = quoteModal.querySelector('input');
      if (firstInput) setTimeout(function () { firstInput.focus(); }, 100);
    }
  }

  function closeQuoteModal() {
    if (quoteModal) {
      quoteModal.classList.remove('modal-overlay--open');
      document.body.style.overflow = '';
    }
  }

  // Open modal from any .quote-trigger button
  quoteTriggers.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      // Close mobile nav first if open
      if (mobileNav && mobileNav.classList.contains('mobile-nav--open')) {
        mobileNav.classList.remove('mobile-nav--open');
        hamburger.classList.remove('hamburger--open');
      }
      openQuoteModal();
    });
  });

  // Close modal via X button
  if (modalClose) {
    modalClose.addEventListener('click', closeQuoteModal);
  }

  // Close modal via overlay click (outside the form)
  if (quoteModal) {
    quoteModal.addEventListener('click', function (e) {
      if (e.target === quoteModal) {
        closeQuoteModal();
      }
    });
  }

  // Close modal via Escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && quoteModal && quoteModal.classList.contains('modal-overlay--open')) {
      closeQuoteModal();
    }
  });

  /* ──────────────────────────────────────────────
     4. FAQ Accordion
     ────────────────────────────────────────────── */
  faqItems.forEach(function (item) {
    const question = item.querySelector('.faq-question');
    if (question) {
      question.addEventListener('click', function () {
        const isOpen = item.classList.contains('faq-item--open');

        // Close all other FAQ items (single-open behavior)
        faqItems.forEach(function (other) {
          if (other !== item) {
            other.classList.remove('faq-item--open');
            const otherBtn = other.querySelector('.faq-question');
            if (otherBtn) otherBtn.setAttribute('aria-expanded', 'false');
          }
        });

        // Toggle current item
        item.classList.toggle('faq-item--open', !isOpen);
        question.setAttribute('aria-expanded', !isOpen);
      });
    }
  });

  /* ──────────────────────────────────────────────
     5. Smooth Scroll for Anchor Links
     ────────────────────────────────────────────── */
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;

      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        const headerHeight = header ? header.offsetHeight : 0;
        const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight - 16;

        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

  /* ──────────────────────────────────────────────
     6. Header Shrink on Scroll
     ────────────────────────────────────────────── */
  let lastScrollY = 0;
  const scrollThreshold = 50;

  function handleScroll() {
    const currentScrollY = window.pageYOffset;
    if (header) {
      if (currentScrollY > scrollThreshold) {
        header.classList.add('header--scrolled');
      } else {
        header.classList.remove('header--scrolled');
      }
    }
    lastScrollY = currentScrollY;
  }

  window.addEventListener('scroll', handleScroll, { passive: true });

  /* ──────────────────────────────────────────────
     7. Basic Form Validation
     ────────────────────────────────────────────── */
  const forms = document.querySelectorAll('.quote-form');
  forms.forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const name  = form.querySelector('input[name="name"]');
      const phone = form.querySelector('input[name="phone"]');
      const email = form.querySelector('input[name="email"]');

      let isValid = true;

      // Clear previous errors
      form.querySelectorAll('.quote-form__error').forEach(function (err) {
        err.remove();
      });
      form.querySelectorAll('.quote-form__input--error').forEach(function (inp) {
        inp.classList.remove('quote-form__input--error');
      });

      // Validate name
      if (name && !name.value.trim()) {
        showError(name, 'Please enter your name');
        isValid = false;
      }

      // Validate phone
      if (phone && !phone.value.trim()) {
        showError(phone, 'Please enter your phone number');
        isValid = false;
      } else if (phone && phone.value.trim().replace(/\D/g, '').length < 10) {
        showError(phone, 'Please enter a valid phone number');
        isValid = false;
      }

      // Validate email
      if (email && email.value.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
        showError(email, 'Please enter a valid email address');
        isValid = false;
      }

      if (isValid) {
        // Show success state
        const submitBtn = form.querySelector('.quote-form__submit');
        if (submitBtn) {
          const originalText = submitBtn.textContent;
          submitBtn.textContent = '✓ Quote Request Sent!';
          submitBtn.disabled = true;
          submitBtn.style.opacity = '0.7';

          setTimeout(function () {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
            submitBtn.style.opacity = '';
            form.reset();
            // Close modal if this was the modal form
            if (form.closest('.modal-content')) {
              closeQuoteModal();
            }
          }, 3000);
        }
      }
    });
  });

  function showError(input, message) {
    input.classList.add('quote-form__input--error');
    const error = document.createElement('div');
    error.className = 'quote-form__error';
    error.textContent = message;
    input.parentNode.appendChild(error);
  }

  /* ──────────────────────────────────────────────
     8. Phone Number Formatting
     ────────────────────────────────────────────── */
  document.querySelectorAll('input[name="phone"]').forEach(function (input) {
    input.addEventListener('input', function () {
      let value = this.value.replace(/\D/g, '');
      if (value.length > 10) value = value.slice(0, 10);
      if (value.length >= 6) {
        this.value = '(' + value.slice(0, 3) + ') ' + value.slice(3, 6) + '-' + value.slice(6);
      } else if (value.length >= 3) {
        this.value = '(' + value.slice(0, 3) + ') ' + value.slice(3);
      } else if (value.length > 0) {
        this.value = '(' + value;
      }
    });
  });

  /* ──────────────────────────────────────────────
     9. Intersection Observer for Scroll Animations
     ────────────────────────────────────────────── */
  if ('IntersectionObserver' in window) {
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-on-scroll--visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    animateElements.forEach(function (el) {
      observer.observe(el);
    });
  }

})();
