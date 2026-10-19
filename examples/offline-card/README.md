# Offline practice / 离线练习

This original example is included under this repository's MIT license. It is **not** a Figma export or proof of a live Figma integration. The SVG illustrates the intended design; [design-spec.json](design-spec.json) is the authoritative source for the three exercise values. Geometry outside those values is illustrative.

本示例为原创离线练习，没有 Figma 授权要求，也不代表已测试真实 Figma 连接。SVG 用于参考，JSON 明确规定本次三个目标值；其他几何细节不作为像素验收标准。

From this directory, run / 在本目录执行：

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/` (implementation) and `http://127.0.0.1:8765/reference.svg` (reference). On Windows use `py -3` instead of `python3` if needed. Stop the service with Ctrl+C.

Install the skill in a disposable copy of this directory or globally. Open that copy in Codex, then send:

```text
Use $figma-ui-restore. This is an offline practice exercise, not a live Figma task.
Target: the running index.html page at http://127.0.0.1:8765/.
Reference: design-spec.json and reference.svg in this directory.
Fix only the three targets in design-spec.json. Preserve behavior and all other styles.
Use a 960x640 viewport and capture before/after browser screenshots when a browser tool is available.
```

中文提示：

```text
使用 $figma-ui-restore。这是离线练习，不需要连接 Figma。
目标为 http://127.0.0.1:8765/，参考当前目录的 design-spec.json 和 reference.svg。
只修复 JSON 中的三个目标值，保留其他样式、数据和按钮行为。
以 960×640 视口取得浏览器修改前后截图；没有浏览器工具则明确标注视觉未验。
```

Read-only variation: replace “fix” with “audit only; list differences without editing any files.” After an audit, `git diff --exit-code -- examples/offline-card` should still be clean in a fresh repository checkout. Evidence files should be saved elsewhere.

After the fix: h1 is 24px; button radius is 8px; role text is #64748b. Primary names remain #172033/600, the button still updates the local notice, and Tab still exposes its focus indicator. Check these facts in the browser rather than inferring them from CSS text alone.

## Live Figma exercise

To test the full connector workflow, use a Figma file you have permission to access and redistribute if publishing results. Supply an exact Frame/node link and a running project route. Verify actual node properties **and** a matching node screenshot. This repository deliberately does not embed a private file key or pretend the offline SVG came from Figma.
