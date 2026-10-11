// v5: live status history, footer status dot, pricing calculator tabs.
(() => {
  const FEED = "https://status.inferralab.com/data.json";
  const DAYS = 90;
  const card = document.querySelector("[data-status-card]");
  const dots = document.querySelectorAll("[data-status-dot]");

  const isoDay = (d) => d.toISOString().slice(0, 10);
  const fmtDay = (iso) => new Date(iso + "T00:00:00Z").toLocaleDateString("en-GB", { day: "numeric", month: "short", timeZone: "UTC" });

  const render = (data) => {
    const comps = Object.values(data.components || {});
    // Results older than 20 minutes aren't current: show them as unknown, never green.
    const ageMin = data.updated ? Math.round((Date.now() - new Date(data.updated)) / 60000) : Infinity;
    const stale = ageMin > 20;
    const allUp = comps.length > 0 && comps.every((c) => c.status === "up");
    if (!stale) dots.forEach((d) => d.classList.add(allUp ? "vup" : "vwarn"));
    if (!card) return;
    const rows = card.querySelector("[data-rows]");
    const today = new Date();
    rows.innerHTML = "";
    let since = null;
    for (const c of comps) {
      const days = c.days || {};
      const row = document.createElement("div");
      row.className = "srow";
      const name = document.createElement("div");
      name.className = "name";
      name.textContent = c.name;
      const state = document.createElement("span");
      state.className = "state " + (stale ? "" : c.status === "up" ? "vup" : c.status ? "vdown" : "");
      state.textContent = stale ? "Checks delayed" : c.status === "up" ? "Up" : c.status ? "Down" : "Unknown";
      name.append(state);
      const bars = document.createElement("div");
      bars.className = "bars";
      bars.setAttribute("role", "img");
      let checks = 0, passed = 0;
      for (let i = DAYS - 1; i >= 0; i--) {
        const d = new Date(today); d.setUTCDate(d.getUTCDate() - i);
        const key = isoDay(d), v = days[key];
        const bar = document.createElement("i");
        if (v) {
          const [n, ok] = v; checks += n; passed += ok;
          bar.className = ok === n ? "vok" : ok === 0 ? "vbad" : "vpart";
          bar.title = `${fmtDay(key)}: ${ok} of ${n} checks passed`;
        } else bar.title = `${fmtDay(key)}: no data`;
        bars.append(bar);
      }
      if (c.since && (!since || c.since < since)) since = c.since;
      const count = document.createElement("div");
      count.className = "count";
      const from = c.since ? fmtDay(c.since.slice(0, 10)) : "";
      count.textContent = checks ? `${passed} of ${checks} checks passed${from ? " since " + from : ""}` : "No checks yet";
      bars.setAttribute("aria-label", `${c.name}: ${count.textContent}`);
      row.append(name, bars, count);
      rows.append(row);
    }
    const upd = card.querySelector("[data-updated]");
    if (upd && data.updated) upd.textContent = "Updated " + new Date(data.updated).toLocaleString("en-GB", { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit", timeZone: "UTC" }) + " UTC";
    const sinceEl = document.querySelector("[data-since]");
    if (sinceEl && since) sinceEl.textContent = "History since " + fmtDay(since.slice(0, 10)) + ".";
  };

  if (card || dots.length) {
    fetch(FEED, { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : Promise.reject()))
      .then(render)
      .catch(() => {
        if (!card) return;
        card.querySelector("[data-rows]").innerHTML =
          '<p>Live status unavailable. <a href="https://status.inferralab.com">Open the status page →</a></p>';
      });
  }

  // Pricing page: one calculator, two tabs.
  document.querySelectorAll("[data-tabs]").forEach((tabs) => {
    const buttons = [...tabs.querySelectorAll("button")];
    const panels = buttons.map((b) => document.getElementById(b.getAttribute("aria-controls")));
    const show = (i) => buttons.forEach((b, j) => { b.setAttribute("aria-selected", String(i === j)); panels[j].hidden = i !== j; });
    buttons.forEach((b, i) => b.addEventListener("click", () => show(i)));
    show(0);
  });
})();
