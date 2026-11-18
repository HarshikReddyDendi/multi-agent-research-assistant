
import re
from llm_config import get_llm


def review_agent(state: dict) -> dict:
    print("\n[Quality Review Agent] Reviewing report...")

    revision_count = state["revision_count"]
    llm = get_llm()

    prompt = f"""
You are a strict research quality reviewer.

Research Topic:
{state['topic']}

Available Research:
{state['research_notes']}

Available Sources:
{state['sources']}

Generated Report:
{state['draft_report']}

Evaluate the report on:

1. Relevance to the research topic.
2. Completeness.
3. Logical organization.
4. Consistency with research findings.
5. Citation and source attribution.
6. Unsupported or potentially fabricated claims.
7. Clarity and professionalism.

IMPORTANT:
- Compare claims against the supplied research evidence.
- Do not approve unsupported claims.
- Do not assume a URL proves a claim.
- Identify missing or incorrect source references.

Approval criteria:
Approve only if the report is sufficiently complete,
coherent, and supported by the supplied evidence.

Return your response in exactly this format:

APPROVED: YES or NO

FEEDBACK:
Explain your evaluation and list required corrections.
"""

    response = llm.invoke(prompt)
    review = response.content.strip()

    # Detect approval status reliably
    match = re.search(
        r"(?im)^\s*APPROVED:\s*(YES|NO)\s*$",
        review
    )

    approved = bool(
        match and match.group(1).upper() == "YES"
    )

    # Increase revision count when rejected
    if not approved:
        revision_count += 1

    print(f"[Quality Review Agent] Approved: {approved}")

    return {
        "approved": approved,
        "review_feedback": review,
        "revision_count": revision_count
    }
