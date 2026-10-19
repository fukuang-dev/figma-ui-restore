---
name: figma-ui-restore
description: "Implement or verify an existing Figma design in a frontend project, or fix specific visual differences in typography, spacing, alignment, colors, icons, and controls. Use for UI 还原、还原 Figma、高保真还原、像素级还原、对照设计稿、UI 验收. Supports full implementation, focused fixes, and read-only audits; not free-form design or backend-only work."
---

# Figma UI Restore

Use the supplied design as the visual baseline and the running browser as the verification target. Preserve business behavior and make the smallest changes needed for the requested result. Respond in the user's language.

## Choose the scope

| Actual request | Workflow |
| --- | --- |
| One or a few specific font, spacing, alignment, color, radius, icon, or control-size differences | **Focused fix:** use the short workflow below |
| A whole page, several pages, a first implementation, or layout differences across regions/states | **Full restore:** read [full-restore.md](references/full-restore.md) |
| Review, compare, list differences, or audit without changing code | **Read-only audit:** collect relevant evidence and report differences; do not edit application code, snapshots, dependencies, or project configuration |
| Discuss an approach or explain a design | Answer the question; do not start implementation |

Judge actual scope rather than keywords: a "quick" whole-page implementation still needs the full workflow. State the selected mode briefly; do not ask users to select a mode when the scope is clear. Respect an explicit read-only request.

## Shared rules

- Read applicable repository instructions and check existing changes. Locate the actual route/component and reuse its architecture, components, i18n, accessibility, and design system. Identify the repository's real package manager and required checks; no framework, directory, or command is hardcoded by this skill.
- Preserve APIs, payloads, permissions, validation, default business values, state machines, and existing functionality. Design screenshots do not authorize changing these. Investigate backend behavior only when relevant and keep backend repositories read-only unless separately authorized. Surface conflicts and continue independent work.
- Use existing authorization. Ask only for missing design, target, or business decisions that cannot be recovered from the conversation, repository, or available tools. Do not repeatedly ask users to approve already authorized work.
- Use an available official Figma connector to read the relevant node's structure/properties and screenshot. Follow any tool-specific prerequisite skills the host actually provides; this package does not depend on another named skill being installed. Read [figma-access.md](references/figma-access.md) for access failures or first-time connection.
- Design evidence priority: matching structured node properties/variables and original assets → matching Figma property panel or SVG values → screenshot-assisted estimates. Confirm node, layer, state, and version before resolving conflicts. Computed styles describe the implementation, not the design. Label estimates and approved deviations.
- Reuse valid evidence when design version, variant, state, and scope still match. Refresh only affected evidence. A tool connection alone does not establish that a node was read.
- Prefer supplied original assets and licensed fonts. Do not replace provided assets with Unicode, emoji, approximate icons, generated images, or improvised drawings. If assets are unavailable, check existing project assets and record the gap.
- Missing browser access does not prohibit authorized code changes, but the result remains **visually unverified**. Missing design properties do not become guessed "Figma facts." Never claim pixel-perfect, 1:1, or visually accepted results without relevant evidence.
- Keep temporary screenshots, exports, overlays, diffs, recordings, and test reports in an already ignored local directory or a system temporary directory. Runtime assets may enter the repository. Do not place temporary evidence in public/build asset directories or publish private designs, credentials, and customer data.
- Do not automatically create agents, worktrees, task documents, commits, pushes, database changes, or deployments. A skill invocation does not grant those permissions.

## Focused fix: locate → change → verify

1. **Lock a verifiable target.** Use explicit user values, a supplied reference, valid prior evidence, or the relevant Figma component/text properties. User-requested overrides take precedence; record them as overrides rather than design facts. If the target is identifiable, proceed without a lengthy brief.
2. **Inspect only what matters.** Read the component, relevant styles/tokens, and necessary callers. Capture a before screenshot of the affected region when possible and inspect its actual computed styles. Avoid whole-file Figma scans, unrelated backend/PRD research, a large plan, or a task directory. Repository-mandated context still applies.
3. **Make the smallest change.** Prefer the page's scope or existing component parameters. Check CSS order, specificity, inheritance, and the actual running service's working directory. If a shared default must change, inspect representative affected callers; do not accumulate overrides without finding the cause.
4. **Screenshot → compare → fix → screenshot → re-check.** Use the same viewport, zoom, language, scroll position, and state. Reload to confirm current code. Check the target and neighboring layout, computed styles, text baselines, wrapping, overflow, and relevant click/focus/hover states. Stop when the scoped target passes; do not expand into a full-site review. Overlays and a full state matrix are optional for focused fixes.
5. **Run required checks and report briefly.** Run repository-required and change-relevant checks. Do not add tests that merely duplicate a reversible CSS edit. Report changes, design source/values, actual browser evidence, check results, and remaining limitations. Explicitly identify skipped checks and missing screenshots.

If a focused task reveals cross-region or multi-state defects, explain the expanded verification scope and use the relevant parts of the full workflow. Pause only the work depending on an unresolved business decision.

## Read-only audit

Use [visual-review.md](references/visual-review.md) to compare the requested design and running route without editing application files. Opening the existing page and saving local evidence are allowed unless the user forbids them. Starting a missing service follows repository rules and user authorization; never change configuration or install dependencies just to audit.

Report each actionable difference with the design node/layer, evidence type, expected value, actual browser value, impact, and likely code location. Separate implementation defects, approved differences, dynamic data, responsive assumptions, and missing evidence. If only screenshots are available, limit conclusions accordingly. Do not fix findings, update visual baselines, or present a static comparison as an executed interaction test.

## Long tasks and handoff

For multi-page work that needs persistent context, optionally use [task-brief.md](assets/task-brief.md) and [task-state.md](assets/task-state.md). Fill recoverable facts yourself; do not make the user complete a long questionnaire. Keep one current state and refresh changed facts on handoff. A focused fix does not require these documents.

## Completion

Distinguish **code changed**, **checks passed**, **visually verified**, and **blocked/unverified**. Full restore needs real screenshots and relevant state verification; a read-only audit delivers findings without a code patch. Build success, HTTP 200, and a screenshot regression against an unapproved baseline do not prove Figma fidelity.
