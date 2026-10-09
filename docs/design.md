# Public website: inferralab.com

Live (preview, noindex) since 2026-10-09: https://inferralab.com on GitHub Pages
from this repo; status page https://status.inferralab.com (repo inferra-AI/status,
checks every 5 minutes from GitHub Actions); CLI downloads from public releases
of inferra-AI/cli. DNS in Route 53 (apex A/AAAA to GitHub Pages, www and status
CNAME to inferra-ai.github.io). To launch: remove every `PREVIEW:` marker
(banner, noindex, robots.txt), replace every `LAUNCH:` value (production API
host, demo commit, video).

Status: decided with the owner 2026-10-09. Built from two independent plans
(Fable, Codex) and two rounds of cross-review; the owner chose Fable's story and
look with Codex's operational rules, plus the corrections below. The round-1
design was rejected for: too many colours, defining Inferra by Vercel,
rudimentary "three steps / under five minutes" claims, no SEO, repetition, no
value proposition, no story.

## 0. Rules for every word on the site

1. **Only what is true on the released version.** Planned features say
   "coming soon" everywhere they appear, including headlines.
2. **"Commit", not "pull request".** A push to a mapped branch deploys; nothing
   forces a PR. Say "every change is a Git commit". Only the MCP server's
   configuration changes are PRs.
3. **No speed claims** ("in minutes", "three steps"). Show real output instead.
4. **Not defined by competitors.** Competitors appear only on dated /compare
   pages, never in the hero or pillars.
5. **Each fact lives in one section.** Every section below lists what it must not
   repeat.
6. Plain language; numbers exact (same rule as the dashboard).

## 1. Positioning

**Category:** a GitHub-native application platform for backends (APIs, workers,
containers) and their data.

**For:** 1–8 person teams and technical founders with an API, a worker and a
Postgres on GitHub, who already code with Claude, Codex, Cursor or VS Code.

**One sentence:** *Inferra turns your GitHub repo into your backend platform: one
file defines production, staging and previews, databases are reachable only by
the apps that declare them, and the bill is flat.*

**What is actually different (true today):**
- The repo is the control plane: `.inferra/org.yaml` + GitHub Environments; a
  push is the only way to deploy (no `inferra push`).
- A database or cache admits only the apps bound to it (network policy); buckets
  use pod identity, no keys handed out.
- gVisor sandbox around every app on every plan, Free included.
- Flat plans: limits stop the next push; they never add to the bill.
- Monorepos rebuild only changed apps and say so on the commit
  ("unchanged since 3f2a1c, still live").

**The AI angle, stated honestly:** other platforms (e.g. Render, Coolify) already
offer MCP servers. Inferra's difference is the permission model: the assistant
can **read** everything you can read, and can **change only `org.yaml`, only as
a pull request you merge**. It never deploys, restarts, deletes or sees a secret
value. Coming soon.

## 2. Plans (from `001_identity_tenancy.sql`; publish exactly these)

| | Free | Pro | Team |
|---|---|---|---|
| Price | $0, 7-day trial | $20/month | $99/month |
| Apps | 3 | 20 | 100 |
| CPU / memory (shared by all apps) | 1.5 / 1.5 GiB | 8 / 16 GiB | 32 / 64 GiB |
| Instances per app | 1 | 10 | 50 |
| Build minutes / month | 100 | 1,000 | 5,000 |
| Bandwidth / month | 10 GB | 100 GB | 1 TB |
| Log history | 1 day | 7 days | 30 days |

Free also caps each app at 0.5 CPU / 512 MiB (`030_free_trial.sql`). Idle sleep
is in the plan catalog but not implemented: never advertise it.
Trial: apps stop on day 7; data is deleted 7 days later unless you upgrade.
Database/cache/bucket availability per plan and seats: confirm from the service
catalog before publishing (open item).

**Network rules (same on every plan):** inbound only through Inferra's HTTPS
gateway (443) to your app's `$PORT`; apps in the same space reach each other;
outbound to any public port (external databases, SMTP, APIs); never private
network ranges or cloud metadata; Inferra-hosted Postgres and Redis reachable by
bound apps only.

## 3. Story and signature visual

- **Hook:** a 30-line `org.yaml` diff; beside it, the environment it creates.
- **Tension:** "You didn't choose this architecture. It accreted." Host, database
  vendor, cache, bucket, CI file, log tool, secrets spreadsheet, a bill you
  can't predict, and an assistant that sees nothing or everything.
- **Resolution:** one repo, one file, one bill. People push; CLI and dashboard
  show what happened; the assistant (coming soon) reads the same evidence.
- **Proof:** the live demo org, the status page, the video, real CLI output.
- **Action:** install the GitHub App; read /setup; download the CLI.

**Signature visual, "The diff is your infrastructure":** left, `org.yaml` as a
diff; right, prod / stage / preview lanes with apps, Postgres, cache, bucket.
Three states only at launch: (1) focus a changed path → only the apps it
rebuilds light up; (2) focus Postgres → lines draw to its bound apps, others show
a lock; (3) the commit status row: `✓ api deployed` /
`✓ worker unchanged since 3f2a1c, still live`. Built as inline SVG + a static
table ("What you wrote / What Inferra created / Who can reach it"); keyboard
focus per hunk; `prefers-reduced-motion` disables motion; dimensions reserved.
Data comes from the demo org. No image digests or internal terms on screen.

