import time

from answer import answer
from eval import UNANSWERABLE

REFUSALS = ("don't have that information", "do not have that information",
            "don't know", "do not know", "does not contain", "doesn't contain")


def refused(text: str) -> bool:
    return any(r in text.lower() for r in REFUSALS)


for q in UNANSWERABLE:
    a = answer(q)
    print(f"{'OK  ' if refused(a) else 'LEAK'} {q}\n     {a[:100]}")
    time.sleep(4)