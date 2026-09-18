import os
import sys
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = Environment(loader=FileSystemLoader(ROOT), undefined=StrictUndefined,
                  keep_trailing_newline=True, lstrip_blocks=True, trim_blocks=True)
env.globals["raise_exception"] = lambda msg: (_ for _ in ()).throw(Exception(msg))
TEMPLATE_FILE = os.environ.get("QWEN_TEMPLATE_FILE", "chat_template.jinja")\ntemplate = env.get_template(TEMPLATE_FILE)

def render(messages, **kwargs):
    return template.render(messages=messages, add_generation_prompt=True, **kwargs)

def must(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS", name)

# Native/default behavior remains intact.
out = render([{"role":"user","content":"hello"}])
must("default is medium/no injected effort", "Reasoning effort is set to " not in out and "Reasoning mode is set to high." not in out)

out = render([{"role":"user","content":"<[l]>\nhello"}])
must("LOW alias", "Reasoning effort is set to low." in out)
must("LOW stripped", "<[l]>" not in out)

out = render([{"role":"user","content":"<[x]>\nhello"}])
must("XHIGH alias", "Reasoning effort is set to xhigh." in out)
must("XHIGH stripped", "<[x]>" not in out)

out = render([{"role":"user","content":"<[high]>\ninspect then act"}])
must("custom high instruction", "Reasoning mode is set to high." in out)
must("custom high iterative contract", "Prefer evidence and forward progress over one enormous uninterrupted thought." in out)
must("custom high stripped", "<[high]>" not in out)

out = render([
    {"role":"user","content":"<[high]>\nstart"},
    {"role":"assistant","content":"done","reasoning_content":"prior reasoning"},
    {"role":"user","content":"continue"},
])
must("custom high sticky", "Reasoning mode is set to high." in out)

out = render([{"role":"user","content":"<[high]>\npart A\n<[m]>\npart B"}])
must("same-message textual last control wins", "Reasoning mode is set to high." not in out and "Reasoning effort is set to xhigh." not in out)
must("medium alias stripped", "<[m]>" not in out)

out = render([
    {"role":"user","content":"<[x]>\nstart deep"},
    {"role":"user","content":"<[high]>\nnow iterate"},
])
must("later message overrides earlier", "Reasoning mode is set to high." in out and "Reasoning effort is set to xhigh." not in out)

out = render([{"role":"user","content":"<|think_high|> legacy"}])
must("legacy Frog high remains xhigh", "Reasoning effort is set to xhigh." in out)

out = render([{"role":"user","content":"<[/]>\nmechanical"}])
must("off alias stripped", "<[/]>" not in out)
must("off alias emits closed think prefill", out.endswith("<think>\n\n</think>\n\n"))

# API alias compatibility remains Frog-compatible: high maps to native xhigh.
out = render([{"role":"user","content":"api high"}], reasoning_effort="high")
must("API high compatibility remains xhigh", "Reasoning effort is set to xhigh." in out)

print("All OMP extension tests passed.")
