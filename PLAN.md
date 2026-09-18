# PLAN — locked r1

Date: 2026-09-18

This plan is the execution contract for the first reliable release. Do not broaden scope until the preceding gate is satisfied.

## Goal

Run Qwen 3.8 as a dependable local coding/development model inside OMP, with one Froggeric-derived chat template that works across llama.cpp and NInfer, avoids pathological uninterrupted XHIGH reasoning, preserves useful reasoning continuity, and uses OMP's native context-maintenance machinery instead of dragging obsolete tool output forever.

## Fixed interface

Reasoning controls:

| User control | Display | Meaning |
|---|---|---|
| `<[l]>`, `<[low]>` | **LOW** | native Qwen low |
| `<[m]>`, `<[med]>`, `<[medium]>` | **MEDIUM** | native Qwen medium; default |
| `<[h]>`, `<[high]>` | **high** | custom iterative agent mode |
| `<[x]>`, `<[xhigh]>` | **XHIGH** | native Qwen xhigh |
| `<[/]>`, `<[off]>` | off | compatibility/automation control |

Rules:
- custom shorthand is recognized only when it begins a line;
- latest recognized control in retained system/developer/user history wins;
- later shorthand in the same message overrides earlier shorthand;
- shorthand is stripped before inference while following text is retained;
- mid-line literals such as `example <[high]>` are not controls;
- original Froggeric `<|think_*|>` controls remain compatible;
- request-level `reasoning_effort=high` keeps Frog's existing mapping to native XHIGH;
- `preserve_thinking` remains enabled by default.

## Definition of custom high

`high` is not a fake fourth Qwen neural effort and not a shorter XHIGH.

It is an iterative development workflow:

```text
reason enough to choose the next consequential action
→ obtain real evidence with a tool/read/grep/test when possible
→ observe
→ continue from preserved reasoning + new evidence
→ repeat
→ verify consequential changes
→ final answer
```

The purpose is to turn one enormous speculative reasoning chain into several connected, evidence-driven reasoning turns.

## Phase 0 — upstream preservation

Status: DONE on PR #1.

- import Froggeric v22.5 source;
- preserve Apache-2.0 attribution;
- keep upstream tests/fuzzer;
- keep one canonical Jinja source;
- document upstream provenance.

Gate: upstream v22.5 tests remain green after extension.

## Phase 1 — template hardening

Status: IMPLEMENTED; CI verification in PR #1.

Requirements:
- short control aliases;
- true textual ordering for shorthand;
- sticky persistence;
- custom iterative high;
- off aliases;
- collision safety;
- no regression to tools/vision/reasoning preservation/prefix stability;
- generated one-line template must remain behaviorally equivalent.

Release test gate:
1. custom extension tests;
2. all 105 upstream v22.5 verification cells;
3. deterministic fuzzer with at least 2,000 generated conversations;
4. pretty + one-line template testing.

Do not merge r1 until this gate is green.

## Phase 2 — llama.cpp runtime qualification

Use the same root `chat_template.jinja`; do not create a drifting second template.

Test on current llama.cpp:
1. normal chat at MEDIUM;
2. LOW / MEDIUM / high / XHIGH sticky switching;
3. off alias;
4. reasoning extraction + `--reasoning-preserve`;
5. one tool call;
6. repeated sequential tool calls;
7. tool failure/retry;
8. preserved reasoning across tool turns;
9. OMP session resume;
10. `/shake`, `/shake thinking`, and post-shake continuation;
11. long-context prefix/cache behavior.

Gate: no malformed tool calls, no lost user text, no unexpected mode switch, no template/runtime parser error.

## Phase 3 — NInfer 4090 qualification

Purpose: full Qwen 3.8 context on RTX 4090; a 130K-only NInfer profile is not the target.

Target:
- 262,144 max context;
- full KV resident on 24 GB 4090 using the current proven 4090 compressed-KV mode;
- OMP OpenAI-compatible serving, preferably Responses if it passes compatibility;
- preserved reasoning/session continuation;
- custom Jinja override.

Test the Phase 2 behavior matrix again, plus:
- 220K+ working context;
- 262K allocation;
- MTP compatibility;
- LAN/Tailscale serving;
- restart/resume/state behavior;
- runtime runaway-thinking fuse.

Gate: full-context operation without CPU attention fallback or API/tool incompatibility.

## Phase 4 — OMP context workflow

Use OMP primitives before adding new storage.

Preferred order:
1. keep recent reasoning and active evidence;
2. use OMP pruning/useless-result elision;
3. Shake old recoverable tool payloads into artifacts;
4. keep durable working facts in `context_notes`;
5. recover details with `read`/`grep` on `history://current/full`;
6. use `new_context` at a safe boundary when rollover is actually needed;
7. reserve `/shake thinking` for deliberate phase/window cleanup.

Experiment with an OMP-side `high` controller only after the template is stable. A controller may create deliberate multi-pass continuation turns when there is no natural tool boundary, but r1 does not fake hidden turns in Jinja.

## Phase 5 — searchable history/index

Do not build a second source-of-truth database.

First benchmark OMP's native full-history grep/read and notes-backed windows.

Then evaluate adapting the existing Codex-Timelines representation:
- compact LLM-facing Markdown;
- semantic headings/anchors;
- full forensic record;
- machine metadata/catalog;
- tree relationships.

If an additional graph is still useful, make it a small derived index referencing OMP history/artifact IDs. Raw evidence remains in OMP.

## Hard safety/reliability rules

- No direct-to-main behavioral changes.
- Every template change gets a regression test.
- Do not change upstream Frog logic merely because a rewrite looks cleaner.
- Do not truncate code/tool arguments by default.
- Do not let Jinja claim it can enforce generation-token budgets.
- Do not inject mid-generation quota notices without separate runtime experiments.
- Do not maintain separate llama.cpp/NInfer Jinja copies unless engine semantics force it.
- Do not call a runtime qualified until tested on the actual engine.