## 4. Homepage (8 sections)

| # | Section | Job | Must not repeat |
|---|---|---|---|
| 1 | Hero | Say what it is; two CTAs; "Watch the demo" link; status dot | Prices, feature lists |
| 2 | It accreted | The problem | Feature inventory |
| 3 | The diff | Make the model obvious (signature visual) | GitHub-flow prose |
| 4 | Four ways in | GitHub App / CLI / dashboard / MCP (coming soon), each one's job and limits | Security copy |
| 5 | Data belongs with the app | Postgres, Valkey, buckets; binding rule; versions; backups | Isolation copy |
| 6 | Watch us run it | Video, demo-org links, logs/metrics/exec/rollback, status | Metric lists elsewhere |
| 7 | Built to run other people's code | gVisor, per-space network, pinned buildpacks | — |
| 8 | Plans and start | Plan table, network rules, trial terms, CTAs | — |

Nav: Docs · Setup · Download · Pricing · Demo · Status · Sign in.
Footer: MCP · Security · Compare · Changelog · llms.txt · Privacy.

### Copy (final draft)

1. **Hero.** Eyebrow *GitHub-native application platform.* H1 *Your GitHub repo
   is your backend platform.* Sub *Commit one file, keep values in GitHub
   Environments, push. Inferra builds, deploys and reports back on the commit:
   APIs, workers and Postgres, sandboxed, for a flat monthly price.* CTAs
   *Install the GitHub App* · *Read the setup guide*. Link *Watch the
   2½-minute demo*.
2. **It accreted.** H2 *You didn't choose this architecture. It accreted.* *A host
   here, a database there, a cache, a bucket, a workflow file, a log tool, a
   secrets spreadsheet, and a bill you can't predict. Inferra is one repo, one
   file, one bill.*
3. **The diff.** H2 *The diff is your infrastructure.* *`main` deploys to prod.
   Every other branch gets its own preview copy, removed with the branch. A
   database declared next to an app appears beside it, its address already in
   the app's environment, reachable by that app and nothing else.*
4. **Four ways in.** H2 *Four ways in. Every change is a Git commit.* GitHub App:
   *a push builds and deploys; the commit shows the result.* CLI: *logs with
   history, metrics, a shell in a running instance, rollback, promote. It
   operates; it never deploys.* Dashboard: *org, space, app, the same facts at a
   glance.* MCP server, coming soon: *connect Claude, Codex, VS Code or Cursor
   and choose the orgs it may see. It reads logs, builds, crashes and metrics and
   explains what's wrong. If the fix is configuration, it opens a pull request
   to `org.yaml`; you merge. It never deploys, restarts, deletes or sees a secret
   value.* CTA *Join MCP early access*.
5. **Data.** H2 *A database only its apps can reach.* Postgres (choose the major
   version in `org.yaml`), Valkey cache, S3 buckets; `ORDERS_URL` /
   `FILES_BUCKET` injected; network policy admits only bound apps; *if you
   delete a database, support can restore it within 7 days* (verify on dev).
6. **Watch us run it.** H2 *We run a real org in public. Look at it.* Video
   (poster, click to play, captions, transcript below); links to the demo repo,
   its live URL, its read-only dashboard, the status page.
7. **Trust.** H2 *Built to run other people's code.* *Every app runs in a gVisor
   sandbox on every plan, Free included. Each space is its own network: closed
   by default, no reach into private ranges or cloud metadata. Buildpacks come
   from a mirrored catalog pinned by digest.*
8. **Plans.** H2 *Flat plans. Limits stop the next push; they never add to the
   bill.* Plan table from §2, network rules, trial terms. CTAs *Install the
   GitHub App* · *Download the CLI* · *Setup guide*.

## 5. Proof without customers

