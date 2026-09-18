# Design lock — r1

Date: 2026-09-18

## Scope

Local Qwen 3.8 powering the OMP development environment. Keep this repository independent of unrelated projects or remote-model role schemes.

## Non-negotiable behavior

1. **Froggeric v22.5 is the base.** Do not rewrite working tool, vision, error-recovery, reasoning-history, or prefix-cache logic without a failing test that justifies it.
2. **Visible reasoning ladder:** **LOW**, **MEDIUM**, custom lowercase **high**, **XHIGH**.
3. **Custom high is iterative, not fake XHIGH.** It biases reason → act → observe → reason loops and prefers obtaining evidence over extending speculative thought.
4. **Thinking history stays preserved by default.** Historical reasoning may be deliberately shaken/rolled over at explicit context-maintenance boundaries, not continuously rewritten.
5. **Short controls:** `<[l]>`, `<[m]>`, `<[h]>`, `<[x]>`; full aliases remain available. `<[/]>` and `<[off]>` are kept for workflow automation even if rarely typed manually.
6. **Sticky state:** latest recognized control in retained system/developer/user history wins. For our shorthand, controls are processed line-by-line so later controls in the same message override earlier ones.
7. **Backward compatibility:** original Froggeric `<|think_*|>` tags and API alias behavior remain intact. In particular, request-level `reasoning_effort=high` still maps to native XHIGH; custom lowercase high is activated by our shorthand/controller.
8. **No template-level fake hard budgets.** A Jinja template cannot count generated reasoning tokens. Runtime token fuses belong in NInfer/llama.cpp/provider/controller layers.
9. **One source template.** llama.cpp and NInfer profiles share the same Jinja unless testing proves a required semantic split.
10. **No merge on vibes.** Upstream test suite + extension tests + deterministic fuzzer + runtime smoke tests are required.

## Shorthand parsing rule

The `<[...]>` family is not reserved by Jinja or Qwen. It is ordinary text. To reduce accidental triggers in pasted code, the r1 parser recognizes our controls only when they begin a line. The control prefix is stripped before inference; any following text on that line remains.

Examples:

```text
<[h]> inspect the failing path, use tools instead of speculating
```

or:

```text
<[m]>
routine edits

<[x]>
deeply verify this concurrency edge case

<[h]>
then converge through tool/test loops
```

The last shorthand control sets the sticky mode for subsequent turns. Section-local effort steering inside a single generation is an experiment, not yet claimed as engine-level reasoning switching.

## Merge gates

- Frog v22.5 tests pass.
- OMP extension tests pass.
- deterministic fuzzer passes at least 2,000 cases before release.
- minified/oneline output renders byte-identically.
- llama.cpp: tool-call + reasoning + preserve-history smoke test.
- NInfer-4090: OpenAI Responses/tool-call + reasoning + 262K profile smoke test.
- OMP: normal tool loop, repeated tool loop, Shake, notes-backed rollover, resume.
