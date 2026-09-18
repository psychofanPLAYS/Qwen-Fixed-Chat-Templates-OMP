# Qwen Fixed Chat Templates — OMP hardening

A conservative derivative of Froggeric's **Qwen Fixed Chat Templates v22.5**, focused on Qwen 3.8 as a local coding/dev model behind **Oh My Pi (OMP)**, with llama.cpp and NInfer runtimes.

## Status

Development is PR-first. The current feature work is intentionally small:

- preserve Froggeric v22.5 behavior and tests;
- add short sticky reasoning controls:
  - `<[l]>` / `<[low]>` → **LOW** (native Qwen low)
  - `<[m]>` / `<[med]>` / `<[medium]>` → **MEDIUM** (native Qwen medium)
  - `<[h]>` / `<[high]>` → **high** (custom iterative reason → act → observe mode)
  - `<[x]>` / `<[xhigh]>` → **XHIGH** (native Qwen xhigh)
  - `<[/]>` / `<[off]>` → thinking off compatibility/workflow control;
- keep Froggeric's original `<|think_*|>` controls intact;
- keep `preserve_thinking` enabled by default;
- test true textual last-control-wins for the new shorthand;
- design OMP context hygiene around Shake + notes-backed context windows rather than stuffing old tool output into the prompt forever.

The shorthand is ordinary text, not XML and not a model special token. It is consumed by the template before inference.

## Why custom `high` exists

Qwen 3.8's useful native ladder is LOW / MEDIUM / XHIGH. The custom lowercase **high** is not presented as a fourth trained Qwen effort. It is an agent workflow:

> think enough to choose the next consequential action; prefer real tool/file/test evidence over prolonged speculation; preserve prior reasoning; reassess after each result; verify before finalizing.

This targets the failure mode where XHIGH produces one enormous uninterrupted reasoning chain before taking useful action.

## Runtime strategy

One Jinja template is the source of truth. llama.cpp and NInfer get separate runtime/profile documentation; we do **not** maintain two hand-edited copies unless an engine proves it requires different Jinja semantics.

See:
- [Design lock](docs/DESIGN-LOCK.md)
- [Conversation/report recap](docs/REPORT-2026-09-18.md)
- [OMP context + memory design](docs/OMP-CONTEXT-MEMORY.md)
- [llama.cpp profile](docs/RUNTIME-LLAMACPP.md)
- [NInfer profile](docs/RUNTIME-NINFER.md)

## Upstream

Derived from Froggeric Qwen Fixed Chat Templates v22.5 (Apache-2.0). Canonical project: https://huggingface.co/froggeric/Qwen-Fixed-Chat-Templates . GitHub mirror used for reproducible source import: https://github.com/rchildre3/Qwen-Fixed-Chat-Templates .

This repository is not represented as an official Froggeric fork because the canonical project is hosted on Hugging Face.
