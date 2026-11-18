from unittest.mock import Mock

import pytest

import agents.analysis_agent as analysis_module


def test_analysis_agent_returns_analysis_from_llm(monkeypatch):
    llm_mock = Mock()
    llm_mock.invoke.return_value.content = "Structured analysis"
    monkeypatch.setattr(analysis_module, "get_llm", Mock(return_value=llm_mock))

    state = {
        "topic": "Renewable energy",
        "research_notes": "Solar capacity is increasing.",
        "sources": [
            {
                "source_id": "S1",
                "title": "Energy report",
                "url": "https://example.com/energy",
                "content": "Solar capacity increased last year.",
            }
        ],
    }

    result = analysis_module.analysis_agent(state)

    prompt = llm_mock.invoke.call_args.args[0]
    assert "Renewable energy" in prompt
    assert "Solar capacity is increasing." in prompt
    assert "S1" in prompt
    assert result == {"analysis": "Structured analysis"}


@pytest.mark.parametrize("missing_key", ["topic", "research_notes", "sources"])
def test_analysis_agent_raises_for_missing_required_state(monkeypatch, missing_key):
    llm_mock = Mock()
    monkeypatch.setattr(analysis_module, "get_llm", Mock(return_value=llm_mock))
    state = {
        "topic": "Renewable energy",
        "research_notes": "Solar capacity is increasing.",
        "sources": [],
    }
    state.pop(missing_key)

    with pytest.raises(KeyError, match=missing_key):
        analysis_module.analysis_agent(state)

    llm_mock.invoke.assert_not_called()
