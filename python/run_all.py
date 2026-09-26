"""Run every framework example and summarise. Exit code 1 if any fails."""
import subprocess
import sys

EXAMPLES = ["langgraph_agent", "llamaindex_agent", "pydantic_ai_agent", "openai_agents_sdk", "smolagents_agent"]
failed = []
for name in EXAMPLES:
    proc = subprocess.run([sys.executable, f"{name}.py"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    line = next((l for l in proc.stdout.splitlines() if l.startswith("[")), "") or f"[FAIL] {name}: {(proc.stderr.strip().splitlines() or ['no output'])[-1]}"
    print(line)
    if proc.returncode != 0 or not line.startswith("[PASS]"):
        failed.append(name)
print(f"\n{len(EXAMPLES) - len(failed)}/{len(EXAMPLES)} passed")
sys.exit(1 if failed else 0)
