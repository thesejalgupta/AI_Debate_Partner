#!/usr/bin/env python3
"""Test script for DebateScorer."""

from scoring import DebateScorer

if __name__ == "__main__":
    scorer = DebateScorer()

    examples = [
        "Because there is clear data from research, we should adopt this policy.",
        "People always do this and it's bad.",
        "Strong evidence shows 80% improvement in tests when guidelines are followed.",
        "I think it's okay."
    ]

    for text in examples:
        scores = scorer.score_argument(text)
        print(f"Input: {text}")
        print(f"Clarity: {scores['clarity']}, Relevance: {scores['relevance']}, Strength: {scores['strength']}, Total: {scores['total']}")
        print(f"Feedback: {scores['feedback']}\n")