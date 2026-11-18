
from llm_config import get_llm


def content_agent(state: dict) -> dict:
    print("\n[Content Agent] Generating research report...")

    llm = get_llm()

    prompt = f"""
You are a professional research report writer.

Research Topic:
{state['topic']}

Research Notes:
{state['research_notes']}

Analysis:
{state['analysis']}

Original Sources:
{state['sources']}

Previous Review Feedback:
{state['review_feedback']}

Revision Number:
{state['revision_count']}

Your responsibilities:

1. Create a professional research report.
2. Include an executive summary.
3. Organize findings into logical sections.
4. Include key insights and implications.
5. Mention limitations and uncertainties.
6. Add source references using source IDs such as [S1].
7. Never invent citations or unsupported facts.
8. Address the previous review feedback when revising.

Use this report structure:

# Research Report

## Executive Summary

## Introduction

## Key Research Findings

## Detailed Analysis

## Trends and Insights

## Challenges and Limitations

## Conclusion

## References

Write a clear, detailed, professional report.
"""

    response = llm.invoke(prompt)

    report = response.content

    print("[Content Agent] Report generated.")

    return {
        "draft_report": report,
        "final_report": report
    }
