import time

from answer import answer
from eval import ANSWERABLE

for question, phrase in ANSWERABLE:
    reply = answer(question)
    print(f"Q: {question}\nexpected fact: {phrase}\nA: {reply}\n")
    time.sleep(4)