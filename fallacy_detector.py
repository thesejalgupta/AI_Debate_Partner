import re
from typing import Optional, Tuple

class FallacyDetector:
    """
    Simple rule-based fallacy detector for debate arguments.
    Detects ad hominem, strawman, and hasty generalization.
    """

    def __init__(self):
        # Pre-compiled regex patterns for speed
        self.ad_hominem_patterns = [
            re.compile(r"\b(you are|you're|your|you\s+.*\s+stupid|idiot|dumb)\b", re.IGNORECASE),
            re.compile(r"\b(weak|liar|fraud)\b", re.IGNORECASE),
        ]
        self.strawman_patterns = [
            re.compile(r"\b(you said .* not true|you only care about|you think.*but)\b", re.IGNORECASE),
            re.compile(r"\b(so you are saying|so you mean|makes me think you believe)\b", re.IGNORECASE),
        ]
        self.hasty_generalization_patterns = [
            re.compile(r"\b(all|every|always|never|nobody|everybody)\b.*\b(are|is|do|have)\b", re.IGNORECASE),
            re.compile(r"\b(.*\b(mentions|examples).*\b(one|a few|a couple)\b.*)\b", re.IGNORECASE),
        ]

    def detect_fallacy(self, user_input: str) -> Tuple[Optional[str], str, str]:
        """
        Detect fallacy in a user argument.

        Returns:
            fallacy_type (str or None): One of 'Ad Hominem', 'Strawman', 'Hasty Generalization', or None.
            explanation (str): What was detected.
            suggestion (str): Advice to improve the argument.
        """
        text = user_input.strip()

        # 1. Ad Hominem
        for p in self.ad_hominem_patterns:
            if p.search(text):
                return (
                    "Ad Hominem",
                    "This statement attacks the speaker rather than addressing the argument.",
                    "Focus on reasoning and evidence instead of personal attacks."
                )

        # 2. Strawman
        for p in self.strawman_patterns:
            if p.search(text):
                return (
                    "Strawman",
                    "This seems to misrepresent or oversimplify the opposing argument.",
                    "Restate the opponent's position accurately and then respond to that."
                )

        # 3. Hasty Generalization
        for p in self.hasty_generalization_patterns:
            if p.search(text):
                return (
                    "Hasty Generalization",
                    "This conclusion is too broad given the limited evidence.",
                    "Use more representative data and avoid sweeping claims."
                )

        # No recognized pattern
        return (
            None,
            "No clear fallacy detected by current rules.",
            "Provide concrete evidence and precise reasoning for stronger argument quality."
        )


if __name__ == "__main__":
    detector = FallacyDetector()

    test_sentences = [
        "You're dumb for thinking climate change is real.",
        "So you are saying we should do nothing and standards matter less.",
        "Everyone always lies when it comes to politics.",
        "I believe we need stronger regulation based on existing reports."
    ]

    for sentence in test_sentences:
        fallacy, explanation, suggestion = detector.detect_fallacy(sentence)
        print(f"Input: {sentence}")
        print(f"Fallacy: {fallacy}")
        print(f"Explanation: {explanation}")
        print(f"Suggestion: {suggestion}\n")
