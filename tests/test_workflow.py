from unittest.mock import Mock

import graph.workflow as workflow_module


def patch_workflow_agents(monkeypatch, review_responses):
    research_mock = Mock(
        return_value={
            "sources": [{"source_id": "S1"}],
            "research_notes": "Research findings",
        }
    )
    analysis_mock = Mock(return_value={"analysis": "Analysis findings"})
    content_states = []

    def generate_report(state):
        content_states.append(state.copy())
        report = f"Draft report {len(content_states)}"
        return {"draft_report": report, "final_report": report}

    content_mock = Mock(side_effect=generate_report)
    review_mock = Mock(side_effect=review_responses)
    monkeypatch.setattr(workflow_module, "research_agent", research_mock)
    monkeypatch.setattr(workflow_module, "analysis_agent", analysis_mock)
    monkeypatch.setattr(workflow_module, "content_agent", content_mock)
    monkeypatch.setattr(workflow_module, "review_agent", review_mock)

    return research_mock, analysis_mock, content_mock, review_mock, content_states


def test_workflow_finishes_when_report_is_approved(monkeypatch):
    agents = patch_workflow_agents(
        monkeypatch,
        [
            {
                "approved": True,
                "revision_count": 0,
                "review_feedback": "Approved.",
            }
        ],
    )
    research_mock, analysis_mock, content_mock, review_mock, _ = agents

    result = workflow_module.run_research_workflow("Renewable energy")

    research_mock.assert_called_once_with("Renewable energy")
    analysis_mock.assert_called_once()
    content_mock.assert_called_once()
    review_mock.assert_called_once()
    assert result["approved"] is True
    assert result["final_report"] == "Draft report 1"


def test_workflow_revises_rejected_report_then_finishes_when_approved(monkeypatch):
    agents = patch_workflow_agents(
        monkeypatch,
        [
            {
                "approved": False,
                "revision_count": 1,
                "review_feedback": "Add citations.",
            },
            {
                "approved": True,
                "revision_count": 1,
                "review_feedback": "Approved.",
            },
        ],
    )
    _, _, content_mock, review_mock, content_states = agents

    result = workflow_module.run_research_workflow("Renewable energy")

    assert content_mock.call_count == 2
    assert review_mock.call_count == 2
    assert content_states[1]["review_feedback"] == "Add citations."
    assert result["approved"] is True
    assert result["revision_count"] == 1
    assert result["final_report"] == "Draft report 2"


def test_workflow_stops_after_maximum_revisions(monkeypatch):
    agents = patch_workflow_agents(
        monkeypatch,
        [
            {
                "approved": False,
                "revision_count": 1,
                "review_feedback": "Add citations.",
            },
            {
                "approved": False,
                "revision_count": 2,
                "review_feedback": "Still missing citations.",
            },
        ],
    )
    _, _, content_mock, review_mock, _ = agents

    result = workflow_module.run_research_workflow("Renewable energy")

    assert content_mock.call_count == 2
    assert review_mock.call_count == 2
    assert result["approved"] is False
    assert result["revision_count"] == workflow_module.MAX_REVISIONS
    assert result["final_report"] == "Draft report 2"
