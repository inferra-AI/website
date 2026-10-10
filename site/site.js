// Inferra site: mobile menu, live status, first-party events.
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

  // First-party events (no cookies, no third parties). Sent only if an endpoint is configured.
  const endpoint = document.querySelector('meta[name="events-endpoint"]')?.content;
  const send = (name, props = {}) => {
    if (!endpoint) return;
    const body = JSON.stringify({ name, path: location.pathname, ref: document.referrer ? new URL(document.referrer).host : "", ...props });
    navigator.sendBeacon?.(endpoint, body);
  };
  send("landing_visit");
  document.addEventListener("click", (e) => {
    const el = e.target.closest("[data-event]");
    if (el) send(el.dataset.event, { href: el.getAttribute("href") });
  });

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
