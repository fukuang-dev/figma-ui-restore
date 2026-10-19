#!/usr/bin/env python3
"""Build the bilingual, dependency-free project website into dist/site."""
import argparse
import html
import json
from pathlib import Path
import shutil
from urllib.parse import urlparse
from xml.etree.ElementTree import Element, SubElement, ElementTree

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist/site'
REPO = 'https://github.com/fukuang-dev/figma-ui-restore'
VERSION = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))['version']
PAGES = ('home', 'install', 'workflows', 'verification')
LABELS = {
 'zh': {'home':'首页','install':'快速开始','workflows':'使用指南','verification':'验收方法','lang':'English','menu':'打开导航','skip':'跳到正文','github':'GitHub 源码','copy':'复制','copied':'已复制','copyfail':'无法自动复制，请选中并手动复制。','footer':'以设计证据还原，以浏览器结果验收。','legal':'独立社区开源项目，与 OpenAI、Figma 无官方隶属关系。','back':'返回首页','docs':'使用文档','next':'继续阅读','author':'作者'},
 'en': {'home':'Home','install':'Quick start','workflows':'Workflows','verification':'Verification','lang':'中文','menu':'Open navigation','skip':'Skip to content','github':'View on GitHub','copy':'Copy','copied':'Copied','copyfail':'Copy unavailable. Select the text and copy it manually.','footer':'Restore from evidence. Verify in the browser.','legal':'Independent open-source community project. Not affiliated with OpenAI or Figma.','back':'Back home','docs':'Documentation','next':'Keep reading','author':'By'}
}
META = {
 'zh': {
  'home': ('Figma UI Restore — Codex Figma UI 还原与交互验收技能','开源 Codex 技能，支持 Figma 页面还原、局部样式修复、产品原型交互流程和 UI 验收。提供安装教程、调用示例与真实浏览器验证方法。'),
  'install': ('安装与快速开始 — Figma UI Restore','安装 Figma UI Restore Codex 技能：内置 Skill Installer、Python 项目安装及插件安装。了解 Figma 授权、浏览器准备与第一次调用。'),
  'workflows': ('Figma 还原与页面交互指南 — Figma UI Restore','学习整页 Figma 还原、局部视觉修复与只读 UI 验收。产品有原型连线时遵循流程，没有定义时基于现有代码分析界面交互。'),
  'verification': ('UI 视觉与交互验收方法 — Figma UI Restore','区分代码检查、设计证据、浏览器视觉对比与交互路径执行。查看 Figma UI Restore 验收清单、公开演示和已验证范围。')},
 'en': {
  'home': ('Figma UI Restore — Figma to Code Skill for Codex','An open-source Codex skill for evidence-based Figma UI implementation, focused visual fixes, product prototype flows and browser verification. Install and get started.'),
  'install': ('Install the Codex Skill — Figma UI Restore','Install Figma UI Restore with Skill Installer, the dependency-free Python installer or the plugin wrapper. Prepare Figma access and your first browser-verified task.'),
  'workflows': ('Figma Implementation and Interaction Workflows — Figma UI Restore','Use full-page implementation, focused visual fixes and read-only UI audits. Follow product prototype flows and analyze missing UI behavior from existing code.'),
  'verification': ('Visual and Interaction Verification — Figma UI Restore','Separate code checks, design evidence, browser visual comparison and executed interaction paths. Explore the original demo, acceptance checklist and tested scope.')}
}

def esc(text): return html.escape(str(text), quote=True)
def path(lang, page='home'):
    return ('en/' if lang == 'en' else '') + (page + '/' if page != 'home' else '')
def local(lang, page='home'): return PREFIX + path(lang,page)
def link(lang,page,text,cls=''): return f'<a class="{cls}" href="{local(lang,page)}">{text}</a>'
def code(text,lang,label=''):
    d=LABELS[lang]
    manual = "手动复制" if lang == "zh" else "Copy manually"
    return f'<div class="code-block"><div class="code-toolbar"><span>{esc(label or "PROMPT / CODE")}</span><button type="button" data-copy data-copy-label="{d["copy"]}" data-copied-label="{d["copied"]}" data-copy-fail="{d["copyfail"]}" data-manual-label="{manual}">{d["copy"]}<span aria-hidden="true"> ↗</span></button></div><pre><code>{esc(text)}</code></pre></div>'
def section(title,body,id=''):
    return f'<section class="article-section"'+(f' id="{id}"' if id else '')+f'><h2>{title}</h2>{body}</section>'
def callout(title,body): return f'<aside class="note"><strong>{title}</strong><p>{body}</p></aside>'

