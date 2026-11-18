
from llm_config import get_llm


def analysis_agent(state: dict) -> dict:
    print("\n[Analysis Agent] Analyzing research...")

    llm = get_llm()

    research_notes = state["research_notes"]
    sources = state["sources"]

    source_context = ""

    for source in sources:
        source_context += f"""
Source: {source['source_id']}
Title: {source['title']}
URL: {source['url']}
Content: {source['content']}
---
"""

    prompt = f"""
You are an expert research analyst.

Research Topic:
{state['topic']}

Research Findings:
{research_notes}

Available Sources:
{source_context}

Your responsibilities:

1. Identify the most important findings.
2. Identify trends and patterns.
3. Compare information across sources.
4. Identify contradictions.
5. Identify knowledge gaps.
6. Separate verified evidence from assumptions.
7. Preserve source IDs for important claims.

Do not invent facts or sources.

Return a structured analysis with these headings:

- Executive Findings
- Major Trends
- Important Insights
- Contradictions
- Knowledge Gaps
- Key Conclusions
"""

    response = llm.invoke(prompt)

    print("[Analysis Agent] Analysis completed.")

    return {
        "analysis": response.content
    }
