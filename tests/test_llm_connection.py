

import sys
from pathlib import Path

# Add project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from llm_config import get_llm


def main():
    print("Connecting to Groq...")

    llm = get_llm()

    response = llm.invoke(
        "Explain what an AI research assistant is in 3 sentences."
    )

    print("\nConnection successful!")
    print("\nLLM RESPONSE:\n")
    print(response.content)


if __name__ == "__main__":
    main()