def demo(lang):
    zh=lang=='zh'
    return f'''<div class="demo" data-demo data-good="true">
      <div class="demo-toolbar"><span class="demo-tag"><i></i> {'原创交互演示' if zh else 'ORIGINAL INTERACTIVE DEMO'}</span><span class="demo-view">{'静态示例 · 不连接 Figma' if zh else 'Static example · no Figma connection'}</span></div>
      <div class="demo-canvases"><div class="demo-pane reference"><span class="pane-label">01 / {'设计规格' if zh else 'REFERENCE'}</span><div class="mini-window"><div class="mini-top"><span class="mini-brand">m.</span><span>workspace / team</span><span>···</span></div><div class="mini-content"><span class="mini-eyebrow">TEAM SETTINGS</span><h3>Make room<br>for your team.</h3><p class="mini-secondary">A shared space for good work.</p><div class="member"><span class="avatar">AL</span><div><strong>Alex Lee</strong><span>Workspace owner</span></div><span class="member-role">Admin</span></div><span class="mini-button">Invite member <span>↗</span></span></div></div><div class="measurement"><span>24px / 600</span><span>radius 8px</span></div></div>
      <div class="demo-pane implementation"><span class="pane-label">02 / {'运行界面示意' if zh else 'IMPLEMENTATION'}</span><div class="mini-window"><div class="mini-top"><span class="mini-brand">m.</span><span>workspace / team</span><span>···</span></div><div class="mini-content"><span class="mini-eyebrow">TEAM SETTINGS</span><h3>Make room<br>for your team.</h3><p class="mini-secondary">A shared space for good work.</p><div class="member"><span class="avatar">AL</span><div><strong>Alex Lee</strong><span>Workspace owner</span></div><span class="member-role">Admin</span></div><span class="mini-button">Invite member <span>↗</span></span></div></div><div class="measurement"><span data-font-value>24px / 600</span><span data-radius-value>radius 8px</span></div></div></div>
      <div class="demo-bottom"><div class="segmented" role="group" aria-label="{'切换示例样式' if zh else 'Switch example styles'}"><button type="button" data-demo-mode="before" aria-pressed="false">{'修复前' if zh else 'Before'}</button><button type="button" data-demo-mode="after" aria-pressed="true">{'修复后' if zh else 'After'}</button></div><p data-demo-status aria-live="polite" data-before="{'演示：字号 32px，圆角 16px，次级文字层级不符。' if zh else 'Example: 32px heading, 16px radius and incorrect secondary text hierarchy.'}" data-after="{'演示：字号、圆角与次级文字颜色匹配规格。' if zh else 'Example: typography, radius and secondary color match the specification.'}">{'演示：字号、圆角与次级文字颜色匹配规格。' if zh else 'Example: typography, radius and secondary color match the specification.'}</p></div>
    </div>'''

