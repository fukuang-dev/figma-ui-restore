# Website / 官网维护

Public site: [Figma UI Restore](https://fukuang-dev.github.io/figma-ui-restore/).

## Source and local checks

`website/build.py` generates eight complete HTML pages: Chinese home, installation, workflows and verification, plus equivalent English pages. It also generates a real 404 page and sitemap, and copies local assets. Only Python 3.10+ standard library is required. The skill installer and website do not need each other to run.

```bash
python3 website/build.py
python3 website/check.py
node --check website/assets/app.js
```

Output: `dist/site/` (ignored; do not commit generated pages or screenshots). To preview the production base path, serve a temporary parent directory containing `figma-ui-restore/` with the output files inside. Open `http://localhost:8000/figma-ui-restore/` after starting a local HTTP server on that directory. Do not serve the repository root or Git metadata.

Edit page content and templates in `website/build.py`, styles and behavior in `website/assets/`. The original social card is a committed 1200×630 PNG; the favicon and teaching illustrations are original assets, not private Figma exports. No third-party fonts, runtime scripts, tracking tools, accounts or server API are used. GitHub itself operates the hosting service; this is not a claim that the host keeps no access logs.

## Publishing

GitHub Settings → Pages → Build and deployment → Source must be **GitHub Actions**. The `Deploy website` workflow runs on relevant pushes to `main` or manual dispatch. It checks public content and generated pages, then uploads only `dist/site`. Deployment permission is limited to the deploy job (`pages: write`, `id-token: write`).

The source version is read from `plugin.json`. Fixed installation commands point to that version's release tag; they do not silently use unreleased main-branch skill changes. Installing the skill does not install or start this website.

## SEO and language rules

- Each indexable page has a unique title/description, self-canonical URL, complete visible HTML, one H1 and reciprocal Chinese/English hreflang links.
- English lives under `/en/`; language links preserve the corresponding document. No language detection redirects hide content from crawlers.
- JSON-LD describes the real project as SoftwareSourceCode and connects WebSite/WebPage/BreadcrumbList. There are no invented ratings, customer counts or reviews.
- `sitemap.xml` contains only the eight canonical pages. The 404 page is noindex. The project path is included in every local asset, canonical, share image and language URL.
- Social metadata uses the local PNG. Essential content and navigation remain usable without JavaScript; copy feedback and the illustrative comparison are progressive enhancements.
- Project Pages live in a subdirectory. A `robots.txt` in that subdirectory would not control crawling: robots must be served at the domain root. We do not add a misleading subdirectory robots file or change the account's root site. Inspect the root robots policy if crawling fails.

After deployment, the owner can verify the URL-prefix property in Google Search Console and submit the sitemap. Add a verification meta tag only when the owner provides the intended token or completes the account setup. No Search Console property has been created or sitemap submitted by this source change. Successful deployment and correct metadata do not guarantee indexing or rankings.

For a future custom domain, configure the owned domain in Pages, update the generator's default `--base-url`, adjust `website/check.py`'s base/path constants and rebuild. Do not add an unowned domain or CNAME merely as a placeholder. Preserve redirects where supported when moving an indexed site.

## Public content boundary

Only generic instructions and original exercises may be published. Do not add private design URLs, file keys, node identifiers, customer content, screenshots, credentials or local machine paths. `website/check.py` rejects concrete Figma file URLs in website source and generated text. Run the repository validator too. Inspect any new images manually; text scans cannot prove a binary image contains no private information.

## 中文说明

官网采用默认 GitHub Pages 地址，内容与源码一起维护。每次改页面内容、样式或脚本后运行上述构建与检查；提交后由 Actions 自动发布。手机菜单、语言切换、复制按钮和示例样式切换应在浏览器中复验。截图留在临时目录，不随官网发布。

SEO 检查覆盖页面标题、描述、canonical、多语言互链、结构化数据、站点地图和内部资源链接。搜索引擎实际收录需上线后观察，Search Console 需站点所有者完成验证；不能用上线成功代替收录或排名结果。

## Local verification record — 2026-10-19

Eight generated language pages passed link, canonical, reciprocal-language, sitemap, JSON-LD and public-content checks. All eight rendered without document horizontal overflow at 320px. The Chinese home was inspected at 1440px; English home and Chinese installation were inspected at 390px. Browser actions confirmed the 32px/16px to 24px/8px demo transition, successful copy feedback, mobile navigation open/Escape close, and corresponding-document language switching. These are website checks, not acceptance of a user’s live design or proof of search-engine indexing.
