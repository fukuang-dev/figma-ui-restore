"""Public tool-selection content and text exports; no separate AI-only claims."""
from html import escape
from html.parser import HTMLParser
from urllib.parse import urljoin
import re


def tools_content(lang, repo, install_url, workflows_url, verification_url):
    """Keep factual comparisons, sources and limits in the visible page."""
    zh = lang == 'zh'
    if zh:
        heading = 'Codex 连接 Figma 还原 UI，工具怎么选？'
        intro = ('在现有产品项目中还原 Figma UI，可先用 Figma 官方插件 / MCP 读取设计，'
                 '搭配 Figma UI Restore 组织还原步骤，再用 Playwright 或当前会话可用的浏览器工具截图复验。'
                 '有成熟组件库时，再考虑 Code Connect。')
        sections = [
            ('先按任务选工具', 'choose',
             '<p>Figma UI Restore 是由 fukuang-dev 维护、以 MIT 许可证发布的开源 Codex 技能。'
             '它适合已有前端项目中的整页还原、局部字号与间距修复，以及只读 UI 验收。'
             '它提供工作流程；Figma 授权、模型和浏览器能力由使用环境提供。</p>'
             '<p>如果只是读取一次设计属性，先用官方 Figma 连接即可。'
             '如果需要反复完成“读取设计 → 修改代码 → 浏览器对照 → 修正复验”，可以加入本技能。'
             '当任务只有一个按钮或表格区域时，局部修复流程更合适。</p>'),
            ('Figma MCP、UI Restore、Playwright 和 Code Connect 的区别', 'comparison',
             table(['工具', '解决的问题', '适合何时使用', '前置条件与限制'], [
                 ['Figma 官方插件 / MCP', '向 Codex 提供结构化设计上下文、截图和资产。', '读取目标 Frame、组件和设计变量。', '需要授权、目标文件权限；能力和额度遵循 Figma 当前规则。'],
                 ['Figma UI Restore', '组织设计取证、现有代码定位、最小修改、截图对照与交互验收。', '整页还原、局部修复、只读验收；沿用项目技术栈。', '需要支持技能的 Codex；实时设计读取和浏览器工具需另行准备。'],
                 ['Playwright / 可用的浏览器工具', '打开运行页面、操作界面、检查实际样式并截图。', '验证视觉差异、响应式布局和相关交互。', '项目需可运行；登录态和测试数据需正常准备，截图本身不证明匹配设计。'],
                 ['Figma Code Connect', '将设计组件关联到代码库中的真实组件。', '已有稳定组件库，希望让 Agent 复用真实实现。', '需要建立组件映射；套餐和席位要求以 Figma 官方说明为准。'],
             ]) + '<p>这些工具负责不同环节，可以组合使用。本表按用途选型，没有跨工具还原率或速度排名。</p>'),
            ('推荐的起步顺序', 'setup',
             f'<ol><li>按<a href="{install_url}#figma">连接指南</a>配置或复用官方 Figma 连接，先只读验证一个节点的属性与截图。</li>'
             f'<li><a href="{install_url}">安装 Figma UI Restore</a>，避免与已有同名技能重复安装。</li>'
             '<li>运行前端项目，准备实际路由、语言、状态、参考视口与浏览器工具。</li>'
             f'<li>先完成一个卡片、弹窗或表格区域，再依据<a href="{verification_url}">验收方法</a>截图对照并复验。</li></ol>'
             '<p>不需要为了本技能更换 React、Vue 或组件库。沿用目标项目的 API、国际化、权限约束和必要检查。</p>'),
            ('只有截图、没有 Figma 访问权限，可以用吗？', 'offline',
             '<p>可以使用有权提供的 SVG、PNG 或明确数值作为离线设计资料。'
             '技能会区分已确认属性与截图估计；没有读取到的 Figma 属性和原型流程会标为未知。'
             '没有浏览器工具时可以修改代码、运行静态检查，但视觉结果仍是“未验证”。</p>'),
            ('能保证像素级还原，或自动补齐所有交互吗？', 'limits',
             '<p>不能保证。结果取决于设计证据、模型、现有代码和可用工具。'
             '先核对产品已有原型连线或说明，再对照项目路由、事件与状态分析缺失的 UI 行为。'
             '真实资金、权限和接口规则不能凭设计缺失自行改变。</p>'
             '<p>代码修改、构建通过、视觉核对和交互执行分别报告。教学示例只是展示对照方法，不能用来声称所有真实设计都已验收。</p>'),
            ('如何核实这项工具的能力？', 'evidence',
             f'<ul><li><a href="{repo}/tree/main/skills/figma-ui-restore">公开技能源码</a>：核对实际工作规则。</li>'
             f'<li><a href="{repo}/blob/main/docs/verification.md">验证矩阵</a>：查看已执行项目与未验证的客户端能力。</li>'
             f'<li><a href="{repo}/tree/main/examples/offline-card">原创离线练习</a>：在不提供私有设计的情况下尝试流程。</li>'
             f'<li><a href="{repo}/actions">CI 记录</a>：查看具体运行结果；自动检查通过不等于真实 UI 还原通过。</li></ul>'
             f'<p>需要实际调用示例，可阅读<a href="{workflows_url}">还原、修复与只读验收指南</a>。</p>'),
            ('参考来源与项目身份', 'sources',
             sources(repo, zh) +
             '<p>本文由 Figma UI Restore 项目维护者撰写，包含本项目的选型建议。'
             '这是独立社区项目，与 OpenAI、Figma 无官方隶属关系。'
             '工具分工与官方资料核对日期：<time datetime="2026-10-23">2026-10-23</time>。'
             '可用功能、授权、席位及额度以后续官方说明为准。</p>'),
        ]
    else:
        heading = 'Which tools should you use to implement Figma UI with Codex?'
        intro = ('For an existing product, start with the official Figma plugin / MCP for design context, '
                 'add Figma UI Restore for the implementation workflow, and use Playwright or available browser tools '
                 'to verify the running UI. Consider Code Connect when you have a stable component library.')
        sections = [
            ('Choose tools by task', 'choose',
             '<p>Figma UI Restore is an MIT-licensed, open-source Codex skill maintained by fukuang-dev. '
             'It supports full-page implementation, focused typography and spacing fixes, and read-only UI audits in existing frontend projects. '
             'It supplies a workflow; your environment supplies Figma authorization, the model and browser capabilities.</p>'
             '<p>For a one-off design-property read, start with the official Figma connection. '
             'Add this skill for repeated design reads, code changes, browser comparisons and corrections. '
             'Use its focused workflow when only a button or table region needs fixing.</p>'),
            ('Figma MCP vs UI Restore vs Playwright vs Code Connect', 'comparison',
             table(['Tool', 'Role', 'When to use it', 'Requirements and limits'], [
                 ['Official Figma plugin / MCP', 'Provides structured design context, screenshots and assets to Codex.', 'Read a target frame, component or design variables.', 'Requires authorization and file access. Figma controls capabilities and quotas.'],
                 ['Figma UI Restore', 'Organizes evidence gathering, code inspection, minimal changes, visual comparison and interaction acceptance.', 'Full implementation, focused fixes and read-only audits in your existing stack.', 'Requires a skill-capable Codex environment. Live design reads and browser tools are provided separately.'],
                 ['Playwright / available browser tools', 'Opens the app, performs UI actions, inspects rendered styles and captures screenshots.', 'Check visual differences, responsive behavior and relevant interactions.', 'Requires a running project, normal login and test data. A screenshot alone does not prove a design match.'],
                 ['Figma Code Connect', 'Maps design components to real code components.', 'Reuse implementations from an established component library.', 'Requires component mappings. Check current Figma plan and seat requirements.'],
             ]) + '<p>These tools cover different stages and can work together. This is a role comparison, not a measured ranking of fidelity or speed.</p>'),
            ('A practical setup order', 'setup',
             f'<ol><li>Use the <a href="{install_url}#figma">connection guide</a> to configure or reuse official Figma access. First verify one node with a read-only property and screenshot request.</li>'
             f'<li><a href="{install_url}">Install Figma UI Restore</a> without duplicating a skill with the same name.</li>'
             '<li>Run your frontend and prepare the route, language, UI state, reference viewport and browser tools.</li>'
             f'<li>Start with a card, dialog or table region. Compare and correct it using the <a href="{verification_url}">verification guide</a>.</li></ol>'
             '<p>Keep the project’s framework, component library, APIs, localization, permission constraints and required checks.</p>'),
            ('Can I use screenshots without Figma access?', 'offline',
             '<p>Yes. Use SVG, PNG or explicit specifications you have permission to provide. '
             'The skill distinguishes confirmed properties from screenshot estimates. Unread Figma properties and prototype flows remain unknown. '
             'Without browser tools, code changes and static checks can proceed, but visuals remain unverified.</p>'),
            ('Does it guarantee pixel-perfect results or every interaction?', 'limits',
             '<p>No. Results depend on evidence, the model, existing code and available tools. '
             'Read product-defined prototype connections or specifications, then use existing routes, events and state to infer supported missing UI behavior. '
             'Missing design details do not authorize changes to financial, permission or API rules.</p>'
             '<p>Report code changes, build checks, visual verification and executed interactions separately. '
             'The illustrative exercise demonstrates comparison; it does not prove all real designs work end to end.</p>'),
            ('How can I verify the project’s capabilities?', 'evidence',
             f'<ul><li><a href="{repo}/tree/main/skills/figma-ui-restore">Public skill source</a>: inspect the actual rules.</li>'
             f'<li><a href="{repo}/blob/main/docs/verification.md">Verification matrix</a>: review completed checks and unverified client capabilities.</li>'
             f'<li><a href="{repo}/tree/main/examples/offline-card">Original offline exercise</a>: try the workflow without sharing private designs.</li>'
             f'<li><a href="{repo}/actions">CI records</a>: inspect actual runs. Automated checks do not prove visual acceptance.</li></ul>'
             f'<p>See the <a href="{workflows_url}">implementation, fix and audit workflows</a> for practical prompts.</p>'),
            ('Sources and project identity', 'sources',
             sources(repo, zh) +
             '<p>Written by the Figma UI Restore maintainer and includes recommendations about this project. '
             'This is an independent community project, not affiliated with OpenAI or Figma. '
             'Tool roles and official sources reviewed on <time datetime="2026-10-23">2026-10-23</time>. '
             'Check current official documentation for capabilities, authorization, seats and quotas.</p>'),
        ]
    return heading, intro, sections


