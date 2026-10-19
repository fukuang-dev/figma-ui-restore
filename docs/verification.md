# Verification matrix / 验证矩阵

Version: 0.2.0. Recorded on 2026-10-19. Do not treat a workflow definition, static source scan, or offline example as proof of a live Figma integration.

| Item | Status | Evidence / limitation |
| --- | --- | --- |
| Skill metadata, plugin/catalog identity and internal Markdown references | Passed locally (macOS) | Metadata/reference/public-content check; see the version-specific validation result below |
| Project install, content integrity, duplicate refusal and dry-run | Passed locally (macOS) | Standard-library tests, including paths with spaces |
| Symlink destination refusal | Passed locally (macOS) | Redirected .agents destination refused without writing outside project |
| User install | Passed isolated test (macOS) | Temporary mock home; real personal skill untouched |
| ZIP exclusion rules and installation from extracted package | Passed locally (macOS) | ZIP inspected and extracted package installed into a temporary project |
| macOS / Linux / Windows installation and packaging | Passed in 0.1.0 GitHub Actions | Python 3.10 validation, seven-test suite and packaging passed in [run 39218656421](https://github.com/fukuang-dev/figma-ui-restore/actions/runs/39218656421). Windows symlink creation test is explicitly skipped. |
| Offline example browser rendering and click behavior | Passed manually in a real browser | 960x640, three computed-style targets corrected in an isolated copy; primary text/weight, no overflow and local click behavior preserved. Not live Figma. |
| Independent offline audit and focused-fix trial | Passed scoped trial | A separate agent audited before edits and changed exactly three CSS declarations; parent verified final computed styles, click and keyboard activation/focus in the browser. |
| Fresh full-page live-Figma workflow | Not yet independently evaluated | The offline scoped trial does not establish whole-page live-connector behavior. |
| Live Figma interaction property read | Passed scoped maintainer check for 0.2.0 | Two real click edges read, with button/target names resolved; private evidence excluded |
| Figma OAuth setup and complete live property/screenshot workflow | Not verified for this public release | Existing authorization was reused; interaction read alone is not a full design/screenshot workflow |
| Plugin marketplace install in individual clients | Not yet verified | Portable metadata included; client versions may differ |
| Other AI clients | Not tested | No cross-client compatibility claim |

本表会在执行实际检查后更新。未验项不会被表述为通过；公开包不含私有 Figma 文件、凭证或客户数据。

## 0.2.0 interaction update

The new reference and seven original scenarios cover defined/partial/absent/unreadable flows, a business conflict, overlay/action semantics and focused styling scope. They are manual decision-review material, not an automated behavioral benchmark or executed application test.

A maintainer's authorized private prototype was read through the live Figma connector: the selected start Frame exposed two ON_CLICK navigation reactions; button text and destination names were separately resolved. This confirms that the supplied example actually contained readable interaction edges. It does not establish all branches, screenshots, OAuth setup for other users, or end-to-end application behavior. No private file/node identifiers or design assets are redistributed.

Local 0.2.0 checks passed: metadata/privacy validation, 34 internal Markdown links, 30 distributable files, all seven installation/distribution tests, ZIP packaging and installation from extraction. YAML frontmatter was parsed independently with Ruby; the optional bundled quick_validate.py could not run because its PyYAML dependency was unavailable. The package itself requires only the Python standard library. Current CI results are available on the repository's Actions page; historical 0.1.0 CI below is not proof of 0.2.0 platform execution.

## Offline browser observations (0.1.0)

The shipped exercise stays intentionally imperfect. A separate ignored copy was changed and observed in the Codex in-app browser at 960x640. Raw before/after screenshots were inspected locally; they are temporary verification artifacts, not bundled product assets.

| Target | Before | After | Source |
| --- | --- | --- | --- |
| h1 font-size | 32px | 24px | Original design-spec.json |
| button border-radius | 16px | 8px | Original design-spec.json |
| .secondary color | rgb(23, 32, 51) | rgb(100, 116, 139) | Original design-spec.json |

Primary names remained rgb(23,32,51), weight 600; document horizontal overflow was false; clicking Invite member still changed the local status text without sending an invitation. Browser caching initially retained old CSS; a verification-only asset query in the isolated copy confirmed the latest file. This is a narrow offline exercise, not whole-page SVG pixel acceptance or a live connector test.

## Independent trial

A separate agent received only the installed skill, the original practice files, and a request to audit before fixing the specified targets. It reported all three numeric differences before editing and changed exactly the three CSS declarations. HTML, JavaScript, data, primary text, focus and responsive rules were unchanged by byte/hash checks. JavaScript syntax checking passed. The parent subsequently checked the final page in a real 960x640 browser: all three values matched, no horizontal overflow, click and Space activation updated the local status, and the focused button had a solid 3px outline.

The trial exposed ambiguous connector wording for offline inputs; the skill now explicitly permits supplied offline evidence without Figma authorization. This is a single scoped trial, not a general benchmark. The independent agent's final browser session was interrupted; final post-fix browser verification was performed by the parent.

## Cross-platform CI

The first Windows run exposed an implicit locale-dependent text decode. All package text reads now specify UTF-8; a non-UTF-8-locale regression test was added. The corrected code passed the macOS, Ubuntu and Windows jobs in the linked run. The workflow uses fail-fast: false so one platform cannot hide the remaining results. Third-party runner action deprecation notices are separate from the passing package checks.
