# NInfer runtime profile

Use the same root Jinja template if the active NInfer build supports chat-template override for the Qwen 3.8 artifact.

Target use case:
- RTX 4090 / sm_89
- Qwen 3.8 27B
- full 262,144 context
- compressed KV mode appropriate to the 4090 fork (currently rk4v4-e8 is the full-context target)
- OpenAI Responses-compatible serving for OMP where practical
- preserved thinking/session continuation

Important separation:
- Jinja controls prompt behavior.
- NInfer controls generation, KV state, MTP, and any real hard thinking-budget fuse.
- OMP controls multi-turn workflow, Shake, pruning, notes, and context rollover.

Do not claim a per-request custom `high` engine effort unless the NInfer endpoint explicitly supports it. In r1, `<[high]>` is template-level iterative steering while native request-level effort compatibility remains unchanged.

Release gate: verify the exact current 4090 fork CLI/API, tool streaming, Responses continuation, preserved reasoning, OMP Shake/resume, and 262K allocation on hardware.
