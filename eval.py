import statistics

from retrieve import search

ANSWERABLE = [
    ("What documents are needed to apply?", "identity proof"),
    ("Do I need to show my payslips?", "salary slips"),
    ("When do I pay the processing fee?", "processing fee"),
    ("Can I repay the loan before the end?", "prepay the loan"),
    ("Is there a penalty for repaying early?", "prepayment charge"),
    ("What if I skip an installment?", "late fee"),
    ("Will a missed EMI hurt my credit score?", "credit score can be affected"),
    ("How old must I be to apply?", "21 years"),
    ("What is the shortest and longest loan duration?", "12 to 60 months"),
    ("How is interest calculated?", "reducing balance"),
    ("Can someone else apply with me?", "co-applicant"),
    ("How long does approval take?", "two to five working days"),
    ("Where can I see my loan statement?", "mobile app"),
    ("What credit score gets me a lower rate?", "above 750"),
    ("How is my EMI collected?", "deducted automatically"),
    ("Can I change my EMI date?", "once during the loan tenure"),
    ("When will I get the foreclosure letter?", "within seven days"),
    ("What do self-employed people need to submit?", "income tax returns"),
    ("How much loan can I get?", "monthly income and existing obligations"),
    ("What proof of address is required?", "address proof"),
]

UNANSWERABLE = [
    "What is the capital of France?",
    "Who won the last cricket world cup?",
    "How do I cook biryani?",
    "What is the weather in Hyderabad today?",
    "Can I get a home loan for a flat?",
    "What is the interest rate on a car loan?",
    "How do I open a savings account?",
    "What is the bank's customer care number?",
    "Which phone should I buy?",
    "Explain how photosynthesis works.",
]


def hit_at(k: int) -> float:
    hits = 0
    for question, phrase in ANSWERABLE:
        results = search(question, k)
        if any(phrase.lower() in c["text"].lower() for _, c in results):
            hits += 1
    return hits / len(ANSWERABLE)


def top_score(question: str) -> float:
    return search(question, 1)[0][0]


if __name__ == "__main__":
    print(f"hit@1: {hit_at(1):.0%}")
    print(f"hit@3: {hit_at(3):.0%}")

    good = [top_score(q) for q, _ in ANSWERABLE]
    bad = [top_score(q) for q in UNANSWERABLE]

    print(f"\nanswerable:   min {min(good):.2f}  median {statistics.median(good):.2f}  max {max(good):.2f}")
    print(f"unanswerable: min {min(bad):.2f}  median {statistics.median(bad):.2f}  max {max(bad):.2f}")

    thresholds = [round(0.30 + 0.05 * i, 2) for i in range(11)]
    rows = []
    print("\nthreshold  answerable kept  unanswerable blocked")
    for t in thresholds:
        kept = sum(s >= t for s in good) / len(good)
        blocked = sum(s < t for s in bad) / len(bad)
        rows.append((t, kept, blocked))
        print(f"{t:.2f}       {kept:>6.0%}           {blocked:>6.0%}")

    candidates = [r for r in rows if r[1] >= 0.95]
    if candidates:
        best = max(candidates, key=lambda r: (r[2], -r[0]))
        print(f"\nSuggested threshold: {best[0]:.2f} "
              f"(keeps {best[1]:.0%}, blocks {best[2]:.0%})")
    else:
        print("\nNo threshold keeps 95% of answerable questions.")

    print("\nMissed at top-1:")
    for question, phrase in ANSWERABLE:
        top = search(question, 1)[0]
        if phrase.lower() not in top[1]["text"].lower():
            print(f"  {question}\n    got: {top[1]['text'][:80]}")

    print("\nUnanswerable questions by top score:")
    for q, s in sorted(zip(UNANSWERABLE, bad), key=lambda x: -x[1]):
        print(f"  {s:.2f}  {q}")