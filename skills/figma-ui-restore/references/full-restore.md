# Full implementation and verification

Read this only for whole-page/multi-page implementation or broad visual verification. Keep focused fixes in the entrypoint's short workflow. For an audit, use these evidence steps without editing code.

## 1. Bind design and runtime

Identify the exact Figma file/node, target route/component, state, language, reference viewport, and browser zoom from the conversation and available context. A Section or canvas boundary is not necessarily a page Frame. Read large designs in relevant child sections after inspecting their tree.

Record the frontend working directory, current changes, actual running service/port, and the version being served. Source files existing on disk do not prove that the browser loads them. Do not print credentials. Locate existing routes, page components, styles, event handlers, data flow, and shared primitives before implementation.

Obtain matching properties, a node screenshot, necessary assets, and the relevant open/closed/selected/empty/error/loading/disabled states. [Access guidance](figma-access.md) covers fallback paths. Existing still-valid evidence can be reused.

## 2. Build a small evidence/difference table

For each important visual item record: design layer/state; evidence source; expected value; current value; proposed code location; adopted value or approved difference. Keep facts separate from implementation assumptions. A concise work note is enough; persistent task documents are optional for longer work.

Inspect:

- Region hierarchy, component variants, Auto Layout, width/height constraints, padding/gap, alignment, scrolling, sticky/fixed elements, and available responsive designs.
- Each semantic text layer: font family, size, weight, line height, letter spacing, color/opacity, alignment, wrapping and truncation. Table headers, primary/secondary cells, amounts/dates, badges and action text may all differ. Do not infer all text styles from a parent row.
- Page/card/header/notice/badge/button backgrounds separately; fills, borders, radii, shadows, icon viewBox versus visible bounds, input/button internal spacing, row heights, and column widths.
- Relevant dialogs, dropdowns, tooltips, hover/focus, empty/error/loading/disabled states. Preserve existing business defaults and validation when the design is silent.

Structured design properties outrank screenshot appearance. Exact selected-layer SVG/property-panel values outrank PNG sampling. Confirm that the selected layer is the target itself, not a parent or neighbor. Do not sample selection highlights, transparency checkerboards, browser chrome, comments, or antialiased edges as design colors.

## 3. Implement a representative slice first

For several pages, first implement one representative page at its reference dimensions, compare it in the browser, and correct major differences before expanding. Reuse existing components, but verify their defaults: library tooltips, shadows, radii and colors do not automatically match the design.

Use the real business component as the baseline for static previews, denied/readonly, empty and disabled variants unless the design explicitly specifies a separate component. Preserve layout, typography, widths and interactions; apply only the necessary state layer. Do not rebuild a second approximate UI for a preview.

Fix layout/size → spacing → typography/assets → colors/borders/radii/states. Scope CSS locally. Shared changes require representative caller checks. If the browser still shows an old value, inspect cascade/order/specificity, actual served CSS, service cwd, stale tabs and HMR before adding more rules.

## 4. Verify in the running browser

Reuse an existing valid development service. Start one only if allowed by the repository and task; otherwise report the runtime gap. Open the actual route with its real authorization. Do not bypass login, grant roles, or execute live business writes for screenshots.

Capture before and after screenshots under equal viewport, device scale, browser zoom, scroll, language, state and comparable data shape. Confirm actual font loading and stable layout. Inspect key nodes with computed styles and geometry; the source declaration alone is not proof.

For tables/lists, sample header, primary/secondary cell, date/amount, badge and action text separately for size, weight, line height, color and alignment. Check real available width, min-width, white-space, padding, wrapping, truncation and click targets. Correct typography can still produce a broken action column.

Reload cleanly before final evidence. Use overlays/diff images when available without adding a large project dependency. Explain missing overlays; do not replace visual judgment with a generic pixel-difference threshold. Dynamic values and OS font antialiasing differences should be identified, not hidden over layout defects.

Validate only the relevant combinations: supplied desktop/narrow/mobile Frames, relevant dialogs/dropdowns, selected states, keyboard focus and affected localized layouts. If no mobile design exists, use existing project conventions, record the assumption, and do not claim mobile pixel fidelity. Do not invent new navigation behavior.

The first acceptance baseline is Figma (or the user's explicit offline specification). Only an accepted browser result can become a later regression baseline. Never update a baseline merely to silence a failing screenshot test.

## 5. Close out proportionately

Run applicable repository checks and change-related behavior checks, without rebuilding unchanged work repeatedly. Keep build/test operations from concurrently writing the same output directory. Record skipped checks and reasons.

Deliver the implemented scope, major differences resolved, evidence sources and adopted key values, browser screenshot locations, checks/results, and any missing evidence or approved deviations. Separate code delivery, visual verification, and business-path verification. Say exactly what remains unverified.
