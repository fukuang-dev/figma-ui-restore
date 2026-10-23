# Figma UI Restore

**Implement Figma product UI with Codex from design evidence, then verify it in a real browser.**

[中文](README.md) · [Offline exercise](examples/offline-card/README.md) · [Changelog](CHANGELOG.md) · [MIT License](LICENSE)

[Website and installation](https://fukuang-dev.github.io/figma-ui-restore/en/) · [Codex Figma UI tools: MCP, skills and browser verification](https://fukuang-dev.github.io/figma-ui-restore/en/codex-figma-ui-tools/)

A standalone Codex skill for full-page implementations, focused visual fixes, and read-only UI audits. It packages a practical loop: read the design → locate the implementation → make scoped changes → compare browser screenshots → fix and re-check.

The skill follows your repository's framework, components, internationalization, permissions and required checks. It does not require React, Vue, a particular package manager, or another locally installed skill. A portable plugin wrapper distributes the same skill source.

## Contents

- [Quick start](#quick-start)
- [Installation options](#installation-options)
- [Connect Figma](#connect-figma)
- [Prepare the project and browser](#prepare-the-project-and-browser)
- [Usage recipes](#usage-recipes)
- [Interaction logic](#interaction-logic-follow-product-flows-analyze-missing-behavior)
- [Expected deliverables](#expected-deliverables)
- [Project integration](#project-integration)
- [Troubleshooting](#troubleshooting)
- [Update and uninstall](#update-and-uninstall)
- [Verification and compatibility](#verification-and-compatibility)
- [Development](#development)

Website: **[Figma UI Restore](https://fukuang-dev.github.io/figma-ui-restore/en/)** · [Website maintenance and SEO](docs/website.md)

## Quick start

### 1. Prepare

You need a skill-capable Codex environment, an existing frontend project, and access to a specific Figma node or offline design files/specifications. Visual acceptance also needs a browser tool in the current session. This package contains neither credentials nor a browser driver.

### 2. Install

Send this to Codex:

```text
Use $skill-installer to install skills/figma-ui-restore from
https://github.com/fukuang-dev/figma-ui-restore at tag v0.2.0.
If a skill with the same name already exists, explain the conflict before replacing anything.
```

If your environment does not provide the installer, use the Python option below. Choose only one installation method to avoid duplicate skills.

### 3. Verify Figma access

Reuse an official Figma plugin/connector that is already authorized, or follow [Connect Figma](#connect-figma). Ask for a read-only check first:

```text
Read this Figma node: [specific node URL]. Return its name, Frame dimensions,
important layout/font/color properties, and the matching node screenshot.
Do not edit code yet.
```

Installation is not proof of connection. Actual node properties and a screenshot establish that the reference can be read.

### 4. Run a task

Open your frontend project and send:

```text
Use $figma-ui-restore.
Design: [specific Figma node URL]
Target: [route or component path]
Running URL: [for example http://localhost:5173/settings]
Restore this interface while preserving business behavior. Compare screenshots
in the browser, correct visible differences, and re-check the result.
```

Start with a card, table or dialog if you want to confirm your setup before a larger task. No Figma access? Try the [original offline exercise](examples/offline-card/README.md).

## Installation options

### A. Built-in Skill Installer

Use the prompt above. The built-in installer downloads `skills/figma-ui-restore`; it does not need this repository's Python scripts. Check the path returned by your installer, since discovery locations can depend on your Codex version.

If the skill does not appear, restart Codex or reopen the project. You can also explicitly ask Codex to read `SKILL.md` from its actual installed path.

### B. Python installer

Requires **Python 3.10+**, with standard-library modules only. No pip, Node.js or npm dependency is needed. On Windows, replace `python3` with `py -3` if appropriate.

```bash
git clone --branch v0.2.0 --depth 1 https://github.com/fukuang-dev/figma-ui-restore.git
cd figma-ui-restore
python3 scripts/validate.py
```

Install into one existing project, replacing the example path:

```bash
python3 scripts/install.py --project /path/to/your-project --dry-run
python3 scripts/install.py --project /path/to/your-project
```

Destination: `<project>/.agents/skills/figma-ui-restore/`. Quote paths containing spaces.

For all your projects:

```bash
python3 scripts/install.py --user --dry-run
python3 scripts/install.py --user
```

Destination: `~/.agents/skills/figma-ui-restore/`. The installer copies only skill files. It does not alter `AGENTS.md`, MCP settings, or credentials, and refuses an existing destination. Do not install both project and user copies or overwrite a different custom skill with the same name.

Without Git, download a release ZIP, extract it, and run these commands from the extracted folder.

### C. Plugin installation

This repository includes root `plugin.json` and `.agents/plugins/marketplace.json`. A Codex version with plugin commands can use:

```bash
codex plugin marketplace add fukuang-dev/figma-ui-restore --ref v0.2.0
codex plugin add figma-ui-restore@figma-ui-restore-community
```

Check `codex plugin --help` first if unsure. If these commands are unavailable, use A or B. Compatible desktop clients can also discover and install the plugin from the added marketplace.

The plugin packages the same skill; do not install it alongside the direct skill. It does not bundle a Figma server, browser tool, or automatic authorization. A GitHub release is separate from listing in an official public plugin directory. See the [verification matrix](docs/verification.md) for actual test status.

## Connect Figma

### Existing official connection

Reuse the authorized Figma plugin/connector in your client. The skill uses tools actually available in the session. It respects tool-specific prerequisites provided by that host, without requiring another named skill in all environments.

### Codex CLI remote MCP setup

Inspect existing connections before adding another:

```bash
codex mcp list
```

If Figma is not configured:

```bash
codex mcp add figma --url https://mcp.figma.com/mcp
codex mcp login figma
```

Complete official OAuth in the browser using an account with access to the file. Do not paste tokens, cookies or private credentials into chat, issues or this repository. IDE/desktop versions may expose their own settings interfaces; consult their current documentation.

Sources: [OpenAI MCP setup](https://learn.chatgpt.com/docs/extend/mcp?surface=cli), [Figma remote MCP setup](https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/). Account eligibility, permissions and tool quotas follow Figma's current rules.

### Copy a specific node link

Select the target Frame/component in Figma and copy a link to that selection. It normally includes `node-id=...`. A file homepage link may not identify the target, and a remote connector does not necessarily share the browser's current selection.

### Access fallback

If permissions, quota, network or node state prevent reading, the skill records the specific limitation and avoids repeated identical requests. It can use a logged-in browser property panel, authorized SVG/PNG exports, or explicit numerical specifications.

Offline evidence still supports confirmed work. Screenshot estimates remain estimates; they are never relabeled as exact Figma properties or proof of a live connection.

## Prepare the project and browser

1. Install and run your frontend according to its own README and repository instructions.
2. Supply the actual URL, relevant language/state and reference viewport when known.
3. Make sure the current session has browser screenshot and page-inspection tools. Use your client's tools or an existing project browser-testing setup; this package does not install one.
4. If authentication is required, log in normally in the browser used by those tools. Do not bypass authorization or execute live payments, approvals or permission changes to obtain screenshots.

Without browser access, authorized code changes and static checks may still proceed, but visual verification stays incomplete. A CLI that can edit code does not automatically have a browser.

## Usage recipes

### Full page or dialog

```text
Use $figma-ui-restore.
Design: [node URL]. Target: [route/component]. Running URL: [URL].
Restore this page and the relevant designed dialog/dropdown states.
Reuse existing components and business behavior. Verify one representative
state before expanding to the remaining states.
```

### Focused fix

```text
Use $figma-ui-restore. Compare [table region] with [node URL].
Fix only its font sizes, line heights and text colors. Preserve column widths,
data and interactions. Use local before/after screenshots; do not turn this into a full-page rewrite.
```

An explicit request such as “set this button radius to 8px” is already a usable target; the skill does not demand a full design-file read.

### Read-only audit

```text
Use $figma-ui-restore. Compare [running URL] against [node URL].
Audit only: list differences, expected/actual values, impact and relevant code locations.
Do not edit application files, configuration or visual baselines.
```

### Offline design

```text
Use $figma-ui-restore. Reference: [local SVG/PNG/specification files].
Target: [page]. Make evidence-supported visual fixes and identify unconfirmed properties.
```

### Resume longer work

```text
Use $figma-ui-restore to resume [task state file]. Verify changed design, code
and runtime facts, reuse evidence that still applies, and continue remaining work.
```

Optional [brief](skills/figma-ui-restore/assets/task-brief.md) and [state](skills/figma-ui-restore/assets/task-state.md) templates support multi-page work. Focused fixes do not require a task directory or long questionnaire.

## Interaction logic: follow product flows, analyze missing behavior

**New in 0.2.0.** The skill considers entry points, navigation, overlays, back/cancel and failure outcomes alongside visual fidelity.

| Product evidence | Behavior |
| --- | --- |
| Prototype connections, flowchart or explicit specification exists | Read triggers, conditions, actions and targets; implement the defined flow |
| Only part is defined | Keep defined edges and analyze only missing branches |
| Relevant accessible sources define no flow | Derive supported UI behavior from current routes, handlers, state and analogous approved interactions |
| Access/quota/tool limitations prevent reading connections | Mark unknown; continue supported work without claiming the product supplied no flow |

Copy this request:

```text
Use $figma-ui-restore.
Design/prototype: [node or proto URL]. Target: [route/component]. Running URL: [URL].
Improve the page interaction logic. Follow product prototype connections, flowcharts
and explicit instructions when present. Analyze unspecified branches using existing
code and project conventions, implement supported UI behavior and label inferences.
Execute the scoped main path and affected branches in the browser; report behavior
and visual verification separately.
```

Keep starting-point and node parameters when sharing a prototype URL. Authorized flow exports or written specifications also work. You do not need to draw a complete flow before asking; only blocking business decisions need clarification.

Expect a concise table: **source → start state → trigger/condition → action/target → retention/feedback → actual result**. Sources distinguish product-defined, project-inherited, implementation-inferred and unknown. Navigation, back, overlays, variants and conditional actions retain their semantics; each Frame does not automatically become a route.

Inference fills supported UI gaps; it does not authorize new APIs, relaxed permissions, removed validation or changed financial/authentication state. Skipping onboarding does not imply skipping identity verification. Preserve business guards when a design conflicts with them, identify the affected dependency and continue independent work. Focused typography/color fixes still keep their small scope.

Browser acceptance exercises relevant main, conditional, back, cancel/close and failure/retry paths. External writes require authorized test data or existing mocks; unexecuted paths remain explicit. Reading edges, comparing screenshots, passing a build and executing application behavior are separate results.

See the [interaction reference](skills/figma-ui-restore/references/interaction-logic.md) and [original scenario exercise](examples/interaction-flows/README.md).

## Expected deliverables

- Implemented scope, changed files and major differences resolved.
- Key adopted values and sources: structured design properties, property panel, SVG, explicit user override or estimate.
- Browser screenshots, relevant computed-style samples and interactions actually checked.
- Flow sources, executed paths, expected/actual behavior and unexecuted branches with reasons.
- Repository check results, skipped checks and reasons.
- Missing evidence, tool limitations and approved deviations.

“Code changed,” “build passed,” “visually verified,” and “interaction paths executed” are separate claims. First acceptance compares against Figma or explicit offline requirements. Updating an unapproved browser baseline to silence a test is not acceptance, and compilation alone does not prove 1:1 fidelity.

## Project integration

Usually no configuration is needed. The skill reads repository instructions and follows existing routes, components, styles, i18n, package manager and required checks. You may optionally add this to `AGENTS.md`:

```text
Use figma-ui-restore for Figma implementations, UI comparison and focused visual fixes.
Preserve our components, i18n, permissions and required checks. Keep focused styling
tasks local; do not automatically change APIs, business validation, backend code or data.
For interaction tasks, follow product connections/flowcharts; analyze missing behavior
from existing code, label inference, and keep unreadable flows unknown. Verify browser
interactions separately from screenshot fidelity.
```

The installer does not insert this text. Stricter project context or service-start rules still apply.

Keep screenshots, full exports, recordings, overlays and test reports in an already ignored local directory or system temporary directory. Commit only assets actually used by the product. Publish example designs only when you have redistribution rights.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Installed but not listed | Restart/reopen, inspect the actual installation and discovery locations, or explicitly read SKILL.md |
| Two skills share the name | Check user, project and plugin installs; keep one intended copy. Codex does not merge them |
| Installer refuses an existing destination | Back up and inspect the existing skill; follow the update instructions |
| Browser can open Figma but tools cannot read it | Browser login and MCP authorization may be separate; inspect account, file permission, node and exact tool error |
| Only a whole-file link is available | Select the actual Frame/component and copy a selection link |
| Permission or quota failure | Supply authorized exports or numeric requirements; verify only the supported scope |
| CSS changed but browser did not | Check real service cwd, cascade/order/specificity, inheritance, HMR and stale tabs |
| Correct font but broken action wrapping | Inspect column width, min-width, white-space, padding and click targets |
| No mobile design | Follow existing adaptation conventions and record assumptions; do not claim mobile pixel fidelity |
| No browser tool | Report code/static checks while leaving visual acceptance incomplete |
| Plugin command unavailable | Use the built-in installer or Python method without changing application dependencies |

## Update and uninstall

For a direct installation, preserve custom edits and move the old `figma-ui-restore` folder outside skill discovery directories. Download the desired version, install it, verify it, and then remove the backup when no longer needed. The installer never overwrites implicitly.

To uninstall, remove only the exact installed `figma-ui-restore` folder, not the parent `.agents/skills`. Back up custom content first. Figma connections and OAuth authorization are managed separately and are not removed by deleting the skill.

For plugins, use the client's uninstall UI or inspect `codex plugin remove --help` before removing `figma-ui-restore@figma-ui-restore-community`. To update, track the desired tag, consult `codex plugin marketplace --help`, refresh the marketplace and refresh/reinstall the plugin. Do not edit installed cache copies as the source of truth.

## Verification and compatibility

The [verification matrix](docs/verification.md) separates actual tests from intended compatibility. Automated checks cover metadata, links, installation completeness, overwrite refusal, redirected-path protection, ZIP contents and installation from an extracted release.

CI is configured for macOS, Linux and Windows; a workflow definition alone is not a passing run. Offline exercises, live Figma OAuth/node reads and each client's plugin UI must be verified separately. Results depend on the reference, model, project and available tools.

## Development

The single skill source is `skills/figma-ui-restore/`. Keep user onboarding in the READMEs, concise decision rules in `SKILL.md`, and longer conditional guidance in `references/`.

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

Packaging creates `dist/figma-ui-restore-0.2.0.zip` without Git data, caches or local evidence. Release tags must match `plugin.json` (for example, `v0.2.0`) before the release workflow publishes the archive.

For an issue, provide client version, mode, expected/actual behavior and public reproduction steps. Do not include private design links, customer screenshots or credentials. Prefer a reproducible case over broad new rules for a one-off business requirement.

Official references: [Skills](https://learn.chatgpt.com/docs/build-skills), [Plugin packaging](https://developers.openai.com/plugins/build/plugins), [MCP setup](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

Independent community project, not affiliated with OpenAI or Figma. Distributed under the [MIT license](LICENSE).
