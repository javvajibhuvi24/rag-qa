import re
from pathlib import Path


def load_chunks(folder: str, max_chars: int = 300) -> list[dict]:
    chunks = []
    for path in Path(folder).glob("*.txt"):
        text = path.read_text(encoding="utf-8")
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        current = ""
        for sentence in sentences:
            if current and len(current) + len(sentence) + 1 > max_chars:
                chunks.append({"source": path.name, "text": current})
                current = sentence
            else:
                current = f"{current} {sentence}".strip()
        if current:
            chunks.append({"source": path.name, "text": current})
    return chunks