# W2 new pages

- `/compare/heroku/` — `site/compare/heroku/index.html`
- `/compare/render/` — `site/compare/render/index.html`
- `/compare/railway/` — `site/compare/railway/index.html`
- `/compare/vercel/` — `site/compare/vercel/index.html`
- `/compare/fly/` — `site/compare/fly/index.html`
- `/migrate/heroku/` — `site/migrate/heroku/index.html`
- `/migrate/render/` — `site/migrate/render/index.html`
- `/migrate/railway/` — `site/migrate/railway/index.html`
- `/migrate/vercel/` — `site/migrate/vercel/index.html`
- `/templates/` — `site/templates/index.html`
- `/ai/` — `site/ai/index.html`
- `/agencies/` — `site/agencies/index.html`
- `/start/` — `site/start/index.html`

## Supporting files

- `site/llms-full.txt`: full assistant reference derived from docs.
- `site/assets/deploy-to-inferra.svg`: README deployment badge.
- `site/w2.css`, `site/w2.js`: new-page layout and campaign/analytics loader.
- `site/analytics-config.js`: empty Umami placeholders, created only if absent.

## Entries for the navigation/sitemap owner

Add Templates (`/templates/`), Deploy with AI (`/ai/`), Agencies (`/agencies/`) to developer/product resources. Link migration guides from the comparison hub; link focused comparisons from `/compare/`. Campaign entry `/start/` is suitable for campaign links. Add every page listed above to the sitemap on launch and `/llms-full.txt` to assistant resources; retain the copied preview noindex tags until launch. `/pricing/` is an explicit W2 dependency: the other job must supply that page (it is absent in this checkout). Existing shared nav/footer retain their copied pricing anchor.

## Campaign codes

No valid codes or validation endpoint were supplied. `window.INFERRA_ANALYTICS.offerCodes` may be an optional array of registered campaign codes (for example, add the real codes alongside src and websiteId in analytics-config.js). Only registered codes show the offer wording; missing, malformed and unknown codes show the normal free allowance. Redemption and eligibility remain wallet operations. No codes or amounts are invented. `offer_viewed` records the supplied code when it has a valid format (including unknown codes), or `none` when missing or malformed, after configured Umami loads.

## Scope

Existing homepage, sitemap, llms.txt, site.js and existing page nav/footer are untouched. No commits made.

## Validation

- All 13 pages: unique IDs, valid BreadcrumbList JSON-LD, unique titles/descriptions/canonical and Open Graph tags.
- Internal link and fragment checks pass except `/pricing/`, pending the other job.
- Headless Chromium: all 13 pages at 375px and 1440px with no horizontal overflow or console errors; mobile menu toggles correctly. External status responses were stubbed for repeatable browser checks.
- Empty Umami placeholders load no analytics script. Configured analytics loads and records `offer_viewed` once for registered, unknown, missing and malformed codes. Registered codes display the offer; the others display the free allowance.
- New HTML is about 143 KB total (about 11 KB per page); no new large media or framework dependencies. The assistant reference is plain text, and the badge is SVG.
