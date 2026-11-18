
import sys
from pathlib import Path

# Add project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from agents.research_agent import research_agent


def main():

    topic = input("\nEnter your research topic: ").strip()

    if not topic:
        print("Please enter a research topic.")
        return

    result = research_agent(topic)

    print("\n" + "=" * 60)
    print("RESEARCH REPORT")
    print("=" * 60)

    print("\nTOPIC:")
    print(result["topic"])

    print("\nRESEARCH FINDINGS:")
    print(result["research_notes"])

    print("\nSOURCES:")

    for source in result["sources"]:
        print(f"\n[{source['source_id']}] {source['title']}")
        print(f"URL: {source['url']}")
        print(f"Relevance: {source['score']:.3f}")


if __name__ == "__main__":
    main()
