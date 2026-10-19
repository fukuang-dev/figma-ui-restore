# Interaction decision exercise / 交互逻辑情境练习

Original, fictional inputs for 0.2.0. No Figma login or product data is required. These cases exercise planning decisions; they are not a runnable app or proof of browser acceptance. Use the installed skill's interaction reference. If running an independent evaluation, give the evaluator only the request and raw inputs, then compare its output with the review criteria below.

## Raw inputs and request

Request: “Use figma-ui-restore to implement the supplied page flow. Read these inputs and produce a scoped transition plan; do not edit code or contact external systems in this exercise.”

1. **Defined:** A three-step guide has product edges `step-1.Next → step-2` and `step-1.Skip → overview`. Existing code sends both buttons to step-3. An existing verification guard remains required before any protected operation.
2. **Partial:** The product specifies `details.Save → summary` after an existing API succeeds. Cancel is not drawn. The shared editor already closes on Cancel without a save, returns focus to its opener and retains the same draft policy as sibling editors. No API contract changes are requested.
3. **Absent:** Accessible product notes and prototype define no interactions for a settings tab strip. The repository's shared tabs already use controlled local state, preserve form drafts on tab changes and expose keyboard navigation. The task adds a tab using that component.
4. **Unknown:** Only a screenshot was exported. The connector reports a permission failure before returning reactions. A Next button and two neighboring Frames are visible. Existing Next behavior goes to a confirmation state.
5. **Conflict:** A product edge appears to skip identity checks and activate a protected action. The current API rejects unverified accounts. Backend edits and changes to permission rules are outside the task.
6. **Action semantics:** A product-defined ON_CLICK reaction opens `help-panel` as an overlay, and the next action sets a presentation variable. Both a legacy `action` property and a current `actions` array describe the same overlay step. A Close control closes the overlay. No persistence rule is specified.
7. **Scope:** The user only asks for an 8px button radius. Its existing click handler and product flow are unchanged.

## Review criteria (read after producing the plan)

| Case | Observable decision |
| --- | --- |
| Defined | Next reaches step-2 and Skip reaches overview; no intuition-based step-3 shortcut; verification guard unchanged |
| Partial | Preserve the specified success edge; derive Cancel from the shared editor without demanding a new product flow; label inherited behavior |
| Absent | Reuse controlled tabs, draft retention and keyboard semantics; label the source; no new routes, API or product questionnaire |
| Unknown | Record unreadable reactions, preserve confirmed behavior provisionally, use available authorized fallback or ask only for the missing destination if blocking; never claim no product flow or infer edges from Frame proximity |
| Conflict | Identify the exact product/business conflict, keep the guard, pause that dependency and continue independent work; no backend edits or bypass |
| Action semantics | Open and close an overlay, respect action order, avoid double execution of legacy/current duplicates; do not invent routing or server persistence |
| Scope | Make the local visual correction and re-check its affected region; no full-flow audit |

For an application task, the plan must also define start state, event/condition, expected destination/state and feedback, source classification and actual browser results. This exercise has no running application: the honest behavior result is “not executed.”

中文：有产品流程按流程；缺分支自行分析；没画与没读到必须区分；业务冲突不猜测；弹层不是新路由；样式小改不扩大范围。以上仅为手动评估情境，不是已执行的真实项目交互验收。
