(() => {
  function measureWhatsAppClick(event) {
    if (event.defaultPrevented || typeof window.oaiq !== 'function') return;
    if (event.type === 'auxclick' && event.button !== 1) return;

    const link = event.target.closest?.('a[href]');
    if (!link || link.hasAttribute('download')) return;

    let url;
    try {
      url = new URL(link.getAttribute('href'), document.baseURI);
    } catch {
      return;
    }
    const isWhatsAppLink = url.protocol === 'https:' && (
      (url.hostname === 'wa.me' && /^\/\d+\/?$/.test(url.pathname)) ||
      (['api.whatsapp.com', 'web.whatsapp.com'].includes(url.hostname) &&
        /^\/send\/?$/.test(url.pathname) && url.searchParams.has('phone'))
    );
    const isWhatsAppAppLink = url.protocol === 'whatsapp:' && url.hostname === 'send' &&
      url.searchParams.has('phone');

    if (isWhatsAppLink || isWhatsAppAppLink) {
      window.oaiq('measure', 'custom', { type: 'custom' }, { custom_event_name: 'click2whatsapp' });
    }
  }

  document.addEventListener('click', measureWhatsAppClick);
  document.addEventListener('auxclick', measureWhatsAppClick);
})();
