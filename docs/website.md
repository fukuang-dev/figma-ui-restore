# Website / 官网维护

Public site: [Figma UI Restore](https://fukuang-dev.github.io/figma-ui-restore/).

## Source and local checks

`website/build.py` generates ten complete HTML pages: Chinese home, installation, workflows, verification and tool selection, plus equivalent English pages. It also generates matching Markdown documents, an optional `llms.txt` reading index, a real 404 page and sitemap, and copies local assets. Only Python 3.10+ standard library is required. The skill installer and website do not need each other to run.

```bash
python3 website/build.py
python3 website/check.py
node --check website/assets/app.js
```

Output: `dist/site/` (ignored; do not commit generated pages or screenshots). To preview the production base path, serve a temporary parent directory containing `figma-ui-restore/` with the output files inside. Open `http://localhost:8000/figma-ui-restore/` after starting a local HTTP server on that directory. Do not serve the repository root or Git metadata.

Edit page content and templates in `website/build.py`, the tool-selection guide and Markdown exporter in `website/discovery.py`, and styles and behavior in `website/assets/`. Asset URLs include content fingerprints; changing CSS, JavaScript, the favicon or social image changes its URL query automatically, preventing stale styles after deployment. The original social card is a committed 1200×630 PNG; the favicon and teaching illustrations are original assets, not private Figma exports. No third-party fonts are loaded. The official deployment loads the owner-configured Cloudflare Web Analytics beacon for aggregate website metrics; local builds and forks leave it off by default. Feedback uses the Web3Forms API only after an explicit form submission; the rest of the website does not require an account or backend API. GitHub itself operates the hosting service; this is not a claim that the host keeps no access logs.

## Publishing

GitHub Settings → Pages → Build and deployment → Source must be **GitHub Actions**. The `Deploy website` workflow runs on relevant pushes to `main` or manual dispatch. It checks public content and generated pages, then uploads only `dist/site`. Deployment permission is limited to the deploy job (`pages: write`, `id-token: write`).

The source version is read from `plugin.json`. Fixed installation commands point to that version's release tag; they do not silently use unreleased main-branch skill changes. Installing the skill does not install or start this website.

## SEO and language rules

- Each indexable page has a unique title/description, self-canonical URL, complete visible HTML, one H1 and reciprocal Chinese/English hreflang links.
- English lives under `/en/`; language links preserve the corresponding document. No language detection redirects hide content from crawlers.
- JSON-LD describes the real project as SoftwareSourceCode and connects WebSite/WebPage/BreadcrumbList. Project identity stays consistent across documents in the same language. The tool-selection guide adds an Article with a visible author and actual source-review date. There are no invented ratings, customer counts or reviews.
- `sitemap.xml` contains only the ten canonical HTML pages. The 404 page is noindex. The project path is included in every local asset, canonical, share image and language URL.
- Social metadata uses the local PNG. Essential content and navigation remain usable without JavaScript; copy feedback and the illustrative comparison are progressive enhancements.
- Project Pages live in a subdirectory. A `robots.txt` in that subdirectory would not control crawling: robots must be served at the domain root. We do not add a misleading subdirectory robots file or change the account's root site. Inspect the root robots policy if crawling fails.
- Markdown exports are generated from the visible main content, retain commands and source links, and link back to their canonical HTML document. Footer links and `rel="alternate" type="text/markdown"` expose these representations. `llms.txt` is an optional reading index, not a crawler permission file, indexing requirement or ranking guarantee. Do not maintain a separate AI-only set of product claims.

For the query-intent audit, source references, owner-side indexing steps and measurement plan, see [Search discovery / SEO and GEO](search-discovery.md). Update the guide's visible review date and `GUIDE_REVIEWED` together only after actually reviewing its sources; builds must not invent fresh dates for unchanged content.

### Discovery revision — 2026-10-23

Replaced the abstract home headline with explicit Codex/Figma UI positioning and added a sourced, bilingual tool-selection guide. Ten HTML pages now have matching Markdown documents and an optional reading index. Browser checks measured all ten routes at 320px without document horizontal overflow; the Chinese home and guide were visually inspected at the default 1280px viewport, the English guide at 320px and 820px, and the Chinese guide's comparison container at 320px. Mobile navigation and corresponding-document language switching worked. The Markdown endpoint returned HTTP 200 with `text/markdown`; the browser may download it rather than render it. Static checks cover source-command fidelity and exported links. Existing seven Python distribution tests and ten Node feedback tests passed. These are local verification results; no search ownership verification, indexing submission or ranking improvement has been established.

After deployment, the owner can verify the URL-prefix property in Google Search Console and submit the sitemap. Add a verification meta tag only when the owner provides the intended token or completes the account setup. No Search Console property has been created or sitemap submitted by this source change. Successful deployment and correct metadata do not guarantee indexing or rankings.

For a future custom domain, configure the owned domain in Pages, update the generator's default `--base-url`, adjust `website/check.py`'s base/path constants and rebuild. Do not add an unowned domain or CNAME merely as a placeholder. Preserve redirects where supported when moving an indexed site.

## Public content boundary

Only generic instructions and original exercises may be published. Do not add private design URLs, file keys, node identifiers, customer content, screenshots, credentials or local machine paths. `website/check.py` rejects concrete Figma file URLs in website source and generated text. Run the repository validator too. Inspect any new images manually; text scans cannot prove a binary image contains no private information.

## 中文说明

官网采用默认 GitHub Pages 地址，内容与源码一起维护。每次改页面内容、样式或脚本后运行上述构建与检查；提交后由 Actions 自动发布。手机菜单、语言切换、复制按钮和示例样式切换应在浏览器中复验。截图留在临时目录，不随官网发布。

SEO 检查覆盖页面标题、描述、canonical、多语言互链、结构化数据、站点地图和内部资源链接。搜索引擎实际收录需上线后观察，Search Console 需站点所有者完成验证；不能用上线成功代替收录或排名结果。

## Local verification record — 2026-10-19

Eight generated language pages passed link, canonical, reciprocal-language, sitemap, JSON-LD and public-content checks. All eight rendered without document horizontal overflow at 320px. The Chinese home was inspected at 1440px; English home and Chinese installation were inspected at 390px. Browser actions confirmed the 32px/16px to 24px/8px demo transition, successful copy feedback, mobile navigation open/Escape close, and corresponding-document language switching. These are website checks, not acceptance of a user’s live design or proof of search-engine indexing.

## Visual refinement — 2026-10-19

Refined for designers and frontend developers: a light canvas, violet identity, an original design-properties/component-code workbench illustration, clearer mode cards, and a matching favicon/social card. Copy, routes, release installation targets and skill behavior are unchanged. The illustration is explicitly labeled as illustrative, not live Figma evidence or a real execution result.

The eight localized pages passed 320px overflow checks. Desktop home and comparison demo were inspected at 1440px; English home and Chinese install at 390px. Copy feedback, mobile navigation, corresponding-document language switching and before/after style changes were rechecked. SEO, link, privacy and asset fingerprint checks passed. Temporary screenshots remain outside the repository.

## Editorial redesign — 2026-10-19

This revision replaces the violet workbench composition with warm off-white, charcoal, restrained vermilion annotations and solid surfaces. The homepage leads with the existing original before/after exercise, now with a synchronized property inspector. Open steps and horizontal workflow rows replace repeated cards. Documentation uses the same typography, spacing, navigation and focus language. No runtime dependencies or fonts were added; installation targets, skill behavior and the eight language routes remain intact.

### Reference research and limits

The owner confirmed there is no website-specific Figma design. This is an original website design, not a pixel-level implementation of the unrelated private product prototype. No private design file was read or published for this work.

The following public homepages were read through web access on 2026-10-19. These observations concern accessible content and information structure, not verified computed styles or animation timing:

| Reference | Observed organization | Application to this website |
| --- | --- | --- |
| [Linear](https://linear.app) | Product positioning is followed by detailed interface examples and workflow sections. | Lead with a concrete comparison before explaining the method. |
| [Vercel](https://vercel.com) | Infrastructure capabilities are grouped around tasks and outcomes, with clear action links. | Keep installation prominent and separate workflows by actual task scope. |
| [v0](https://v0.app) | A direct creation question introduces examples, templates and capabilities. | Give users a clear first task and a copyable request. |
| [Framer](https://www.framer.com) | Idea-to-launch positioning is developed through editing and design examples. | Explain the progression from evidence to implementation to verification. |
| [Cursor](https://cursor.com) | The public page includes interface demonstrations and identifies their illustrative purpose. | Use an original, labeled, interactive teaching example. |
| [Onlook](https://www.onlook.ai) | Visual engineering is explained with editor and page content rather than abstract feature names alone. | Show the reference, implementation and inspected properties together. |
| [Lovable](https://lovable.dev) | Creation, refinement and deployment are presented as a connected journey. | Keep the homepage sequence coherent and end with the next concrete action. |

Browser attempts to open Linear, Vercel and Cursor failed with connection closure or navigation timeouts. Their live hover behavior, scroll transitions and current rendered appearance were **not** verified. The other four references were read as web content, without a browser visual review. The palette, typography, spacing, logo and CSS interactions in this revision are our own design decisions; no reference brand assets, customer claims or whole-page layouts were copied.

### Local browser verification

All eight localized pages were checked for document overflow at 320px. Chinese and English desktop homepages were visually inspected at 1440px; Chinese mobile home and installation, plus English mobile home, were checked at 390px. Browser checks covered before/after styling and inspector values, copy feedback, FAQ expansion, mobile menu opening, Escape closing with focus return, and language switching to the equivalent document. No browser script errors were reported during those checks. The original exercise remains illustrative and does not execute Codex, read Figma or send invitations.

Static build, Python compatibility, public-content/link/SEO validation, JavaScript syntax and the seven existing distribution tests passed. Local screenshots remain outside the repository. This does not verify private product designs, every assistive technology or search engine indexing. No Search Console setup was performed.


## Email feedback — 2026-10-19

The footer feedback link progressively enhances to a native `<dialog>` on all localized pages, with GitHub Issues as its no-JavaScript/unsupported-browser fallback. The original exercise and skill instructions are unaffected. The dialog supports a category, required message (5 non-whitespace characters, 3,000 UTF-16 code units maximum) and optional reply email. It includes visible provider disclosure and a link to the provider privacy policy. Drafts stay only in the current page DOM: closing/reopening preserves them, while navigating away or reloading discards them. No local storage, attachments, hidden analytics, query strings or URL fragments are submitted.

`website/assets/feedback.mjs` posts JSON directly to the fixed HTTPS Web3Forms endpoint with cookies omitted. A success UI requires both HTTP success and `success: true`. Rejected submissions, rate limits, malformed responses, network failures and a 20-second timeout keep the fields. There is no automatic retry because a timed-out request may already have been delivered. Pending fields and submit controls are disabled. The hidden `botcheck` field complements the provider's spam filtering; there is no claim that client-side controls stop direct API abuse. hCaptcha is not enabled in this first integration; it can be added if spam becomes a problem. The free service has quotas and no email-delivery guarantee.

### Deployment and reuse

The builder reads optional `WEB3FORMS_ACCESS_KEY`. This is a **public form identifier**, not an SMTP password or secret API token. It is necessarily visible in deployed HTML. Do not supply an email password, mail authorization code or service account credential. Missing configuration disables email submission with a localized explanation and the GitHub fallback; malformed identifiers fail the build.

The Pages workflow supplies the owner-approved public Form ID only when `github.repository` matches this upstream repository. Forks get an empty value and must replace that workflow expression with their own repository/Form ID or provide their own Actions variable. Local builds default to no email delivery. Installing the skill does not configure feedback or send mail. Neither the recipient address nor Form ID is placed in `skills/` or installation examples.

For a local configured preview, set `WEB3FORMS_ACCESS_KEY` to your own public Form ID before running `python3 website/build.py`. Run the existing static checks and `node --test tests/test_feedback.mjs`. The Node tests stub the transport; they do not send emails. Cross-platform CI runs those tests on Node 22, followed by existing Python validation and packaging.

### Verification scope

A single labeled Chinese integration test was submitted through the actual browser form, with the optional reply email blank. Web3Forms accepted it and the UI displayed the success state. This confirms API acceptance, not that a recipient opened it or that it reached the primary inbox. Inbox delivery needs the owner's mailbox confirmation. Do not repeat live tests merely for screenshots. Temporary UI fixtures and screenshot artifacts stay outside the repository.

Local UI checks covered desktop and mobile layouts, all eight language pages at 320×640 without horizontal overflow, blank-message validation, optional-email omission, character count, draft retention, close/Escape focus restoration, and forward/reverse Tab wrapping. An isolated browser fixture simulated a delayed 429 response followed by successful retry: it verified disabled pending controls, retained message/email, retry feedback and the success reset. That fixture made no network requests and is not distributed. Ten Node transport tests, seven existing Python distribution tests and static SEO/public-content checks passed locally. No full screen-reader or real mailbox delivery audit was performed.


## Cloudflare Web Analytics — 2026-10-20

The owner supplied the dashboard-generated module snippet for `fukuang-dev.github.io`. The builder inserts the official `https://static.cloudflareinsights.com/beacon.min.js` module immediately before `</body>` in all eight localized pages and the custom 404 page. No custom event tracking or feedback-field instrumentation is added. The feedback email, message and category are not passed to the analytics integration.

`CLOUDFLARE_WEB_ANALYTICS_TOKEN` is an optional **public beacon identifier**, not a Cloudflare account API token. Only a 32-character hexadecimal value is accepted; malformed input fails before output replacement. The Pages workflow configures the owner-provided identifier only for this upstream repository. Forks and local builds default to no beacon, and can supply their own public identifier if they choose to enable analytics. Do not add account API tokens or credentials to this variable. Installing the Skill neither installs nor runs this website or its beacon.

The checker verifies one consistent optional beacon configuration across all generated pages. Verify both an unconfigured build (no beacon) and a configured build (one matching script per page), while keeping existing SEO, asset, link and private-design checks intact. Do not load configured local previews repeatedly into the production property to manufacture traffic.

To view data: sign in to Cloudflare → Observability → Analytics → Web analytics → select `fukuang-dev.github.io`. Filter the path to `/figma-ui-restore/` when distinguishing this project from other instrumented sites on the same hostname. Existing history before installation cannot be reconstructed by this integration. Ad blockers, network failures and browser restrictions can prevent beacons; reported visits are measurements, not a complete server access log or a count of identified people. The source integration does not prove dashboard ingestion or historical counts.

Official references: [manual installation](https://developers.cloudflare.com/web-analytics/get-started/) and [data collection](https://developers.cloudflare.com/web-analytics/data-metrics/data-origin-and-collection/). Dashboard data can take a few minutes to appear after real visits. No DNS, hosting provider, domain ownership or Cloudflare account permissions were changed.
