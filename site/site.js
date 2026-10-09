// Inferra site: mobile menu, the diff highlighter, live status, first-party events.
(() => {
  const menu = document.querySelector(".menu-btn"), links = document.getElementById("nav-links");
  menu?.addEventListener("click", () => {
    const open = links.classList.toggle("open");
    menu.setAttribute("aria-expanded", String(open));
  });

  // The diff: focusing or hovering a line lights up what it creates.
  const env = document.getElementById("env");
  const light = (keys) => {
    env.classList.toggle("focusing", keys.length > 0);
    env.querySelectorAll("[data-k]").forEach((el) => el.classList.toggle("lit", keys.includes(el.dataset.k)));
  };
  document.querySelectorAll(".code .ln[data-lit]").forEach((ln) => {
    const keys = ln.dataset.lit.split(" ");
    const on = () => { document.querySelectorAll(".code .ln.on").forEach((x) => x.classList.remove("on")); ln.classList.add("on"); light(keys); };
    const off = () => { ln.classList.remove("on"); light([]); };
    ln.addEventListener("mouseenter", on); ln.addEventListener("focus", on);
    ln.addEventListener("mouseleave", off); ln.addEventListener("blur", off);
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
})();
