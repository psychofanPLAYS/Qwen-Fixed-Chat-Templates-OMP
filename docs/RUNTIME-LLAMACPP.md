# llama.cpp runtime profile

The root `chat_template.jinja` is the llama.cpp version; no separate hand-maintained copy is required.

Baseline launch shape:

```text
llama-server ... --jinja --chat-template-file chat_template.jinja --reasoning-format deepseek --reasoning-preserve
```

Keep Flash Attention and the chosen compiled KV-cache pair enabled separately. This repository does not hard-code KV precision into the chat template.

Reasoning shorthand is handled by Jinja:
- `<[l]>` LOW
- `<[m]>` MEDIUM
- `<[h]>` custom high
- `<[x]>` XHIGH
- `<[/]>` off

Release gate: verify structured tool calls, reasoning extraction, preserved reasoning across tool turns, prefix stability, and OMP Shake/resume behavior against the current llama.cpp build.
