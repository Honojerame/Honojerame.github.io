(() => {
  'use strict';
  document.documentElement.classList.add('js');

  const menuButton = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#site-navigation');
  const closeMenu = (restoreFocus = false) => {
    if (!menuButton || !navigation) return;
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.textContent = 'Menu +';
    navigation.classList.remove('is-open');
    if (restoreFocus) menuButton.focus();
  };

  if (menuButton && navigation) {
    menuButton.hidden = false;
    menuButton.addEventListener('click', () => {
      const open = menuButton.getAttribute('aria-expanded') !== 'true';
      menuButton.setAttribute('aria-expanded', String(open));
      menuButton.textContent = open ? 'Close −' : 'Menu +';
      navigation.classList.toggle('is-open', open);
    });
    navigation.addEventListener('click', (event) => {
      if (event.target.closest('a')) closeMenu();
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') closeMenu(true);
    });
    document.addEventListener('click', (event) => {
      if (!event.target.closest('.site-header')) closeMenu();
    });
    window.matchMedia('(min-width: 801px)').addEventListener('change', () => closeMenu());
  }

  const year = document.querySelector('[data-year]');
  if (year) year.textContent = String(new Date().getFullYear());

  // Play one brief current sweep as each card enters view, including on touch
  // screens. CSS also replays it on hover or keyboard focus without intercepting links.
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if ('IntersectionObserver' in window && !reducedMotion.matches) {
    const cardObserver = new window.IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        cardObserver.unobserve(entry.target);
        if (reducedMotion.matches) return;
        entry.target.classList.add('is-energized');
        window.setTimeout(() => entry.target.classList.remove('is-energized'), 3100);
      });
    }, { threshold: 0.25 });
    document.querySelectorAll('.project-card').forEach((card) => cardObserver.observe(card));
  }

  // Keep the existing Formspree endpoint and its native no-JavaScript POST.
  // A message is shown as sent only after an affirmative server response.
  const form = document.querySelector('#contact-form');
  if (form && window.fetch && window.AbortController) {
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const button = form.querySelector('button[type="submit"]');
      const status = document.querySelector('#form-status');
      if (button.disabled) return;
      button.disabled = true;
      button.textContent = 'Sending…';
      status.textContent = '';
      status.removeAttribute('data-state');
      form.setAttribute('aria-busy', 'true');
      const controller = new AbortController();
      const timeout = window.setTimeout(() => controller.abort(), 15000);
      try {
        const response = await fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: { Accept: 'application/json' },
          signal: controller.signal,
        });
        if (!response.ok) throw new Error('Message service did not accept the request.');
        status.textContent = 'Thanks for reaching out. Your message was sent successfully.';
        status.dataset.state = 'success';
        form.reset();
      } catch (error) {
        status.textContent = error.name === 'AbortError'
          ? 'The request timed out, so delivery could not be confirmed. Your message is still here. You can also email preciousonoj@gmail.com.'
          : 'Your message could not be sent. Please try again or email preciousonoj@gmail.com. Your message is still here.';
        status.dataset.state = 'error';
      } finally {
        window.clearTimeout(timeout);
        button.disabled = false;
        button.innerHTML = 'Send message <span class="arrow" aria-hidden="true">↗</span>';
        form.removeAttribute('aria-busy');
      }
    });
  }
})();
