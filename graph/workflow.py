
from langgraph.graph import StateGraph, START, END

from graph.state import ResearchState

from agents.research_agent import research_agent
from agents.analysis_agent import analysis_agent
from agents.content_agent import content_agent
from agents.review_agent import review_agent


MAX_REVISIONS = 2


# ---------------------------------
# Node 1: Research Agent
# ---------------------------------

def research_node(state: ResearchState):

    result = research_agent(state["topic"])

    return {
        "sources": result["sources"],
        "research_notes": result["research_notes"]
    }


# ---------------------------------
# Node 2: Analysis Agent
# ---------------------------------

def analysis_node(state: ResearchState):

    return analysis_agent(state)


# ---------------------------------
# Node 3: Content Agent
# ---------------------------------

def content_node(state: ResearchState):

    return content_agent(state)


# ---------------------------------
# Node 4: Quality Review Agent
# ---------------------------------

def review_node(state: ResearchState):

    return review_agent(state)


# ---------------------------------
# Conditional Routing
# ---------------------------------

def route_after_review(state: ResearchState):

    if state["approved"]:
        print("\n[Workflow] Report approved!")
        return "finish"

    if state["revision_count"] >= MAX_REVISIONS:
        print("\n[Workflow] Maximum revisions reached.")
        return "finish"

    print("\n[Workflow] Sending report for revision...")
    return "revise"


# ---------------------------------
# Build LangGraph
# ---------------------------------

builder = StateGraph(ResearchState)

builder.add_node("research", research_node)
builder.add_node("analysis", analysis_node)
builder.add_node("content", content_node)
builder.add_node("review", review_node)

builder.add_edge(START, "research")

builder.add_edge("research", "analysis")
builder.add_edge("analysis", "content")
builder.add_edge("content", "review")

builder.add_conditional_edges(
    "review",
    route_after_review,
    {
        "revise": "content",
        "finish": END
    }
)

# Compile workflow
research_workflow = builder.compile()


# ---------------------------------
# Run Workflow
# ---------------------------------

def run_research_workflow(topic: str):

    initial_state = {
        "topic": topic,
        "sources": [],
        "research_notes": "",
        "analysis": "",
        "draft_report": "",
        "review_feedback": "",
        "approved": False,
        "revision_count": 0,
        "final_report": ""
    }

    result = research_workflow.invoke(initial_state)

    return result
