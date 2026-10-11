# W2 page review

Reviewed against `site/index.html`, `site/pricing/index.html`, `site/mcp/index.html`, and the pages under `site/docs/` and `site/compare/`. The local product reference `site/llms-full.txt` also confirms Wallet → Redeem code. No network writes, commits, pushes, or sub-agents were used.

## Shared shell and language

All four headers and footers already matched the v5 homepage exactly; preserved them. Added the missing `tpl.css`, retained `v5.css`, `v5.js`, page-specific metadata and `noindex, nofollow`. Load the page-specific wrapping rules after the shared styles. Replaced dense rate abbreviations with monthly prices for one virtual CPU and each GB, explained that smaller sizes cost less, and linked to pricing. No sitemap or navigation files were changed.

The “unlisted” description differs from the existing homepage: its shared navigation and footer already link to `/ai/` and `/templates/`, and its body links to `/ai/`. Those existing links were preserved to meet the matching-shell requirement. Owner decision: whether to remove those links site-wide in a separate change.

## `/ai/`

- Wrong: internal terms such as service bindings, branch quotas and selected-secret workflow obscured the instructions. A hardcoded development outbound IP could become stale. The tool count added an unnecessary maintenance dependency.
- Changed: explained branch limits, connected services and the files' purposes; linked to secret setup and the current outbound IP guidance. Kept precise configuration names in technical examples. Clarified GitHub source builds with buildpacks, fixed running copies, independent preview databases, managed Postgres backups, memory-only Valkey and private object storage. Preserved read-only MCP inspection, failure explanations and proposed diffs, with repository edits separate from MCP access.
- Owner decisions: none specific to this page. No custom domains, multi-region, certification, autoscaling or AWS-managed database availability promises were added.

## `/start/`

- Wrong: the primary flow treated offer redemption as a required onboarding step. Dense billing text repeated the allowance. The shared W2 script could promise credits merely because a code appeared in an analytics allowlist.
- Changed: made deployment and the $5 monthly allowance the main flow; moved optional code redemption to its own paragraph. Added source-build and available-service context. In `site/w2.js`, changed the campaign message to “Check it in your wallet”; eligibility and amount remain subject to wallet confirmation.
- Owner decisions: confirm campaign terms before publishing any specific credit amount. No campaign amount is promised here.

## `/templates/`

- Wrong: three GitHub template repositories were presented as available without corroboration elsewhere on the reviewed site. “Deploy to Inferra” buttons actually opened GitHub's repository creation flow. Badge snippets repeated those unverified targets.
- Changed: replaced the template catalog with starter setup guidance for Next.js + Postgres, FastAPI + worker, and AI chat. Removed the unverified repository links and badges. Linked to existing configuration, migration, secret and external API guides. Explained the source/buildpack deployment flow and preview costs. Kept existing section IDs and the page URL.
- Owner decisions: restore actual template creation links only after confirming the repositories are public, usable, and contain working deployment configuration. The title now says “Starter setups”; the unchanged shared shell still labels the route “Templates.”

## `/agencies/`

- Wrong: an otherwise undocumented partner program and partner mailbox were advertised. Org/namespace/quota language was unnecessarily technical. Preview instructions omitted branch configuration guidance.
- Changed: replaced the partner program pitch with the existing contact page. Explained projects, fresh preview data, separate branch costs and shared account credits. Added branch-file and billing reference links. Kept the documented repository access and account ownership rules.
- Owner decisions: confirm a partner program and its contact address before restoring the removed claim. Separate client wallets still require separate owning accounts; this page promises no per-project billing.

## Verification

Run the included offline script:

```sh
python3 scripts/check-w2-links.py
```

Output:

```text
ai: 56 local href/src references checked; noindex and v5 shell OK
start: 49 local href/src references checked; noindex and v5 shell OK
templates: 54 local href/src references checked; noindex and v5 shell OK
agencies: 50 local href/src references checked; noindex and v5 shell OK
Broken local references: 0
```

The script checks every local href and src, requires targets to be files within `site/`, checks HTML fragment IDs, compares header/footer blocks exactly with the homepage, and checks noindex and shared CSS/JS. External and mail links are excluded. `git diff --check` also passes.

Mobile CSS inspection at 390px: the existing `.wrap` becomes 350px wide; document text wraps anywhere; code blocks have a maximum width of 100% and wrap long lines via `w2.css`; button groups wrap; the shared menu stacks and footer uses two columns. The revised pages have no tables or fixed-width grids. No new CSS was needed. A Chromium check was attempted using local assets with external requests blocked, but the environment prevented browser launch (`sandbox_host_linux.cc: Operation not permitted`). Rendered scroll widths and screenshots could not be verified; the owner should confirm all four pages at 390px with the menu closed and open before publication.

Source discrepancy outside scope: some reference pages say “No plans,” while the task confirms free and paid plans exist. These pages describe the confirmed free allowance and prepaid credits without repeating the contradictory “No plans” claim.
