# Qwen Fixed Chat Templates — OMP hardening

> 🚧 **WIP / experimental. Not a stable release yet.**
>
> The implementation is being qualified against real **Oh My Pi (OMP) + llama.cpp** agent sessions before it is promoted as ready for normal use.

This project hardens Froggeric's **Qwen Fixed Chat Templates v22.5** for Qwen 3.8 used as a local coding/dev model behind **OMP**, with llama.cpp first and NInfer qualification afterward.

## Current development

Active implementation:

- branch: `feat/omp-reasoning-workflow-r1`
- PR: [#1 — Harden Froggeric v22.5 for OMP local Qwen workflows](../../pull/1)
- current gate: [#2 — qualify on current llama.cpp + OMP](../../issues/2)

The feature branch already contains the template, tests, fuzzer, runtime docs, and OMP context-workflow design. CI/Jinja testing is green, but **real-engine runtime qualification is intentionally still open**.

## Planned gates

1. **llama.cpp + OMP runtime qualification** — issue #2
2. **NInfer 4090 / full-context qualification** — issue #3
3. **OMP iterative `high` + Shake/notes workflow** — issue #4
4. **native OMP history vs Codex-Timelines-style derived index** — issue #5

See [PLAN.md](PLAN.md) for the locked first-release plan and [UPSTREAM.md](UPSTREAM.md) for provenance.

## Upstream

Derived from Froggeric Qwen Fixed Chat Templates v22.5 under Apache-2.0.

**Do not treat this repository as production-ready until the runtime gates are closed.**
