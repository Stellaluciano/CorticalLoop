from corticalloop import CorticalLoop, LoopConfig


def test_loop_runs_and_returns_record():
    loop = CorticalLoop(config=LoopConfig(max_iters=2, num_hypotheses=3, top_k=2))
    result = loop.solve("Improve incident response process", context={"constraints": ["24/7 coverage"]})
    assert result.final_answer
    assert len(result.record.iterations) >= 1
    assert result.record.selected_path