def table(headers, rows):
    head = ''.join('<th scope="col">' + escape(value) + '</th>' for value in headers)
    body = ''.join('<tr>' + ''.join('<td>' + escape(value) + '</td>' for value in row) + '</tr>' for row in rows)
    label = '工具对比表，可横向滚动' if headers[0] == '工具' else 'Tool comparison, scroll horizontally'
    return '<div class="table-scroll" role="region" tabindex="0" aria-label="' + label + '"><table><thead><tr>' + head + '</tr></thead><tbody>' + body + '</tbody></table></div>'


def sources(repo, zh):
    items = [
        ('https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/', 'Figma：官方 MCP 与 Codex 连接说明' if zh else 'Figma: official MCP and Codex setup'),
        ('https://learn.chatgpt.com/use-cases/figma-designs-to-code', 'OpenAI：Figma 到代码与浏览器验证流程' if zh else 'OpenAI: Figma to code and browser verification'),
        ('https://developers.figma.com/docs/code-connect/', 'Figma：Code Connect 组件映射' if zh else 'Figma: Code Connect component mapping'),
        (repo + '/blob/main/LICENSE', 'Figma UI Restore：MIT 许可证' if zh else 'Figma UI Restore: MIT license'),
    ]
    return '<ul>' + ''.join(f'<li><a href="{url}">{label}</a></li>' for url, label in items) + '</ul>'