def home(lang):
 zh=lang=='zh'
 if zh:
  hero='从设计稿，<br>到<span class="highlight">经得起对照</span><br>的界面。'
  lead='给 Codex 一套有依据的还原流程。读取 Figma、接入现有项目、核对交互，最后在真实浏览器中完成验收。'
  modes=[('01','整页还原','先锁定原稿、状态与资产，再实现一个可验收样板，逐步扩展。','完整实现'),('02','局部修复','字号、间距、颜色或控件尺寸，只定位相关组件，最小修改后局部复验。','快速模式'),('03','只读验收','逐项列出设计值、运行值、证据与影响；保留代码和现有基准。','审查模式')]
  workflow=[('READ','读取真正的设计证据','结构化属性决定数值，截图用于整体对照；估计始终标明为估计。'),('BUILD','融入你的现有项目','复用组件、国际化和正式资产，沿用业务逻辑与 API。'),('VERIFY','在浏览器里核对结果','查看实际样式、状态与点击结果，修正差异后再验一次。')]
  policytitle='页面怎么走，<br>也属于还原。'
  policytext='有产品连线就遵循产品，没有定义就分析现有实现。界面做对，也要让操作去到正确的地方。'
  flows=[('01','产品有定义','读取原型连线、流程图和说明，保留触发条件、动作与目标。'),('02','产品未定义','结合当前路由、组件状态和同类交互，补齐有依据的 UI 行为。'),('03','证据未读取','明确权限或工具缺口；未知不等于产品没画，不猜测业务规则。')]
  questions=[('需要安装什么？','需要支持技能的 Codex 环境。实时读取设计还需要 Figma 连接，视觉验收还需要当前会话可用的浏览器工具。'),('支持 React 之外的项目吗？','技能不绑定特定框架，沿用目标项目的技术栈、组件、包管理器和必要检查。'),('会改动我的业务逻辑吗？','默认保留 API、权限、校验和业务状态约束。产品流程与现有业务约束冲突时，列出具体缺口，不自行绕过。'),('安装后会自动连接 Figma 吗？','不会。技能提供工作流程，Figma 授权和浏览器能力由使用环境单独提供。')]
 else:
  hero='From design.<br>To an interface<br><span class="highlight">you can verify.</span>'
  lead='Give Codex a workflow grounded in evidence. Read Figma, work inside your existing project, follow product flows, and verify the result in a real browser.'
  modes=[('01','Full implementation','Establish the reference, states and assets. Verify one representative slice before expanding.','FULL RESTORE'),('02','Focused fixes','Correct typography, spacing, color or control sizing with a small patch and local verification.','FOCUSED MODE'),('03','Read-only audits','Report expected and actual values, evidence and impact. Leave code and baselines untouched.','AUDIT MODE')]
  workflow=[('READ','Read real design evidence','Structured properties establish values. Screenshots support the comparison. Estimates stay labeled.'),('BUILD','Fit your existing project','Reuse components, localization and original assets. Preserve business behavior and APIs.'),('VERIFY','Check the running browser','Inspect actual styles, states and interaction outcomes. Correct differences, then check again.')]
  policytitle='The way it works<br>is part of the design.'
  policytext='Follow product-defined connections. Analyze existing behavior where the product is silent. Restore where actions lead, as well as how they look.'
  flows=[('01','Product-defined','Read prototype connections, flowcharts and specifications. Preserve triggers, conditions and targets.'),('02','Not defined','Use existing routes, component state and analogous interactions to derive supported UI behavior.'),('03','Not yet read','Name access and tool gaps. Unknown evidence does not mean the product supplied no flow.')]
  questions=[('What do I need?','A skill-capable Codex environment. Live design reads also need a Figma connection; visual acceptance needs browser tools in the current session.'),('Does it work beyond React?','The skill follows your project’s framework, components, package manager and required checks. It is not tied to a particular frontend stack.'),('Will it change business behavior?','It preserves APIs, permissions, validation and business state constraints. Conflicts are reported rather than silently bypassed.'),('Does installation connect Figma?','No. The skill supplies the workflow. Figma authorization and browser capabilities come from your own environment.')]
 first='开始使用' if zh else 'Get started'
 modehtml=''.join(f'<a class="mode-row" href="{local(lang,"workflows")}#{["full","focused","audit"][i]}"><span class="mode-number">{n}</span><div><span class="eyebrow">{tag}</span><h3>{title}</h3></div><p>{body}</p><span class="row-arrow" aria-hidden="true">↗</span></a>' for i,(n,title,body,tag) in enumerate(modes))
 steps=''.join(f'<div class="process-step"><span class="step-code">{n}</span><h3>{title}</h3><p>{body}</p></div>' for n,title,body in workflow)
 flowhtml=''.join(f'<div class="flow-row"><span>{n}</span><div><h3>{title}</h3><p>{body}</p></div></div>' for n,title,body in flows)
 faqs=''.join(f'<details><summary>{q}<span aria-hidden="true">+</span></summary><p>{a}</p></details>' for q,a in questions)
 prompt=('使用 $figma-ui-restore。\n设计：[你的节点链接]\n目标：[页面路由或组件]\n请按设计还原，优先遵循产品交互流程，\n保留现有业务逻辑，并在浏览器中对照复验。' if zh else 'Use $figma-ui-restore.\nDesign: [your node URL]\nTarget: [route or component]\nRestore the design, follow product interaction flows,\npreserve business behavior and verify in the browser.')
 return f'''<section class="hero wrap"><div class="hero-copy"><div class="release-pill"><span></span> OPEN SOURCE <b>v{VERSION}</b></div><h1>{hero}</h1><p class="hero-lead">{lead}</p><div class="hero-actions">{link(lang,'install',first+' <span aria-hidden="true">↗</span>','button primary')}<a class="button plain" href="{REPO}">{LABELS[lang]['github']} <span aria-hidden="true">↗</span></a></div><p class="hero-meta">MIT LICENSE <span>·</span> CODEX SKILL <span>·</span> 中文 / ENGLISH</p></div><div class="hero-art"><div class="art-caption"><span>FIGMA → CODE → BROWSER</span><span>01—03</span></div><div class="blueprint"><div class="blueprint-heading"><span class="bracket">[ ]</span><span>DESIGN EVIDENCE</span><span class="tiny-plus">+</span></div><div class="blueprint-line wide"></div><div class="blueprint-line"></div><div class="blueprint-boxes"><span></span><span></span><span></span></div><div class="blueprint-ruler"><i></i><span>gap: 16</span><i></i></div></div><div class="terminal"><div class="terminal-top"><span class="terminal-dots">● ● ●</span><span>figma-ui-restore</span><span>↗</span></div><div class="terminal-body"><p><span class="terminal-muted">$</span> figma-ui-restore</p><p><span class="terminal-check">✓</span> Read design properties</p><p><span class="terminal-check">✓</span> Follow product flows</p><p><span class="terminal-check">✓</span> Compare in the browser</p><div class="terminal-result"><span class="terminal-check">↳</span> Evidence before confidence<span class="cursor"></span></div></div></div><div class="art-footnote">{'工作流程示意 · 非真实执行日志' if zh else 'Workflow illustration · not an execution log'}</div></div></section>
 <div class="principles"><div class="wrap"><span>{'设计证据优先' if zh else 'EVIDENCE FIRST'}</span><i>✳</i><span>{'保留现有业务' if zh else 'EXISTING BUSINESS LOGIC'}</span><i>✳</i><span>{'真实浏览器复验' if zh else 'REAL BROWSER CHECKS'}</span><i>✳</i><span>{'不确定项明确标注' if zh else 'HONEST LIMITATIONS'}</span></div></div>
 <section class="wrap section"><div class="section-heading"><span class="eyebrow">01 / RIGHT-SIZED WORKFLOW</span><h2>{'大任务有闭环，<br>小修改有分寸。' if zh else 'A full loop.<br>For the scope you need.'}</h2><p>{'三种工作模式，沿用同一套证据标准。局部修复无需重复做整页调查。' if zh else 'Three modes. One standard of evidence. A small visual fix does not need a whole-page investigation.'}</p></div><div class="mode-list">{modehtml}</div></section>
 <section class="section demo-section"><div class="wrap"><div class="section-heading compact"><span class="eyebrow">02 / SEE THE DIFFERENCE</span><h2>{'不是“看着差不多”。<br>是差异有据可查。' if zh else 'Beyond “looks close.”<br>Make the difference visible.'}</h2><p>{'切换修复前后，观察字号、圆角与文字层级。此处为原创静态教学示例，不代表真实 Figma 任务已验收。' if zh else 'Switch before and after to inspect typography, radius and text hierarchy. This original static teaching example is not a verified live Figma task.'}</p></div>{demo(lang)}</div></section>
 <section class="wrap section process"><div class="section-heading"><span class="eyebrow">03 / HOW IT WORKS</span><h2>{'把还原变成<br>可核验的过程。' if zh else 'A process you can<br>actually inspect.'}</h2></div><div class="process-grid">{steps}</div></section>
 <section class="flow-section"><div class="wrap flow-grid"><div><span class="eyebrow">04 / INTERACTION LOGIC</span><h2>{policytitle}</h2><p>{policytext}</p>{link(lang,'workflows',('了解交互流程规则' if zh else 'Explore interaction rules')+' ↗','text-link')}</div><div>{flowhtml}</div></div></section>
 <section class="wrap section start-section"><div><span class="eyebrow">05 / YOUR FIRST TASK</span><h2>{'从一个真实页面，<br>开始你的第一次还原。' if zh else 'Start with one page.<br>Make the first task count.'}</h2><p>{'安装技能，提供设计节点与目标页面。缺失信息能查则查，只询问真正阻塞的决定。' if zh else 'Install the skill and provide a design node and target page. Recover available context; clarify only decisions that block progress.'}</p>{link(lang,'install',('查看完整安装步骤' if zh else 'Read the installation guide')+' ↗','text-link')}</div>{code(prompt,lang,'CODEX / FIRST TASK')}</section>
 <section class="wrap section faq-section"><div><span class="eyebrow">06 / GOOD TO KNOW</span><h2>{'开始之前，<br>你可能想知道。' if zh else 'A few things<br>worth knowing.'}</h2></div><div class="faq-list">{faqs}</div></section>
 <section class="final-cta wrap"><span class="eyebrow">BUILD WITH EVIDENCE.</span><h2>{'把下一次还原，<br>做得更有依据。' if zh else 'Your next interface.<br>Built on better evidence.'}</h2><div>{link(lang,'install',first+' ↗','button primary')}<a class="button plain" href="{REPO}/releases">{'下载最新版本' if zh else 'Download a release'} ↗</a></div></section>'''


