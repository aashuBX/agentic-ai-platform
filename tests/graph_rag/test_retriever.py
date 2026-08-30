"""Uses the `graph_repository`/`graph_retriever` fixtures (tests/conftest.py), which seed the real
demo/data/relationships.json dataset through the real extraction pipeline."""

from app.graph_rag.context_formatter import GraphContextFormatter


def test_direct_relationship_is_found(graph_retriever):
    paths = graph_retriever.retrieve("Who is the agent assigned to John Doe?")
    descriptions = [p.describe() for p in paths]
    assert any("ASSIGNED_TO--> Sarah Lee" in d for d in descriptions)


def test_multi_hop_relationship_is_found(graph_retriever):
    paths = graph_retriever.retrieve("Tell me about John Doe's appointment")
    descriptions = [p.describe() for p in paths]
    assert any("BOOKED--> APT-4001 --WITH--> Sarah Lee" in d for d in descriptions)


def test_unrelated_query_finds_nothing(graph_retriever):
    assert graph_retriever.retrieve("What is the weather today?") == []


def test_unknown_name_finds_nothing(graph_retriever):
    assert graph_retriever.retrieve("Who is assigned to Nobody Special?") == []


def test_max_hops_limits_path_depth(graph_retriever):
    shallow = graph_retriever.retrieve("Tell me about John Doe", max_hops=1)
    deep = graph_retriever.retrieve("Tell me about John Doe", max_hops=2)
    assert len(deep) >= len(shallow)
    assert all(len(p.hops) <= 1 for p in shallow)


def test_context_formatter_prefers_longer_more_specific_paths(graph_retriever):
    paths = graph_retriever.retrieve("Who is the agent assigned to John Doe?")
    context = GraphContextFormatter().format(paths)
    lines = context.split("\n")
    assert lines == sorted(lines, key=len, reverse=True)


def test_context_formatter_handles_no_paths():
    assert GraphContextFormatter().format([]) == ""
