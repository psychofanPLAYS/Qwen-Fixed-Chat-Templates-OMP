# OMP context + memory design

## Use OMP's existing machinery first

Current OMP can mechanically reduce history without asking another model to summarize it.

### Shake

Auto-shake currently protects a recent tail and elides eligible heavy content into recoverable artifacts. Manual `/shake` is more aggressive. `/shake thinking` can remove old reasoning blocks when the operator deliberately chooses to trade prefix/reasoning continuity for context space.

Recommended policy for this template:
- do not shake active evidence before it has been consumed;
- do not constantly shake thinking while `preserve_thinking` is providing useful continuity;
- shake old bulky tool outputs after their durable conclusions are represented in working state;
- use thinking shake only at a clear phase/window boundary.

### Notes-backed context windows

OMP's experimental context management supplies:
- `context_notes`: a small persistent working notebook;
- `new_context`: rollover at a safe tool-loop boundary;
- `history://current/full`: recoverable full branch history;
- `read` and `grep`: targeted retrieval from that history.

This is the preferred foundation for long-running local-Qwen sessions.

## Proposed high-mode loop

```text
MEDIUM-depth reasoning
    ↓
choose next consequential action
    ↓
tool / read / grep / test / edit
    ↓
observe real result
    ↓
continue from preserved reasoning
    ↓
record durable state if needed
    ↓
repeat
    ↓
verification pass
```

When context pressure rises, OMP maintenance should prune/shake recoverable bulk first. Only then roll to a new notes-backed context window.

## Optional TraceLedger

Do not duplicate full transcripts. If experiments show a graph/index helps navigation, keep only compact nodes/edges referencing OMP history entry IDs/artifacts.

Suggested files:
- `.omp-memory/ledger.tsv` — append-only compact nodes/edges.
- `.omp-memory/current.md` — human/model-readable active view generated from the ledger.

This remains optional until notes-backed history retrieval is benchmarked.
