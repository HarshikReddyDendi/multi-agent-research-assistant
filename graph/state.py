
from typing import TypedDict


class ResearchState(TypedDict):
    # User's research topic
    topic: str

    # Research Agent output
    sources: list
    research_notes: str

    # Analysis Agent output
    analysis: str

    # Content Agent output
    draft_report: str

    # Quality Review Agent output
    review_feedback: str
    approved: bool

    # Revision management
    revision_count: int

    # Final output
    final_report: str
