# Visual evidence and audit

## Compare like with like

Use the Frame's original CSS dimensions, not its zoomed Figma canvas appearance. Match viewport, device scale, zoom, scroll, language and state. Wait for fonts, images and layout to stabilize. Record platform/font differences when material.

Figma is the first visual baseline. Browser regression snapshots become useful only after the browser output has been accepted against that baseline. HTTP 200, build success, a static fixture, or a previously accepted screenshot from another version each establish different facts.

## Inspect by semantic layers

Measure region/component bounds, padding/gap, borders, radii, backgrounds, icon bounds and typography. Inspect child text layers separately rather than inheriting a row's style across all cells. A row selector that makes every cell bold or muted is acceptable only if the design actually specifies it.

Verify hierarchy first: layout/size, spacing, typography/assets, then colors/borders/states. Inspect interaction-only visuals such as tooltip, native title, focus ring, hover, disabled, drawer and dropdown. Keep accessibility semantics; do not add unrequested visual decoration.

For a shared component, sample affected callers and the localized/long-text conditions relevant to the change. Check overflow and usable click targets, not just declared font sizes. Responsive verification follows actual supplied designs and project support; do not invent a mobile fidelity claim.

## Classify findings

| Category | Treatment |
| --- | --- |
| Implementation defect | Identify affected node/code and propose the smallest correction |
| Approved product difference | Record who/what authorized it and its visual effect |
| Dynamic data difference | Compare layout using a comparable shape; preserve actual data |
| Responsive assumption | Mark inferred behavior; do not call it design fact |
| Missing evidence | State the exact unavailable node/property/state |

Each actionable audit finding should include: area/state, expected value and evidence source, actual browser value/screenshot, impact, likely code location, and recommendation. Prioritize visible layout or readability defects over tiny antialiasing differences. Do not invent a universal acceptable pixel-error percentage.

## Evidence artifacts

A full review should have the reference, raw browser screenshot and regional observations. Add aligned overlay/diff images when practical; record why they are missing. Focused fixes need only local before/after screenshots and relevant computed styles. Exclude dynamic content only if the mask is documented and does not hide a defect under review.

Temporary evidence stays in ignored local directories or the system temporary directory. Public example assets require an explicit right to redistribute. Never publish private customer/design screenshots as a side effect of verification.

## Honest result language

- **Code changed:** the patch exists; this says nothing about browser verification.
- **Checks passed:** name the checks actually run and their outcomes.
- **Visually verified:** name the exact reference, route/region/state, viewport and browser evidence.
- **Unverified/blocked:** state the unavailable tool/input and practical effect.

If the user requested an audit, deliver findings and do not apply fixes, alter baseline images, install dependencies or edit project configuration. If only screenshots were compared, do not claim that interactions were executed.
