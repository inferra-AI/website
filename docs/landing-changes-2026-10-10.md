# Landing page changes

Updated 2026-10-10.

## Customer journey and video

- Replaced the hero's illustrated dashboard with the real demo app overview.
- Added a five-step journey immediately after the hero: connect the GitHub App, add `.inferra/org.yaml` and `.inferra/<branch>.yaml`, push and go live, watch metrics and logs, and roll back.
- Steps use horizontal arrows on desktop and stack with downward arrows on mobile. Screenshots link to full-size images, have descriptive alt text and explicit dimensions, and load lazily in the journey.
- Setup captions explain that organization and namespace screenshots show the resulting dashboard, rather than the GitHub installation or file editor.
- Embedded `/demo/inferra-demo.mp4` with controls, playsinline, metadata preload and the app overview poster. No autoplay.

## Real screenshots

Captured the anonymous, read-only demo at `https://api.dev.inferralab.dev/demo` using headless Chromium, 1440 × 900, light mode, without browser chrome. External browser requests were restricted to GETs to the demo host; no actions that change platform state were taken.

The first release poll succeeded: HTML referenced `/assets/app.v1.js?v=17808f9b44bf&demo=1`, and that served script contained `helpMenu`. No 15-minute fallback was needed. This records the requested readiness signal, rather than claiming a release number not exposed by the page.

Optimized WebP assets in `site/assets/journey/`:

| Capture | File | Bytes |
| --- | --- | ---: |
| Organization overview | organization.webp | 16,012 |
| Namespace with apps | namespace.webp | 15,654 |
| App overview | app.webp | 30,764 |
| App metrics | metrics.webp | 33,438 |
| Logs | logs.webp | 22,876 |
| Deployments | deployments.webp | 18,834 |

Waited for loaded views and charts. CPU and memory axis labels were visually checked and do not overlap. The captured range has no request traffic; the corresponding panels truthfully show no requests. Logs contain a redacted platform startup message. Screens were reviewed for personal data; only public demo organization/app identifiers, commits, runtime statistics and platform messages appear.

Authentic dashboard screenshots retain the product's current “Spaces” sidebar label. Website prose uses “namespace.” Deployment actions are unavailable in the read-only demo; the caption explains this instead of presenting a clickable rollback control in the capture.

## Value proposition and wording

- Hero promise focuses on bringing code without maintaining servers, clusters or Dockerfiles.
- Added eight compact pastel cards covering source builds, branch preview namespaces, managed Postgres with backups and restore to any point in 7 days, cache and S3 buckets, custom Docker-image services, public internet connections, app isolation and private branch networks, prepaid reservations and the monthly $5 allowance, and assistants through MCP.
- Explain namespace as a separate running copy, instances as running app copies, CPU as computing power, and MCP as an assistant connection.
- Added external-services and own-database/queue FAQs. State that outbound IPs are fixed, shared by all platform apps and listed in docs/dashboard; credentials belong in secrets; private connections to customers' clouds are coming later.
- Custom-image services explicitly have no backups; recommend managed Postgres when backups are needed.
- Updated `llms.txt` and rebuilt FAQ JSON-LD from the visible answers. Organization and software descriptions match the new hero promise. Actual MCP tool identifiers, including `list_spaces`, remain unchanged.

## Repetition removed

- Removed the five-item facts strip: repeated free allowance, managed data, isolation and prepaid-credit claims.
- Removed the “You / Inferra” split and associated why cards: repeated setup flow, servers/builds, previews, data and isolation.
- Removed the two-file configuration illustration/table section and its repeated preview examples; the journey links to the existing setup guide for complete file examples.
- Removed the illustrated Git-deployment step section; the real screenshot journey now explains the flow.
- Removed the illustrative feature bento: repeated branch previews, data, isolation, observation, deployment history and assistant claims now live in the journey/value grid.
- Removed repetitive general, comparison, deployment, pricing and isolation FAQ answers. Retained specific language/worker questions and added operational questions that expand on the grid.
- Removed the three pricing fact cards and repeated monthly allowance in the hero and final CTA. Retained the reservation calculators and a billing-doc link; differentiated their supporting notes.
- Replaced the final two setup/assistant cards with a short repository/setup CTA.
- Removed the stale demo-video placeholder comment.

## Validation

- Chromium at 375px and 1440px: document width equals viewport width, with no overflowing main-content elements.
- Scrolled each image into view and awaited decoding: all seven homepage image elements load successfully; six unique screenshot files are under 250 KB.
- Video source loads and metadata is available.
- Homepage internal page, asset and fragment links resolve; all IDs are unique.
- Both JSON-LD blocks parse; FAQ questions and answers exactly match visible FAQ text.
- No browser console errors or page exceptions. External status requests were stubbed locally during validation to avoid sending requests outside the authorized demo host.
- Reservation calculator regression checks pass, including independent calculators, input/range synchronization, free allowance and responsive layout.
- `git diff --check` passes. No commits made.
