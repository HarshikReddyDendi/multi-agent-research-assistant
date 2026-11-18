from unittest.mock import Mock

import pytest

import agents.research_agent as research_module


def test_research_agent_returns_structured_sources_and_notes(monkeypatch):
    search_results = [
        {
            "title": "First source",
            "url": "https://example.com/1",
            "content": "First finding",
            "score": 0.9,
        },
        {
            "title": "Second source",
            "url": "https://example.com/2",
            "content": "Second finding",
            "score": 0.8,
        },
    ]
    search_mock = Mock(return_value=search_results)
    llm_mock = Mock()
    llm_mock.invoke.return_value.content = "Organized research notes"

    monkeypatch.setattr(research_module, "search_web", search_mock)
    monkeypatch.setattr(research_module, "get_llm", Mock(return_value=llm_mock))

    result = research_module.research_agent("Example topic")

    search_mock.assert_called_once_with(query="Example topic", max_results=5)
    llm_mock.invoke.assert_called_once()
    assert "Example topic" in llm_mock.invoke.call_args.args[0]
    assert result == {
        "topic": "Example topic",
        "research_notes": "Organized research notes",
        "sources": [
            {
                "source_id": "S1",
                "title": "First source",
                "url": "https://example.com/1",
                "content": "First finding",
                "score": 0.9,
            },
            {
                "source_id": "S2",
                "title": "Second source",
                "url": "https://example.com/2",
                "content": "Second finding",
                "score": 0.8,
            },
        ],
    }


def test_research_agent_raises_when_search_returns_no_results(monkeypatch):
    search_mock = Mock(return_value=[])
    get_llm_mock = Mock()
    monkeypatch.setattr(research_module, "search_web", search_mock)
    monkeypatch.setattr(research_module, "get_llm", get_llm_mock)

    with pytest.raises(RuntimeError, match="No web search results found"):
        research_module.research_agent("Example topic")

    get_llm_mock.assert_not_called()
