
import os
from typing import Optional

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

_llm: Optional[ChatGroq] = None

def get_llm():
    """Return the configured Groq language model."""
    global _llm
    if _llm is None:
        _llm = ChatGroq(
            model=os.getenv("MODEL_NAME", "openai/gpt-oss-120b"),
            temperature=0.3,
            max_tokens=2048,
            api_key=os.getenv("GROQ_API_KEY")
        )
    return _llm
