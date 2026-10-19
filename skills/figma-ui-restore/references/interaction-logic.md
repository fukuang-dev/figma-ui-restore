# Product interaction logic and flow acceptance

Read for page interaction implementation/optimization and full UI acceptance. A focused styling fix preserves behavior and verifies only affected interactions; do not expand it into a whole-site flow investigation.

## Establish what the product defines

| Evidence status | Decision |
| --- | --- |
| Defined | Follow the scoped prototype connections, page flowchart and explicit product specification |
| Partial | Preserve defined edges; analyze only the missing branches |
| Absent | After inspecting accessible relevant sources, derive supported UI behavior from existing code and project conventions |
| Not yet read | Record permission/quota/tool-field/node gaps; do not relabel unknown evidence as no flow |

The user's current explicit decision takes precedence. For conflicting product sources, check node, state and version; if still unresolved, identify the conflicting branch and continue independent work. Do not silently choose based on what feels conventional.

A `/proto/` URL may identify a page, selected node and separate starting node. Preserve those meanings when locating the flow; page-id is not a screen node. If the current connector accepts only design-node URLs, resolve the same file and actual node through supported read tools, rather than assuming the prototype is inaccessible. Follow host tool prerequisites. A visual node read or screenshot alone does not establish that reactions were read.

## Read the scoped flow

Collect entry/start state, triggering element/event, conditions, action type, destination and relevant state/feedback. Follow reachable targets only within the assignment, with visited-node tracking to avoid loops. Do not scan an entire design file to resolve one button.

Distinguish navigation, back, open/close overlay, component-variant changes, scroll, external links, delays and condition/variable actions. Do not turn every edge into a new route or drop an unreadable condition. Several prototype Frames can represent states of one existing component. Prefer the current reaction actions array; if only legacy action is available, use it as fallback. When both expose the same reaction, do not execute it twice.

For a drawn flowchart, inspect arrow direction, decision nodes and branch labels; do not infer connections from screen order or proximity. If the connector omits reactions, use an available authorized Prototype panel/player or supplied flow export. Record exact inaccessible branches and work on confirmed ones. Do not repeatedly retry the same access failure or ask the user to draw a new flow when the existing one is merely unreadable.

## Analyze absent or missing branches

Read relevant routes, component handlers/state, product context and analogous approved flows. For API-dependent behavior, inspect current contracts/implementation according to repository rules. Trace user goal → entry action → preconditions → transition → success/error feedback → back/cancel/retry and data retention.

Implement reliably supported UI decisions without asking the user to design every transition. For example, reuse a sibling dialog's established cancel/close behavior or an existing wizard's previous/next state model. Label each adopted behavior as inherited project behavior or implementation inference; neither becomes a product fact. State the reasoning briefly and keep inferred changes scoped and reversible.

Design silence does not authorize new APIs, permission rules, validation, business defaults, persistence, fees, authentication bypasses or business state-machine changes. Preserve existing business constraints. A product-defined skip action can dismiss onboarding without satisfying verification. If the product flow requires unsupported business behavior or conflicts with those constraints, name the exact gap, preserve the guard, and pause only that dependency for a product/user decision. Do not rewrite backend code as an incidental UI fix.

## Turn edges into acceptance targets

Use a small local note or an existing task state; a simple task needs no new long document. Tag rows **product-defined**, **project-inherited**, **implementation-inferred** or **unknown**.

| Source/status | Start/precondition | Element/event | Condition | Action/destination | Retention/feedback | Browser actual/result |
| --- | --- | --- | --- | --- | --- | --- |
| Product-defined | Guide step 1 | Next/click | None | Show guide step 2 | Follow existing draft policy | Not executed |
| Product-defined | Guide step 1 | Skip/click | None | Show overview | Verification state unchanged | Not executed |
| Project-inherited | Dialog open | Cancel/click | Existing guard | Close dialog | No submit request | Not executed |

These are illustrative rows, not facts about the next user's design.

Execute the scoped main path and relevant conditional/negative, back, cancel/close, error and retry paths in the actual running browser. When affected, check refresh, browser history, duplicate activation, focus, localization and data retention. Assert the destination/state and visible feedback, and inspect relevant request outcomes when applicable. Match each check to its source and record expected versus actual results.

Use authorized test environments, supplied fixtures or existing mocks for side effects. Do not send real invitations, payments, approvals or permission changes merely to verify a UI. If execution would exceed authorization or available resources, leave that path explicitly unverified while completing supported checks. Read-only audits deliver findings, not fixes or baseline changes.

Report **prototype edges read**, **application interaction paths executed**, **API outcomes verified**, and **visual comparison completed** separately. Builds, screenshots and source inspection do not prove a user flow works. For manual scenario prompts and expected boundaries, see the repository's `examples/interaction-flows/` (not required by the installed skill).