- **Status page** at `status.inferralab.com`: **Upptime** (open source, runs on
  GitHub Actions + GitHub Pages: free, and monitored from outside our cloud, so
  it stays up when we're down). Components: API, GitHub webhook intake, builds,
  deploys (a real probe deploy), dashboard, demo app. No invented history: it
  shows real uptime from the day it starts. Incidents posted as GitHub issues.
- **Live demo org**: `github.com/inferra-AI/inferra-demo` (public; already
  pushed; Inferra App to be installed on camera). `api` + `worker`, Postgres
  added on camera. `/demo` page links the repo, its commit statuses, the live
  URL and a **read-only public dashboard view** (to build: no sign-in, one org,
  secrets as names only, logs sanitised, no actions). Demo is on an operator
  account. Reset runbook; a scheduled commit keeps statuses fresh; an external
  check alerts when any proof link breaks.
- **Video** (recorded on the demo org after rc.17, with the final UI):
  full cut 2:30 (cap 3:00) and a 30–45 s cut. Real clock: waits shown as a timer
  or a labelled cut ("1m 40s later"). Chapters: install App → commit `org.yaml`
  → push → status green → open URL → add Postgres (only `api` rebuilds, `worker`
  "unchanged, still live"; the page shows `database: connected`) → break the
  health check, read `inferra logs`, `inferra rollback` → dashboard + status.
  The MCP chapter is recorded only once MCP works. Captions (WebVTT), HTML
  transcript with copyable commands, VideoObject with a Clip per chapter.
  Re-record when a shown screen, CLI output or `org.yaml` syntax changes; the
  page caption says "Recorded with Inferra vX".

## 6. Journeys

- **/setup** (one canonical guide, printable): prerequisites (GitHub **admin** on
  the repo; a non-admin must ask an admin to install the App: say so, with a
  copyable request message) → install the App → install the CLI and `inferra
  login` → `inferra init` → spaces and branches → GitHub Environments (secret
  values never reach Inferra unless you use the optional workflow or set them
  in Inferra) → commit and push → read the status, open the URL, `inferra logs`
  → add Postgres → next steps (previews, promote, rollback, billing, restore,
  uninstall). Troubleshooting per failure message.
- **/download**: generated from the release manifest (cannot drift): version,
  date, changelog link; one row per artifact actually built, with SHA-256;
  manual download + checksum first, then `curl -fsSL https://inferralab.com/install.sh | sh`
  with the script shown in full; `INFERRA_VERSION` pinning; update and
  uninstall. Signatures only if the pipeline signs (otherwise say so). Header
  line: *Git pushes create deployments; the CLI inspects and operates them.*
- **/mcp** (coming soon): connection targets; a tool table (what each reads, its
  scope, audit record, whether it can open a PR); auth, org selection, revoke;
  early-access form.

## 7. Measurement

First-party, cookieless analytics (self-hosted Umami or Plausible), no ad
pixels, no session replay, nothing from logs/env/secrets. Funnel:
`landing_visit` → `install_app_click` → `github_app_installed` (server) →
`org_yaml_committed` (server; valid and invalid counted separately) →
`first_deploy_succeeded` (server; **activation**) →
`second_deploy_within_7d` (server; must come from a different, user-initiated
commit) → `plan_upgraded` (Stripe webhook). Also: download clicks by OS,
/setup step views, zero-result docs searches, MCP early-access submits (counted
when saved server-side), trial emails sent/delivered/clicked/upgraded (SPF/DKIM
set up first), week-4 and week-8 retention. Staff and demo accounts excluded.
Weekly review; baseline over the first 20 installs before setting targets.

## 8. SEO and AI-assistant visibility

- Title *Inferra: GitHub-native platform for APIs, workers and Postgres*;
  meta *Deploy APIs, workers and containers from your GitHub repo, with managed
  Postgres, cache, buckets, previews and logs, on flat monthly plans.*
- Static HTML; hero text and the visual's table in the HTML; inline SVG; no
  autoplay; self-hosted fonts; sitemap, canonicals; robots allow GPTBot,
  ClaudeBot, PerplexityBot, Google-Extended; `/llms.txt`; a one-paragraph
  factual definition at the top of every page; schema: Organization,
  SoftwareApplication + Offers, BreadcrumbList, VideoObject, HowTo on /setup
  (for understanding, not rich results).
- Pages in order: /setup, /download, /demo, /pricing, /docs, /security, /mcp,
  /changelog; then dated /compare/* and /alternatives/*, then /use-cases/*
  (python worker + postgres, node api + worker, monorepo, preview environments),
  and a Procfile → `org.yaml` migration guide.
- **Launch blocker:** public docs must match the code (branch
  docs-launch-truth: architecture.md §13, gVisor wording, network rules).

## 9. Look

One accent. Ink `#14213D`; accent Cobalt `#2456F0`; background `#FAFAF7`;
lines `#ECEBE6`; muted text `#5F6570`; body text `#1A1A1A`. Green / amber / red
only on status dots. Type: Instrument Serif for H1/H2, Inter for text,
JetBrains Mono for code (all self-hosted); sizes 56/60, 36/42, 22/30, 17/28,
13/18. Bordered panels (1px, 8px radius, no shadow) only for the diff, the four
ways in, and plans; tables for comparisons and network rules; no nested cards,
no gradient blobs, no stock images. Imagery: real product only (demo-org
dashboard crops, real CLI output, the diff). Dark mode follows the system.

## 10. Before launch (gates)

1. Docs match the code (docs-launch-truth merged).
2. The generated env workflow no longer trips GitHub's "may be malicious" check
   (verified 2026-10-09: sending only named secrets with the Action pinned by
   SHA runs without a hold; branch env-workflow-selected). `api.inferralab.com`
   (the Action's default API address) must resolve.
3. /setup and /download live; CLI downloadable with checksums.
4. Demo org live with the read-only dashboard view; status page running.
5. Video recorded on the release that is live.
6. Restore window, backup wording and preview naming verified on dev.
7. Custom domains: not built. The site says so on /pricing and /docs
   ("coming soon: your own domain"); production migrations are not courted
   until they ship.
8. Competitor pricing table: published only when every figure is read from the
   vendor's page on the stated date; until then /compare pages describe billing
   models, not totals.
