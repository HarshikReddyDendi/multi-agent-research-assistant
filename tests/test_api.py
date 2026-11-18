from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

import api.main as api_module


@pytest.fixture
def client():
    return TestClient(api_module.app)


def test_home_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Multi-Agent AI Research Assistant API is running."
    }


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_research_endpoint_returns_workflow_result(client, monkeypatch):
    workflow_mock = Mock(
        return_value={
            "topic": "Renewable energy",
            "final_report": "Research report",
            "approved": True,
            "revision_count": 1,
            "review_feedback": "Approved.",
        }
    )
    monkeypatch.setattr(api_module, "run_research_workflow", workflow_mock)

    response = client.post("/research", json={"topic": "Renewable energy"})

    workflow_mock.assert_called_once_with("Renewable energy")
    assert response.status_code == 200
    assert response.json() == {
        "topic": "Renewable energy",
        "final_report": "Research report",
        "approved": True,
        "revision_count": 1,
        "review_feedback": "Approved.",
    }


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"topic": ""},
        {"topic": "AI"},
        {"topic": "x" * 501},
        {"topic": 42},
    ],
)
def test_research_endpoint_rejects_invalid_input(client, monkeypatch, payload):
    workflow_mock = Mock()
    monkeypatch.setattr(api_module, "run_research_workflow", workflow_mock)

    response = client.post("/research", json=payload)

    assert response.status_code == 422
    workflow_mock.assert_not_called()


def test_research_endpoint_returns_server_error_when_workflow_fails(
    client, monkeypatch
):
    workflow_mock = Mock(side_effect=RuntimeError("workflow failure"))
    monkeypatch.setattr(api_module, "run_research_workflow", workflow_mock)

    response = client.post("/research", json={"topic": "Renewable energy"})

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Research failed. Check the server terminal for details."
    }