def install(lang):
 zh=lang=='zh'
 clone_cmd = f"git clone --branch v{VERSION} --depth 1 {REPO}.git\ncd figma-ui-restore\npython3 scripts/validate.py"
 project_cmd = "python3 scripts/install.py --project /path/to/your-project --dry-run\npython3 scripts/install.py --project /path/to/your-project"
 plugin_cmd = f"codex plugin marketplace add fukuang-dev/figma-ui-restore --ref v{VERSION}\ncodex plugin add figma-ui-restore@figma-ui-restore-community"
 mcp_zh = "codex mcp list\n# 仅在尚未配置 Figma 时添加并授权\ncodex mcp add figma --url https://mcp.figma.com/mcp\ncodex mcp login figma"
 mcp_en = "codex mcp list\n# Add and authorize only if Figma is not configured\ncodex mcp add figma --url https://mcp.figma.com/mcp\ncodex mcp login figma"
 if zh:
  intro='先安装技能，再确认设计和浏览器可用。三种安装方式任选一种，避免同名技能重复出现。'
  prereq='<ul><li>支持技能的 Codex 环境和一个可以运行的前端项目。</li><li>有权访问的设计节点，或明确的 SVG、PNG、离线规格。</li><li>进行视觉验收时，当前会话需要浏览器截图与页面检查能力。</li></ul>'
  installer=f'使用 $skill-installer 安装这个仓库的技能：\n{REPO}\n技能目录：skills/figma-ui-restore\n版本：v{VERSION}\n已有同名技能时保留定制内容，不直接覆盖。'
  sections=section('01 / 准备环境',prereq)+section('02 / 使用内置安装器',f'<p>在 Codex 中发送下面的请求。安装完成后查看返回路径；如果技能尚未出现，重启 Codex 或重新打开项目。</p>{code(installer,lang,"CODEX / INSTALL")}')
  sections+=section('03 / 或者，用 Python 安装',f'<p>只需要 Python 3.10+ 标准库。Windows 可将 <code>python3</code> 换成 <code>py -3</code>。先克隆固定版本：</p>{code(clone_cmd,lang,"TERMINAL")}<p>在现有项目中安装，替换成你的实际项目路径：</p>{code(project_cmd,lang,"PROJECT INSTALL")}<p>目标为 <code>&lt;项目&gt;/.agents/skills/figma-ui-restore/</code>。也可使用 <code>--user</code> 安装到个人技能目录。安装器拒绝覆盖，不修改 AGENTS.md、MCP 配置或凭证。</p>')
  sections+=section('04 / 插件安装方式',f'<p>支持插件命令的客户端可使用以下方式；先通过 <code>codex plugin --help</code> 确认当前版本支持。插件与直接安装共用一份技能，无需同时安装。</p>{code(plugin_cmd,lang,"PLUGIN")}')
  sections+=section('05 / 确认 Figma 连接',f'<p>复用已授权的官方 Figma 插件或连接器。尚未配置时，按 <a href="https://learn.chatgpt.com/docs/extend/mcp?surface=cli">Codex MCP 文档</a>和 <a href="https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/">Figma 远程 MCP 文档</a>完成连接。先检查现有连接，避免重复配置。</p>{code(mcp_zh,lang,"TERMINAL / OPTIONAL")}<p>在 Figma 选中目标 Frame 或组件，复制具体节点链接。先请 Codex 只读返回节点名称、尺寸、关键属性和对应截图，实际取得证据后再开始还原。使用离线规格无需 Figma 登录，但需标注证据来源。</p>')
  sections+=section('06 / 发起第一次任务',code('使用 $figma-ui-restore。\n设计：[你的具体节点或原型链接]\n目标：[路由或组件路径]\n运行地址：[你的本地预览地址]\n还原该页面及相关交互。保留现有业务逻辑，\n在浏览器中对照、修正和复验，分别报告视觉与交互结果。',lang)+callout('更新已有安装','先备份自定义修改，把旧技能移到发现目录之外，再安装新版。不要把旧备份留成另一个同名技能。')+f'<p>更多说明：<a href="{REPO}/blob/main/README.md">完整中文 README</a>。</p>')
 else:
  intro='Install the skill, then verify design and browser access. Choose one installation method to avoid duplicate copies.'
  sections=section('01 / Prerequisites','<ul><li>A skill-capable Codex environment and a working frontend project.</li><li>An authorized design node or explicit offline SVG/PNG/specification.</li><li>Browser screenshot and page-inspection tools for visual acceptance.</li></ul>')
  installer=f'Use $skill-installer to install skills/figma-ui-restore\nfrom {REPO}\nat tag v{VERSION}. Preserve existing customizations;\ndo not overwrite an existing skill implicitly.'
  sections+=section('02 / Built-in installer',f'<p>Send the request below to Codex. Check the returned path and restart Codex or reopen the project if discovery has not refreshed.</p>{code(installer,lang,"CODEX / INSTALL")}')
  sections+=section('03 / Or install with Python',f'<p>Requires Python 3.10+ standard library only. On Windows, use <code>py -3</code> if appropriate.</p>{code(clone_cmd,lang,"TERMINAL")}<p>Replace the example with your existing project directory:</p>{code(project_cmd,lang,"PROJECT INSTALL")}<p>The destination is <code>&lt;project&gt;/.agents/skills/figma-ui-restore/</code>. Use <code>--user</code> for your personal skill directory instead. The installer refuses existing destinations and does not edit AGENTS.md, MCP settings or credentials.</p>')
  sections+=section('04 / Plugin installation',f'<p>Check <code>codex plugin --help</code> for client support. The plugin wraps the same skill; do not install both copies.</p>{code(plugin_cmd,lang,"PLUGIN")}')
  sections+=section('05 / Verify Figma access',f'<p>Reuse your authorized official Figma plugin or connector. For setup, follow <a href="https://learn.chatgpt.com/docs/extend/mcp?surface=cli">Codex MCP documentation</a> and <a href="https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/">Figma remote MCP documentation</a>. Inspect existing connections first.</p>{code(mcp_en,lang,"TERMINAL / OPTIONAL")}<p>Copy a link to the actual Frame or component. First request a read-only check returning the node name, dimensions, key properties and matching screenshot. Offline specifications do not require Figma login; label the evidence source.</p>')
  sections+=section('06 / Run your first task',code('Use $figma-ui-restore.\nDesign: [your specific node or prototype URL]\nTarget: [route or component]\nRunning URL: [your local preview URL]\nRestore this page and its relevant interactions.\nPreserve business behavior; compare, fix and re-check\nin the browser. Report visual and interaction results separately.',lang)+callout('Updating an existing install','Back up custom changes, move the old skill outside discovery directories, and install the new version. Do not leave a second discoverable copy.')+f'<p>More details: <a href="{REPO}/blob/main/README.en.md">complete English README</a>.</p>')
 return article(lang,'install',intro,sections)


