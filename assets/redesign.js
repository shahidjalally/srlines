(() => {
  const desktopGroups = [...document.querySelectorAll('.nav-group')];
  desktopGroups.forEach((group) => {
    const button = group.querySelector('button');
    const setOpen = (open) => {
      desktopGroups.forEach((other) => {
        if (other !== group) {
          other.classList.remove('open');
          other.querySelector('button').setAttribute('aria-expanded', 'false');
        }
      });
      group.classList.toggle('open', open);
      button.setAttribute('aria-expanded', String(open));
    };
    button.addEventListener('click', () => setOpen(!group.classList.contains('open')));
  });

  const toggle = document.querySelector('.menu-toggle');
  const drawer = document.querySelector('.mobile-drawer');
  const closeButton = document.querySelector('.drawer-close');
  const backdrop = document.querySelector('.drawer-backdrop');
  let returnFocus;
  const focusable = () => [...drawer.querySelectorAll('a,button,summary')].filter((item) => !item.hidden);
  const setDrawer = (open) => {
    if (open) returnFocus = document.activeElement;
    drawer.classList.toggle('open', open);
    drawer.setAttribute('aria-hidden', String(!open));
    toggle.setAttribute('aria-expanded', String(open));
    backdrop.hidden = !open;
    document.body.classList.toggle('drawer-open', open);
    if (open) closeButton.focus(); else returnFocus?.focus();
  };
  toggle?.addEventListener('click', () => setDrawer(true));
  closeButton?.addEventListener('click', () => setDrawer(false));
  backdrop?.addEventListener('click', () => setDrawer(false));
  drawer?.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => setDrawer(false)));

  document.addEventListener('click', (event) => {
    if (!event.target.closest('.nav-group')) desktopGroups.forEach((group) => {
      group.classList.remove('open');
      group.querySelector('button').setAttribute('aria-expanded', 'false');
    });
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      desktopGroups.forEach((group) => {
        group.classList.remove('open');
        group.querySelector('button').setAttribute('aria-expanded', 'false');
      });
      if (drawer?.classList.contains('open')) setDrawer(false);
    }
    if (event.key === 'Tab' && drawer?.classList.contains('open')) {
      const items = focusable();
      if (event.shiftKey && document.activeElement === items[0]) { event.preventDefault(); items.at(-1).focus(); }
      else if (!event.shiftKey && document.activeElement === items.at(-1)) { event.preventDefault(); items[0].focus(); }
    }
  });
  window.addEventListener('resize', () => { if (innerWidth >= 900 && drawer?.classList.contains('open')) setDrawer(false); });

  const current = location.pathname === '/' ? '/' : location.pathname;
  document.querySelectorAll('header a, .mobile-drawer a').forEach((link) => {
    if (link.getAttribute('href') === current) { link.classList.add('active'); link.setAttribute('aria-current', 'page'); }
  });

  document.querySelectorAll('[data-filter]').forEach((button) => button.addEventListener('click', () => {
    document.querySelectorAll('[data-filter]').forEach((item) => item.classList.toggle('active', item === button));
    document.querySelectorAll('[data-category]').forEach((card) => { card.hidden = button.dataset.filter !== 'all' && card.dataset.category !== button.dataset.filter; });
  }));

  const form = document.querySelector('#contact-form');
  form?.addEventListener('submit', (event) => {
    const invalid = [...form.elements].find((field) => field.willValidate && !field.validity.valid);
    if (invalid) {
      event.preventDefault();
      const status = form.querySelector('.form-status');
      if (status) status.textContent = 'Please complete the required fields and enter a valid email address.';
      invalid.setAttribute('aria-invalid', 'true');
      invalid.focus();
    }
  }, true);
})();
