
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from graph.workflow import run_research_workflow


def main():

    topic = input("\nEnter your research topic: ").strip()

    if not topic:
        print("Research topic cannot be empty.")
        return

    print("\nStarting Multi-Agent Research Assistant...")
    print("=" * 60)

    result = run_research_workflow(topic)

    print("\n" + "=" * 60)
    print("FINAL RESEARCH REPORT")
    print("=" * 60)

    print(result["final_report"])

    print("\n" + "=" * 60)
    print("QUALITY REVIEW")
    print("=" * 60)

    print(result["review_feedback"])

    print("\nReport approved:", result["approved"])
    print("Revisions:", result["revision_count"])

    # Save report
    output_dir = PROJECT_ROOT / "outputs"
    output_dir.mkdir(exist_ok=True)

    report_path = output_dir / "research_report.md"
    report_path.write_text(
        result["final_report"],
        encoding="utf-8"
    )

    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
