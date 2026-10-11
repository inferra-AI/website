// Inferra site: mobile menu, live status and optional Umami events.
(() => {
  document.documentElement.classList.add("js");
  const menu = document.querySelector(".menu-btn"), links = document.getElementById("nav-links");
  menu?.addEventListener("click", () => {
    const open = links.classList.toggle("open");
    menu.setAttribute("aria-expanded", String(open));
  });

  // Status dot: read the status page's summary; stay neutral if it can't be reached.
  const status = document.querySelector("[data-status]");
  if (status) {
    fetch("https://status.inferralab.com/api/summary.json", { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : Promise.reject()))
      .then((s) => {
        const down = (s.sites || s).filter?.((x) => x.status && x.status !== "up").length ?? 0;
        status.querySelector(".dot").className = "dot" + (down ? " warn" : "");
        status.lastElementChild.textContent = down ? "Some systems degraded" : "All systems operational";
      })
      .catch(() => {});
  }

  // Optional Umami analytics. Do Not Track disables both loading and events.
  const dnt = [navigator.doNotTrack, window.doNotTrack, navigator.msDoNotTrack]
    .some(value => value === "1" || value === "yes");
  const config = window.INFERRA_ANALYTICS || {};
  const enabled = !dnt && Boolean(config.src && config.websiteId);
  const track = (name, data) => {
    if (!enabled) return;
    try { window.umami?.track(name, data); } catch { /* Analytics must never break the site. */ }
  };
  window.inferraTrack = track;
  const heading = document.querySelector('[data-hero-heading]');
  const variant = new URLSearchParams(location.search).get('hero') === 'b' ? 'b' : 'a';
  if (heading && variant === 'b') heading.textContent = 'Just bring your code. We run it.';
  if (enabled) {
    const script = document.createElement('script');
    script.defer = true;
    script.src = config.src;
    script.dataset.websiteId = config.websiteId;
    script.dataset.doNotTrack = 'true';
    script.addEventListener('load', () => {
      if (heading) track('hero_variant', { variant });
    });
    document.head.appendChild(script);
  }
  // Umami handles annotated clicks itself. Do not also send the same click manually.

  // Hero picture: scale it to fit between its column start and the window edge.
  const scene = document.querySelector(".hero-scene");
  if (scene) {
    const fit = () => {
      if (innerWidth <= 900) { scene.style.removeProperty("--fit"); return; }
      const left = scene.getBoundingClientRect().left;
      const s = Math.min(1, (document.documentElement.clientWidth - left - 32) / 850);
      scene.style.setProperty("--fit", Math.max(0.5, s).toFixed(3));
    };
    fit();
    addEventListener("resize", fit);
  }
})();

// Setup request: copy only on an explicit user action.
document.querySelectorAll('[data-copy]').forEach((button) => {
  button.addEventListener('click', async () => {
    const target = document.getElementById(button.dataset.copy);
    if (!target) return;
    try {
      await navigator.clipboard.writeText(target.textContent);
      button.textContent = 'Copied';
    } catch {
      const range = document.createRange();
      range.selectNodeContents(target);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      button.textContent = 'Text selected — copy with your keyboard';
    }
  });
});