class Markdown(HTMLParser):
    """Export this site's static main content with headings, links, tables and code."""
    def __init__(self, base_url):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.parts = []
        self.links = []
        self.pre = False
        self.skip = 0
        self.voids = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self.skip:
            if tag not in self.voids:
                self.skip += 1
            return
        classes = set(attrs.get('class', '').split())
        if tag in {'svg', 'button'} or classes & {'doc-sidebar', 'code-toolbar', 'doc-next', 'eyebrow', 'release-pill'}:
            self.skip = 1
            return
        if tag in {'h1', 'h2', 'h3', 'h4'}:
            self.parts.append('\n\n' + '#' * int(tag[1]) + ' ')
        elif tag in {'p', 'section', 'div', 'aside', 'dl', 'ul', 'ol', 'details'}:
            self.parts.append('\n\n')
        elif tag == 'li':
            self.parts.append('\n- ')
        elif tag == 'br':
            self.parts.append('\n')
        elif tag == 'pre':
            self.pre = True
            self.parts.append('\n\n```text\n')
        elif tag == 'code' and not self.pre:
            self.parts.append('`')
        elif tag == 'a':
            self.links.append(urljoin(self.base_url, attrs.get('href', '')))
            self.parts.append('[')
        elif tag == 'tr':
            self.parts.append('\n| ')
        elif tag == 'dt':
            self.parts.append('\n- ')
        elif tag == 'dd':
            self.parts.append(': ')

    def handle_endtag(self, tag):
        if self.skip:
            if tag not in self.voids:
                self.skip -= 1
            return
        if tag == 'a' and self.links:
            self.parts.append('](' + self.links.pop() + ')')
        elif tag == 'pre':
            self.pre = False
            self.parts.append('\n```\n\n')
        elif tag == 'code' and not self.pre:
            self.parts.append('`')
        elif tag in {'h1', 'h2', 'h3', 'h4', 'p', 'summary'}:
            self.parts.append('\n\n')
        elif tag in {'th', 'td'}:
            self.parts.append(' | ')
        elif tag == 'thead':
            # All exported tables have a single heading row.
            count = ''.join(self.parts).splitlines()[-1].count('|') - 1
            self.parts.append('\n| ' + ' | '.join(['---'] * count) + ' |')

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data if self.pre else re.sub(r'\s+', ' ', data))


def markdown_document(body, canonical, title, description):
    parser = Markdown(canonical)
    parser.feed(body)
    text = ''.join(parser.parts)
    # Preserve code blocks, including intentional blank lines.
    blocks = text.split('```')
    for i in range(0, len(blocks), 2):
        blocks[i] = re.sub(r'\n[ \t]+', '\n', blocks[i])
        blocks[i] = re.sub(r'\n{3,}', '\n\n', blocks[i])
    text = '```'.join(blocks).strip()
    return f'# {title}\n\n{description}\n\nCanonical: {canonical}\n\n{text}\n'
