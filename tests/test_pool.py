from corticalloop.pool import HypothesisPool
from corticalloop.types import Hypothesis


def test_pool_topk_and_prune():
    pool = HypothesisPool()
    pool.add([
        Hypothesis(id="a", text="A", score=0.2),
        Hypothesis(id="b", text="B", score=0.8),
        Hypothesis(id="c", text="C", score=0.5),
    ])
    assert [h.id for h in pool.topk(2)] == ["b", "c"]
    pool.prune_below(0.5)
    assert sorted(h.id for h in pool.all()) == ["b", "c"]
