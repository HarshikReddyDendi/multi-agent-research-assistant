from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from graph.workflow import run_research_workflow

app = FastAPI(
    title="Multi-Agent AI Research Assistant",
    description="An API powered by LangGraph and multiple AI agents.",
    version="1.0.0"
)


class ResearchRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="The topic to research"
    )


class ResearchResponse(BaseModel):
    topic: str
    final_report: str
    approved: bool
    revision_count: int
    review_feedback: str


@app.get("/")
def home():
    return {
        "message": "Multi-Agent AI Research Assistant API is running."
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/research", response_model=ResearchResponse)
def conduct_research(request: ResearchRequest):
    try:
        result = run_research_workflow(request.topic)

        return ResearchResponse(
            topic=result["topic"],
            final_report=result["final_report"],
            approved=result["approved"],
            revision_count=result["revision_count"],
            review_feedback=result["review_feedback"]
        )

    except Exception as error:
        print(f"[API Error] {error}")
        raise HTTPException(
            status_code=500,
            detail="Research failed. Check the server terminal for details."
        )