def workflows(lang):
 zh=lang=='zh'
 if zh:
  intro='根据实际范围选择流程。大任务保留证据与闭环，小修复保持局部；交互来源始终清楚。'
  body=section('整页或多页还原','<p>确定具体设计节点、目标路由、语言和状态。读取相关属性、截图及原始资产，再检查现有组件和数据流。先完成一个代表性页面或状态，经过浏览器对照再扩展。</p><p>关键数值区分设计事实、项目继承、实现假设和已批准差异。原组件的默认颜色、阴影或提示，并不自动等于设计要求。</p>'+code('使用 $figma-ui-restore。\n设计：[节点链接]；目标：[路由]；运行地址：[URL]。\n还原页面及相关弹窗状态，先验证一个代表性状态，\n再扩展其他状态。保留现有组件和业务行为。',lang),'full')
  body+=section('少量样式快速修复','<p>单个或少数明确的字号、行高、间距、颜色、圆角或控件尺寸问题，定位直接相关组件并最小修改。有效的已有证据可以复用，不重复导出整页或调查无关业务。</p><p>用同一视口和状态复验目标区域及邻近布局。涉及共享组件时抽查受影响调用点，仍遵守项目必跑检查。</p>'+code('使用 $figma-ui-restore。\n只修复 [区域] 的字号、间距与文字颜色。\n保留数据、列宽和交互，使用局部前后截图复验，\n不扩大成全页重做。',lang),'focused')
  body+=section('只读 UI 验收','<p>对照设计与运行页面，列出预期、实际、来源、影响和可能的代码位置。只交付差异和建议，不修改代码、配置或截图基准。</p>'+code('使用 $figma-ui-restore。\n对照 [设计节点] 检查 [运行地址]。\n只读验收：列出设计值、实际值、影响和代码位置。\n不修改应用文件或视觉基准。',lang),'audit')
  body+=section('页面交互：先确认产品定义',flow_table(lang)+ '<p>读取触发元素、事件、条件、动作与目标。区分导航、返回、弹层开关、组件状态、滚动和条件动作；原型里的每个 Frame 不一定需要一个新路由。</p><p>产品未定义时，分析现有路由、组件状态和同类交互，直接实施可靠推导的界面行为并标明依据。若产品只画了一部分，保留已有流程，仅补缺失分支。</p>'+callout('UI 推导不等于业务授权','不凭设计缺失新增 API、放开权限、删除校验或更改资金、认证及持久化语义。“跳过引导”不等于“跳过身份认证”。业务冲突只暂停相关依赖。')+code('使用 $figma-ui-restore。\n原型：[链接]；目标：[页面]。\n有产品连线、流程图或说明时按产品实现；\n没有定义的部分，自行分析现有代码与项目惯例，\n标注推导，并验证主路径及相关返回、取消和失败分支。',lang),'interactions')
  body+=section('离线资料与交接','<p>SVG、PNG、明确规格和数值也可作为输入。标清哪些是精确值、哪些是截图估计。长任务可使用仓库模板维护当前状态；局部修复不要求长任务文档。</p><p>工具权限、额度或字段缺失导致连线没读到时，记录具体障碍，尝试可用的授权原型面板或导出，继续处理已确认部分。不能把读取失败称为产品没有流程。</p>')
 else:
  intro='Choose the workflow by actual scope. Keep evidence and verification for large work, and small patches for focused fixes.'
  body=section('Full-page implementation','<p>Establish the specific node, target route, language and state. Read relevant properties, screenshots and original assets, then inspect existing components and data flow. Implement and verify one representative slice before expanding.</p><p>Separate design facts, inherited project behavior, implementation assumptions and approved differences. A component library’s defaults do not automatically match the reference.</p>'+code('Use $figma-ui-restore.\nDesign: [node]. Target: [route]. Running URL: [URL].\nRestore the page and its relevant dialog states.\nVerify one representative state before expanding;\npreserve existing components and business behavior.',lang),'full')
  body+=section('Focused visual fixes','<p>For specific typography, spacing, color, radius or control-size differences, locate related components and make a small patch. Reuse valid evidence rather than exporting the whole page or investigating unrelated business logic.</p><p>Verify the region and adjacent layout under matching conditions. Sample affected callers if a shared component changes; keep required repository checks.</p>'+code('Use $figma-ui-restore.\nFix only the typography, spacing and colors in [region].\nPreserve data, column widths and interactions.\nCompare local before/after screenshots;\ndo not turn this into a full-page rewrite.',lang),'focused')
  body+=section('Read-only UI audit','<p>Compare design and runtime; report expected/actual values, source, impact and likely code location. Deliver findings without editing application code, configuration or visual baselines.</p>'+code('Use $figma-ui-restore.\nCompare [running URL] with [design node].\nAudit only: report expected/actual values and impact.\nDo not change application files or visual baselines.',lang),'audit')
  body+=section('Interaction logic: establish product intent',flow_table(lang)+'<p>Read the element, event, condition, action and destination. Distinguish navigation, back, overlays, component states, scroll and conditional actions. Each prototype Frame does not need a new route.</p><p>For undefined behavior, analyze current routes, handlers, state and analogous approved interactions. Implement supported UI decisions and label their source. Partial specifications retain their defined edges.</p>'+callout('UI inference is not business authorization','Do not invent APIs, relax permissions, remove validation or change financial, authentication or persistence semantics. Skipping onboarding does not skip verification. Pause only the conflicting dependency.')+code('Use $figma-ui-restore.\nPrototype: [URL]. Target: [page].\nFollow product connections, flowcharts and specifications.\nAnalyze missing UI branches from current code and conventions.\nLabel inferences and verify the main path and affected\nback, cancel and failure branches.',lang),'interactions')
  body+=section('Offline evidence and handoff','<p>Authorized SVG, PNG and explicit specifications also work. Separate exact values from screenshot estimates. Optional task templates support long work; a focused fix needs no long task document.</p><p>Permission, quota or missing tool fields can leave reactions unreadable. Record the exact gap and use available authorized fallback evidence. Continue confirmed work without claiming the product supplied no flow.</p>')
 return article(lang,'workflows',intro,body)

