(() => {
  const config = window.INFERRA_ANALYTICS;
  let offer = null;
  let viewedCode = null;
  if (location.pathname.replace(/\/$/, '') === '/start') {
    const candidate = new URLSearchParams(location.search).get('offer') || '';
    // Only explicitly registered campaign codes get the offer message.
    viewedCode = /^[A-Za-z0-9_-]{1,64}$/.test(candidate) ? candidate : null;
    const codes = Array.isArray(config?.offerCodes) ? config.offerCodes : [];
    if (/^[A-Za-z0-9_-]{1,64}$/.test(candidate) && codes.includes(candidate)) {
      offer = candidate;
      document.getElementById('offer-message').textContent = `Have code ${offer}? Ask us about eligibility.`;
      document.getElementById('offer-note').textContent = 'Email support@inferralab.com with the code to check eligibility and terms before signing up.';
    }
  }
  const trackOffer = () => {
    if (location.pathname.replace(/\/$/, '') === '/start') {
      try { window.umami?.track('offer_viewed', {code: viewedCode || 'none'}); } catch {}
    }
  };
  if (config?.src && config?.websiteId) {
    const script = document.createElement('script');
    script.defer = true;
    script.src = config.src;
    script.setAttribute('data-website-id', config.websiteId);
    script.addEventListener('load', trackOffer, {once:true});
    document.head.append(script);
  } else { trackOffer(); }
})();
