# Search discovery / SEO 与 GEO

## 2026-10-23 的检索复盘

起点问题是“推荐 Codex 连接 Figma 还原产品设计 UI 的工具”。此前回答使用了偏向官方文档的查询，例如 `site.developers.openai.com codex Figma plugin MCP design implementation`，随后转向官方 MCP 和浏览器验证资料。这条路径适合核对官方连接方式，却没有完整覆盖社区还原技能和现有项目工作流。不能把回答者的检索范围问题直接归因于本站 SEO。

后续混合查询中未看到本站，也不是“所有搜索引擎未收录”的证明。同名技能还出现在其他公开仓库中；品牌发现需要把 **Figma UI Restore / figma-ui-restore / fukuang-dev / Codex skill** 联系清楚。仅凭同名不能认定是同一项目。

检查过的实际证据：

| 检查 | 本次观察 | 解释范围 |
| --- | --- | --- |
| 线上首页 HTTPS 请求 | HTTP 200，返回完整 HTML | 排除本次请求中的首页宕机；不证明所有抓取器都可访问 |
| 线上 sitemap | 可读取，发布版含八个 HTML URL | 发布版已有基础发现入口；不证明引擎已读取 |
| 域名根 `/robots.txt` | HTTP 404 | 本次未取得禁止规则；不证明每个爬虫都成功抓取 |
| 网页抓取工具打开首页 | 工具报无法访问；普通 HTTP 请求成功 | 记录工具差异，不把它等同于网站不可用 |
| 已有源码 | 静态 HTML、独立标题/描述、canonical、hreflang、JSON-LD、sitemap | 基础 SEO 已存在，继续机械添加同类标签不是主要改进 |
| 搜索后台 | 本次没有访问 Search Console 或 Bing Webmaster Tools | 实际覆盖率、展示量、关键词排名及抓取错误仍待后台证据 |

## 本次实现与目标

1. 首页 H1 和首段直接说明“用 Codex 还原 Figma UI”，说明开源技能身份与适用范围，保留品牌名、作者和源码链接。
2. 新增中英文 `/codex-figma-ui-tools/`、`/en/codex-figma-ui-tools/`。正文先回答工具怎么搭配，再比较官方 Figma MCP、本技能、浏览器工具、Code Connect；区分用途、前置条件与限制。
3. 页面包含维护者身份、实际资料核对日期、官方来源、技能源码、验证矩阵与原创练习。它是维护者的选型建议，不冒充独立评测。
4. 通过首页、导航和文档侧栏链接选型指南，避免只在 sitemap 中出现的孤立入口。新增页面拥有独立 canonical、双向语言链接、标题与描述，并进入 sitemap。
5. 同一语言内保持 SoftwareSourceCode 实体一致；选型文档的 Article 与可见作者、日期相符。不添加虚构评分、下载量、用户证言或“还原率”。
6. 从实际 HTML 正文生成 `index.md`，保留多行命令和引用链接，提供 HTML 返回地址。页脚和 alternate 链接公开文本入口；`llms.txt` 仅作可选文档索引。

GEO 在这里指让答案检索系统更容易理解、核实和引用公开内容。不存在一项由本站控制的“AI 必须推荐”开关。Google 明确说明，其 AI 搜索功能沿用 SEO 基础，不要求额外的 AI 文本文件或专用 schema；因此 Markdown 和 `llms.txt` 的价值是读取便利，不能写成排名因素。[Google AI features](https://developers.google.com/search/docs/appearance/ai-features)

## 发布后的所有者操作

这些操作涉及站点所有权和外部账户，本次源码优化没有代为完成。

1. 按正常流程发布，确认首页、中英文选型指南、sitemap、Markdown 与 llms.txt 实际返回成功。源码检查通过不能替代发布检查。
2. 在 Google Search Console 添加或使用 `https://fukuang-dev.github.io/figma-ui-restore/` 的 URL 前缀资源，并完成其提供的所有权验证。根据选择的 HTML 文件或 meta 验证方法，再加入后台实际给出的文件/标识，不使用占位 token。
3. 提交 `https://fukuang-dev.github.io/figma-ui-restore/sitemap.xml`。检查首页及两个选型 URL 的实时抓取、索引状态和 Google 选择的 canonical。后台可用时再请求索引；提交不是收录保证。[Search Console guide](https://developers.google.com/search/docs/monitor-debug/search-console-start)
4. 如果使用 Bing Webmaster Tools，同样验证站点并提交 sitemap，分别观察 Bing 数据；不能用 Google 的状态推断 Bing 的状态。
5. 后续若增加根站、CDN 或自定义域名，再核对根目录 robots 与防火墙。项目子路径的 robots.txt 无效，不在当前项目里生成一个伪控制文件。[robots location](https://developers.google.com/search/docs/crawling-indexing/robots/intro)
6. 若调整 OpenAI 爬虫规则，先区分搜索用的 OAI-SearchBot 与训练用的 GPTBot，再依据所有者意图配置；不要为搜索曝光擅自改变训练许可。[OpenAI crawler documentation](https://developers.openai.com/api/docs/bots)

## 后续值得补的内容

- **一份可公开复现的真实案例**：原始规格或有再分发权的设计、初始代码、调用请求、实际改动、同视口前后截图、检查命令、环境版本和剩余差异。当前原创演示不能包装成真实客户成果。
- **一份独立英文上手教程**：围绕一个实际任务，完整展示安装、设计读取、局部修复和复验。优先完善现有教程，避免批量生成换关键词的近似页面。
- **真实的项目传播入口**：在合适的技能/工具目录、技术文章和讨论里介绍实际用法，注明作者身份并链接对应指南。外部发帖、评论和提交目录需要另外执行；不制造评分、转载网络或虚假背书。

## 如何评估是否有改善

发布时记录真实日期、提交 SHA 和后台基线。按周或按月比较同长度时间段，先看发现和索引，再看非品牌展示量、点击和目标页；新站数据少时延长观察，不能承诺几天内见效。

| 查询类别 | 示例 | 观察项 |
| --- | --- | --- |
| 品牌与作者 | `Figma UI Restore fukuang-dev`、`figma-ui-restore Codex` | 是否识别正确项目，官网/仓库是否出现 |
| 中文任务 | `Codex Figma UI 还原 工具`、`Codex Figma 局部样式修复` | 指南与任务的匹配、非品牌展示及点击 |
| 英文任务 | `Codex Figma UI tools`、`Figma to code Codex skill` | 英文指南发现、目标地区/语言表现 |
| 对比问题 | `Figma MCP vs UI restore skill`、`Codex Figma browser verification` | 是否准确区分连接、工作流和运行验证 |
| AI 回答抽样 | 固定原始问题，在记录环境中少量复测 | 是否检索并正确引用官网/仓库，是否夸大能力 |

AI 抽样需记录日期、产品/模型、问题、联网与来源限制、实际引用 URL 及回答是否准确。不同工具会使用不同索引和检索策略，结果有波动；带官方域名限定的查询与开放工具推荐查询分开评估。浏览量统计无法直接证明 AI 提及率或搜索索引覆盖率。

## 本地检查

```bash
python3 website/build.py
python3 website/check.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
node --check website/assets/app.js
node --test tests/test_feedback.mjs
```

浏览器另查十个 HTML 页面在桌面和窄屏的排版、导航、语言切换、表格横向容器和文本入口。自动检查覆盖新路由、canonical/语言/sitemap 关系、项目实体一致性、正文与 Markdown 命令保真、导出链接及锚点、索引完整性和公开内容边界。检查通过后无需为未变化的代码反复执行整套流程。