def flow_table(lang):
 if lang=='zh': rows=[('已定义','遵循产品连线、流程图和明确说明。'),('部分定义','保留已有边，仅分析空缺分支。'),('没有定义','从现有实现和项目惯例推导 UI 行为。'),('尚未读取','记录缺口，未知不当作没有。')];heads=('证据状态','处理方式')
 else: rows=[('Defined','Follow product connections, flowcharts and specifications.'),('Partial','Preserve defined edges; analyze only missing branches.'),('Absent','Derive UI behavior from existing code and conventions.'),('Not yet read','Record the access gap. Unknown is not absent.')];heads=('Evidence status','Decision')
 return '<div class="table-scroll"><table><thead><tr>'+''.join(f'<th scope="col">{h}</th>' for h in heads)+'</tr></thead><tbody>'+''.join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a,b in rows)+'</tbody></table></div>'


def verification(lang):
 zh=lang=='zh'
 if zh:
  intro='“代码改好了”“视觉对上了”“交互跑通了”，是不同的结论。每一个通过，都应能对应实际证据。'
  body=section('01 / 锁定比较基线','<p>首次基准来自 Figma 或明确的离线规格。使用匹配的节点、状态、语言和视口，等待字体和布局稳定。浏览器回归截图只有在对照设计验收后，才能作为后续基准。</p><p>结构化属性优先于截图观感；颜色、字号和字重按具体文本或组件图层检查，不把父容器样式套给所有子层。</p>')
  body+=section('02 / 核对可见差异','<ol><li>布局、容器尺寸与可用宽度。</li><li>padding、gap、对齐和文本基线。</li><li>字体、字重、行高、图标与正式资产。</li><li>颜色、边框、圆角及打开、选中、禁用等相关状态。</li></ol><p>查看真实 computed style、换行、溢出和点击区域；纯代码声明或构建成功不能替代浏览器证据。</p>')
  body+=section('03 / 单独执行交互','<p>按流程表在真实运行页执行本次主路径及相关分支。记录起点、触发/条件、预期目标、实际结果与数据保留。按影响覆盖返回、关闭、取消、失败/重试、键盘焦点和刷新等行为。</p><p>读取原型连线不等于执行了应用流程。外部写操作仅使用已授权测试环境或现有 mock；无法执行的项明确写“未验证”，不为截图发送真实邀请、交易或权限变更。</p>')
  states=[('代码已修改','实际文件发生了相关变更。'),('检查通过','列出真实运行的命令和结果。'),('视觉已核对','说明设计来源、路由/区域、状态、视口和浏览器证据。'),('交互已执行','列出实际执行的路径、分支与预期/实际结果。'),('未验证','说明缺失工具、证据或环境及其影响。')]
  body+=section('04 / 如实报告结果','<dl class="result-list">'+''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a,b in states)+'</dl>')
  body+=section('原创演示：规格与实现',f'<p>下面的示例只演示三项样式差异。按钮用于切换显示状态，不会运行 Codex、读取 Figma 或发送邀请。</p>{demo(lang)}<p>需要实际练习，可使用仓库中的 <a href="{REPO}/tree/main/examples/offline-card">离线卡片练习</a>和 <a href="{REPO}/tree/main/examples/interaction-flows">交互决策情境</a>。</p>')
  body+=section('公开工具的验证范围',f'<p>安装器、拒绝覆盖、路径保护、元数据与打包已通过 macOS、Linux、Windows CI；Windows 的符号链接创建测试明确跳过。已有原创离线练习与受限范围的实时交互属性读取记录。</p><p>这些检查不代表所有客户端安装方式、模型或真实设计任务都已端到端验收。具体记录与限制以 <a href="{REPO}/blob/main/docs/verification.md">验证矩阵</a>和 <a href="{REPO}/actions">GitHub Actions</a> 为准。</p>'+callout('设计与客户资料保持私有','公开官网只使用通用规则和原创示例，不发布用户的私有 Figma 地址、节点标识、客户信息或设计截图。临时验收证据留在本地忽略目录或系统临时目录。'))
 else:
  intro='Code changed, visuals matched and interactions executed are different outcomes. Every passing claim should point to real evidence.'
  body=section('01 / Establish the reference','<p>First acceptance compares the running UI with Figma or an explicit offline specification. Match the node, state, language and viewport; wait for stable fonts and layout. Only an accepted browser result can become a later regression baseline.</p><p>Structured properties outrank screenshot appearance. Check semantic text and component layers rather than applying one parent style to every child.</p>')
  body+=section('02 / Inspect visible differences','<ol><li>Layout, container geometry and available width.</li><li>Padding, gaps, alignment and text baselines.</li><li>Typography, weight, line height, icons and original assets.</li><li>Colors, borders, radii and relevant open, selected or disabled states.</li></ol><p>Inspect computed styles, wrapping, overflow and click targets in the actual browser. Source declarations or a successful build do not replace visual evidence.</p>')
  body+=section('03 / Execute interactions separately','<p>Run the scoped main path and relevant branches in the real application. Record the start, trigger/condition, expected destination, actual outcome and retention. Include affected back, close/cancel, failure/retry, focus and refresh behavior.</p><p>Reading prototype edges does not execute the application flow. External writes need authorized test data or existing mocks. Mark unexecuted paths honestly; do not send real invitations, transactions or permission changes for screenshots.</p>')
  states=[('Code changed','Relevant application files were modified.'),('Checks passed','Name the commands actually run and their results.'),('Visually verified','Name the reference, route/region, state, viewport and browser evidence.'),('Interactions executed','List tested paths and branches with expected/actual outcomes.'),('Unverified','Name missing evidence, tools or environment and the practical limitation.')]
  body+=section('04 / Report precise outcomes','<dl class="result-list">'+''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a,b in states)+'</dl>')
  body+=section('Original demo: reference and implementation',f'<p>This teaching example illustrates three style differences. Its controls switch visual states; they do not run Codex, read Figma or send invitations.</p>{demo(lang)}<p>For practice, explore the <a href="{REPO}/tree/main/examples/offline-card">offline card exercise</a> and <a href="{REPO}/tree/main/examples/interaction-flows">interaction decision scenarios</a>.</p>')
  body+=section('What has actually been tested',f'<p>Installer behavior, overwrite refusal, path protection, metadata and packaging passed CI on macOS, Linux and Windows. Windows explicitly skips symlink creation. Original offline trials and a scoped live interaction-property read are recorded separately.</p><p>These checks do not prove every client, model or live design task works end to end. See the <a href="{REPO}/blob/main/docs/verification.md">verification matrix</a> and <a href="{REPO}/actions">GitHub Actions</a> for exact evidence and limitations.</p>'+callout('Private designs stay private','This public website uses generic rules and original examples. It does not publish users’ private Figma URLs, node identifiers, customer data or design screenshots. Temporary acceptance evidence stays in ignored local or system temporary directories.'))
 return article(lang,'verification',intro,body)


