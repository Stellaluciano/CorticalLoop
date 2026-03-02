# CorticalLoop Architecture

CorticalLoop models AI reasoning as iterative feedback loops inspired by cortical circuits. It is a complementary abstraction to chain-of-thought for AI agents focused on iterative refinement.

## Core components
- **Cortical State**: Runtime state captured per iteration.
- **Hypothesis Pool**: Candidate set of hypotheses.
- **Feedback Signal**: Scoring output from evaluator.
- **Recurrent Loop**: Controller coordinating generate → evaluate → refine.
- **Inhibitory Gate**: Optional pruning of low-scoring hypotheses.

See `docs/architecture.mmd`. To regenerate the PNG locally, run `python scripts/render_diagram.py`.
