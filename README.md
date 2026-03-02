# CorticalLoop

**CorticalLoop** is a neuro-inspired **AI reasoning** framework for **AI agents** that models problem solving as iterative feedback loops rather than a single linear trace.

- 🧠 Neuro-inspired abstractions: cortical state, hypothesis pool, feedback signal, recurrent loop.
- 🔁 Practical iterative refinement with pluggable hypothesis generation, evaluation, and refinement.
- 🔍 Audit-friendly run records as a hypothesis graph/collection across iterations (JSON export).

## Why CorticalLoop?
Many systems frame reasoning with chain-of-thought traces. CorticalLoop offers a **complementary** and **alternative perspective** focused on hypothesis generation and iterative refinement. This is a different abstraction in the same problem-space, designed to coexist with other methods.

## Architecture
> Note: The PNG is generated locally (not committed) to keep the repo text-only-friendly for environments that cannot review binary diffs.

Generate the diagram asset:
```bash
python scripts/render_diagram.py
```

Then view `assets/corticalloop_architecture.png` locally.

Mermaid source: [`docs/architecture.mmd`](docs/architecture.mmd)

## Quickstart (offline, no API keys)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python examples/quickstart.py
```

## MVP API
```python
from corticalloop import CorticalLoop, LoopConfig

loop = CorticalLoop(config=LoopConfig(max_iters=4, num_hypotheses=4, top_k=2))
result = loop.solve(task="Draft a project rollout plan", context={"constraints": ["2 weeks", "small team"]})

print(result.final_answer)
print(result.record.to_json())
```

## Core concepts
- **Cortical State**: per-iteration working representation.
- **Hypothesis Pool**: collection of candidate plans/solutions.
- **Feedback Signal**: evaluator scores used for selection.
- **Recurrent Loop**: iterative controller with stop conditions.
- **Inhibitory Gate**: optional low-score pruning for cost control.

## Integrations (planned)
- LangChain and LlamaIndex adapters
- Tool-using agent runtimes
- Multi-agent hypothesis exchange

## Roadmap
- **v0.1**: offline loop, mock LLM, heuristic evaluator, run-record JSON.
- **v0.2**: optional OpenAI-backed generator/evaluator/refiner and richer tracing tools.
- **v1.0**: robust adapter ecosystem, benchmarking, and production observability.

## FAQ
**Is this the same as chain-of-thought?**
Not exactly. Chain-of-thought is often represented as a linear reasoning trace, while CorticalLoop emphasizes iterative feedback loops over a hypothesis pool. They are related approaches in AI reasoning and can be complementary depending on the use case.

**Does CorticalLoop require API keys?**
No. The default path is offline using `MockLLM` + `HeuristicEvaluator`.

## GitHub description suggestion
CorticalLoop is a neuro-inspired AI reasoning framework for AI agents. It models reasoning as iterative feedback loops of hypothesis generation, evaluation, and refinement, with audit-ready run records. Offline-first with MockLLM + heuristic evaluator, plus optional OpenAI adapters when API keys are available.

## License
MIT