def article(lang,page,intro,body):
 d=LABELS[lang]
 sidebar=''.join(link(lang,p,d[p],'doc-link'+(' active' if p==page else '')) for p in PAGES[1:])
 nextpage=PAGES[(PAGES.index(page)+1)%len(PAGES)]
 next_link=link(lang,nextpage,d[nextpage]+" ↗")
 return f'<div class="wrap doc-layout"><aside class="doc-sidebar"><span class="eyebrow">{d["docs"]}</span><nav aria-label="{d["docs"]}">{sidebar}</nav><a class="source-link" href="{REPO}/releases">v{VERSION} ↗</a></aside><article class="article"><header class="article-head"><span class="eyebrow">FIGMA UI RESTORE / {page.upper()}</span><h1>{d[page]}</h1><p>{intro}</p></header>{body}<div class="doc-next"><span>{d["next"]}</span>{next_link}</div></article></div>'


def render(lang,page,body,notfound=False):
 d=LABELS[lang]; title,description=META[lang][page]
 url=BASE+'/'+path(lang,page)
 other='en' if lang=='zh' else 'zh'
 nav=''.join(link(lang,p,d[p],'nav-link'+(' current' if p==page else '')) for p in PAGES[1:])
 alternate=''.join(f'<link rel="alternate" hreflang="{l}" href="{BASE}/{path(k,page)}">' for k,l in [('zh','zh-Hans'),('en','en')])+f'<link rel="alternate" hreflang="x-default" href="{BASE}/{path("zh",page)}">'
 graph=[{'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':'Figma UI Restore','inLanguage':['zh-Hans','en']},{'@type':'SoftwareSourceCode','@id':BASE+'/#software','name':'Figma UI Restore','description':description,'codeRepository':REPO,'license':REPO+'/blob/main/LICENSE','version':VERSION,'author':{'@type':'Person','name':'fukuang-dev','url':'https://github.com/fukuang-dev'}},{'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':description,'inLanguage':'zh-Hans' if lang=='zh' else 'en','isPartOf':{'@id':BASE+'/#website'},'about':{'@id':BASE+'/#software'}}]
 if page!='home':graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':d['home'],'item':BASE+'/'+path(lang)},{'@type':'ListItem','position':2,'name':d[page],'item':url}]})
 structured = json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</','<' + chr(92) + '/')
 return f'''<!doctype html>
<html lang="{'zh-CN' if lang=='zh' else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc('404 — Figma UI Restore' if notfound else title)}</title><meta name="description" content="{esc(description)}"><meta name="robots" content="{'noindex,follow' if notfound else 'index,follow,max-image-preview:large'}"><meta name="theme-color" content="#f6f5f0">
{'' if notfound else f'<link rel="canonical" href="{url}">{alternate}'}
<meta property="og:type" content="website"><meta property="og:site_name" content="Figma UI Restore"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{url}"><meta property="og:locale" content="{'zh_CN' if lang=='zh' else 'en_US'}"><meta property="og:image" content="{BASE}/assets/social.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Figma UI Restore — Evidence first. Browser verified."><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{BASE}/assets/social.png">
<link rel="icon" href="{PREFIX}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{PREFIX}assets/styles.css"><script src="{PREFIX}assets/app.js" defer></script><script type="application/ld+json">{structured}</script></head>
<body><a class="skip-link" href="#main">{d['skip']}</a><header class="site-header"><div class="wrap nav-inner"><a class="brand" href="{local(lang)}" aria-label="Figma UI Restore / {d['home']}"><span class="brand-symbol" aria-hidden="true">f<span>↗</span></span><span>Figma UI Restore<span class="brand-dot">.</span></span></a><button class="menu-toggle" type="button" aria-label="{d['menu']}" aria-expanded="false" aria-controls="site-nav"><span aria-hidden="true">☰</span></button><nav id="site-nav" class="site-nav" aria-label="{'主导航' if lang=='zh' else 'Main navigation'}">{nav}<span class="nav-divider"></span><a class="lang-link" href="{local(other,page)}" lang="{other}" hreflang="{'en' if other=='en' else 'zh-Hans'}">{d['lang']}</a><a class="nav-github" href="{REPO}" aria-label="GitHub">GitHub ↗</a></nav></div></header>
<main id="main">{body}</main><footer class="site-footer"><div class="wrap footer-top"><div><a class="brand" href="{local(lang)}">Figma UI Restore<span class="brand-dot">.</span></a><p>{d['footer']}</p></div><nav aria-label="{'页脚导航' if lang=='zh' else 'Footer'}">{link(lang,'install',d['install'])}{link(lang,'verification',d['verification'])}<a href="{REPO}/releases">Releases ↗</a><a href="{REPO}/issues">{'反馈问题' if lang=='zh' else 'Report an issue'} ↗</a></nav></div><div class="wrap footer-bottom"><span>© 2026 <a href="https://github.com/fukuang-dev">fukuang-dev</a> · <a href="{REPO}/blob/main/LICENSE">MIT License</a></span><span>{d['legal']}</span></div></footer><div class="sr-only" id="copy-status" role="status" aria-live="polite"></div></body></html>'''


