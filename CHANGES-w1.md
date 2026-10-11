# W1: homepage and shared website updates

Implemented in `site/`; no commits or publishing actions performed.

- AI-first hero: “Your AI wrote the app. Inferra runs it.” Alternative “Just bring your code. We run it.” selected by `?hero=b`. Required subline, Get started CTA and new-tab, no-sign-up dashboard CTA.
- Assistant strip with text badges, copyable deployment prompt and `/ai/` link. Trust panels cover live uptime, managed Postgres backups and 7-day restore, isolation and prepaid billing. Linked the live demo app. No deploy-time claim was added without a measurement; the customer-quote placeholder is an HTML comment.
- Moved both reservation calculators to `/pricing/`. Added all four resource prices, prepaid billing, card requirement, monthly account free usage, service explanations and FAQPage structured data. Homepage retains a pricing teaser.
- Added empty Umami configuration in `site/analytics-config.js`. Every existing site page loads it before `site.js`. The loader inserts the configured deferred script with `data-website-id`; empty configuration or Do Not Track disables analytics. Annotated signup, demo and copy-deploy actions; calculator interaction sends one event after a 600 ms debounce, with calculator name only. Hero event includes `variant: a|b`. Umami handles UTM attribution; this site does not store it separately. Removed the old event endpoint implementation.
- Updated privacy explanation, shared navigation/footer links, titles/descriptions, canonicals, Open Graph and Twitter metadata, SoftwareApplication offers and subpage breadcrumbs. Offers describe $0 for the first $5 of monthly account usage; the request’s `/bin/bash` fragment was treated as malformed price text, consistent with the explicit free-tier rule.
- Sitemap includes all current pages plus the migration, comparison, template, assistant, agency, start and pricing destinations requested for the other job. Robots references the sitemap. Existing preview noindex / Disallow settings remain in place.
- Revised legacy prose to use namespace and reservation/usage wording; technical command identifiers, external source URLs and compatibility environment variable names remain intact.

## Validation

- Headless Chromium checked every existing `site/*.html` page at 375 px and 1440 px: no horizontal overflow, duplicate IDs, malformed JSON-LD or browser script errors. All existing internal destinations and fragments resolve.
- Four linked destinations are not present in this checkout: `/ai/`, `/templates/`, `/migrate/heroku/`, `/agencies/`. These are explicitly assigned to the other job. The other requested future sitemap URLs are also listed ahead of that job’s output. Recheck once those pages arrive; their metadata and analytics includes must follow the shared pattern.
- Mock Umami script verified hero B attribution, copy-deploy click event, calculator debounce and Do Not Track suppression. Empty configuration makes no analytics script request. Account calculator at 2 vCPU, 1 GB memory and 10 GB storage returns $35.20 before monthly free usage.
- Initial resource transfer measured about 635–711 KB for home and 129–154 KB for pricing, depending on viewport and font loading. Screenshots load lazily; video uses metadata preload. Desktop homepage visually reviewed.
- `git diff --check` passes.

## Configuration and release notes

Fill both analytics configuration placeholders to enable reporting. No analytics service credentials or IDs were invented. Production canonicals use `https://inferralab.com/`; application links retain the supplied development host.

The existing GitHub Pages workflow publishes the separate `public/` pre-launch page. This task updates the full `site/` website; it does not switch deployment sources or publish the full site.
