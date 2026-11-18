from unittest.mock import Mock

import pytest

import agents.review_agent as review_module


@pytest.mark.parametrize(
    ("llm_response", "expected_approved", "expected_revision_count"),
    [
        ("APPROVED: YES\n\nFEEDBACK:\nLooks good.", True, 2),
        ("APPROVED: NO\n\nFEEDBACK:\nAdd source citations.", False, 3),
        ("Approval: YES\n\nFEEDBACK:\nUnsupported approval format.", False, 3),
    ],
)
def test_review_agent_decides_approval_and_revision_count(
    monkeypatch, llm_response, expected_approved, expected_revision_count
):
    llm_mock = Mock()
    llm_mock.invoke.return_value.content = llm_response
    monkeypatch.setattr(review_module, "get_llm", Mock(return_value=llm_mock))
    state = {
        "topic": "Renewable energy",
        "research_notes": "Solar capacity is increasing.",
        "sources": [{"source_id": "S1"}],
        "draft_report": "# Research Report\n\nExample report",
        "revision_count": 2,
    }

    result = review_module.review_agent(state)

    assert result == {
        "approved": expected_approved,
        "review_feedback": llm_response,
        "revision_count": expected_revision_count,
    }
    assert "Example report" in llm_mock.invoke.call_args.args[0]


@pytest.mark.parametrize(
    "missing_key",
    ["topic", "research_notes", "sources", "draft_report", "revision_count"],
)
def test_review_agent_raises_for_missing_required_state(monkeypatch, missing_key):
    llm_mock = Mock()
    llm_mock.invoke.return_value.content = "APPROVED: YES\n\nFEEDBACK:\nLooks good."
    monkeypatch.setattr(review_module, "get_llm", Mock(return_value=llm_mock))
    state = {
        "topic": "Renewable energy",
        "research_notes": "Solar capacity is increasing.",
        "sources": [{"source_id": "S1"}],
        "draft_report": "# Research Report\n\nExample report",
        "revision_count": 2,
    }
    state.pop(missing_key)

    with pytest.raises(KeyError, match=missing_key):
        review_module.review_agent(state)

    llm_mock.invoke.assert_not_called()