def build(base_url):
 global BASE,PREFIX
 parsed=urlparse(base_url)
 if parsed.scheme!='https' or not parsed.netloc or parsed.query or parsed.fragment:raise ValueError('Use an absolute HTTPS base URL without query/fragment')
 BASE=base_url.rstrip('/');PREFIX=parsed.path.rstrip('/')+'/'
 if OUT.exists():shutil.rmtree(OUT)
 OUT.mkdir(parents=True)
 shutil.copytree(ROOT/'website/assets',OUT/'assets')
 for lang in LABELS:
  for page,fn in [('home',home),('install',install),('workflows',workflows),('verification',verification)]:
   target=OUT/path(lang,page)/'index.html';target.parent.mkdir(parents=True,exist_ok=True)
   target.write_text(render(lang,page,fn(lang)),encoding='utf-8')
 missing=f'<section class="wrap section not-found"><span class="eyebrow">404 / PAGE NOT FOUND</span><h1>这页走丢了。<br>This page is missing.</h1><p>请从首页继续，或在 GitHub 报告失效链接。<br>Start from home, or report a broken link on GitHub.</p>{link("zh","home","返回首页 / Back home ↗","button primary")}</section>'
 (OUT/'404.html').write_text(render('zh','home',missing,notfound=True),encoding='utf-8')
 ns='http://www.sitemaps.org/schemas/sitemap/0.9'
 import xml.etree.ElementTree as ET
 ET.register_namespace('',ns);xml=Element('{'+ns+'}urlset')
 for lang in LABELS:
  for page in PAGES:SubElement(SubElement(xml,'{'+ns+'}url'),'{'+ns+'}loc').text=BASE+'/'+path(lang,page)
 ElementTree(xml).write(OUT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
 (OUT/'.nojekyll').write_text('',encoding='utf-8')
 print(f'Built 8 localized pages, 404, sitemap and local assets: {OUT}')

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--base-url',default='https://fukuang-dev.github.io/figma-ui-restore')
 build(parser.parse_args().base_url)
