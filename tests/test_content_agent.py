from unittest.mock import Mock

import pytest

import agents.content_agent as content_module


def test_content_agent_returns_report_and_includes_revision_context(monkeypatch):
    llm_mock = Mock()
    llm_mock.invoke.return_value.content = "# Research Report\n\nExample report"
    monkeypatch.setattr(content_module, "get_llm", Mock(return_value=llm_mock))
    state = {
        "topic": "Renewable energy",
        "research_notes": "Solar capacity is increasing.",
        "analysis": "Adoption is accelerating.",
        "sources": [{"source_id": "S1"}],
        "review_feedback": "Clarify the limitations.",
        "revision_count": 1,
    }

    result = content_module.content_agent(state)

    prompt = llm_mock.invoke.call_args.args[0]
    assert "Renewable energy" in prompt
    assert "Clarify the limitations." in prompt
    assert "Revision Number:\n1" in prompt
    assert result == {
        "draft_report": "# Research Report\n\nExample report",
        "final_report": "# Research Report\n\nExample report",
    }


@pytest.mark.parametrize(
    "missing_key",
    ["topic", "research_notes", "analysis", "sources", "review_feedback", "revision_count"],
)
def test_content_agent_raises_for_missing_required_state(monkeypatch, missing_key):
    llm_mock = Mock()
    monkeypatch.setattr(content_module, "get_llm", Mock(return_value=llm_mock))
    state = {
        "topic": "Renewable energy",
        "research_notes": "Solar capacity is increasing.",
        "analysis": "Adoption is accelerating.",
        "sources": [{"source_id": "S1"}],
        "review_feedback": "Clarify the limitations.",
        "revision_count": 1,
    }
    state.pop(missing_key)

    with pytest.raises(KeyError, match=missing_key):
        content_module.content_agent(state)

    llm_mock.invoke.assert_not_called()
