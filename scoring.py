import re
from typing import Dict

class DebateScorer:
    """
    Simple debate scoring based on clarity, relevance, and argument strength.
    Uses lightweight heuristics and is easy to integrate with DebateEngine.
    """

    def __init__(self):
        # Keywords that indicate relevance to debate topics.
        self.relevance_keywords = {
            'evidence', 'study', 'data', 'research', 'fact', 'reason', 'policy', 'argument', 'support', 'cause', 'impact'
        }

    def score_argument(self, user_input: str) -> Dict[str, object]:
        """
        Score an argument by clarity, relevance, and strength.

        Args:
            user_input (str): The argument to score.

        Returns:
            Dict[str, object]: keys: clarity, relevance, strength, total, feedback.
        """
        text = user_input.strip()

        # Clarity based on length and sentence structure
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        sentence_count = len(sentences)
        word_count = len(text.split())

        if word_count == 0:
            clarity = 0
        elif word_count < 8:
            clarity = 4
        elif word_count < 20:
            clarity = 6
        elif word_count < 35:
            clarity = 8
        else:
            clarity = 10

        # Relevance based on keyword hits
        tokens = re.findall(r"\w+", text.lower())
        keyword_hits = sum(1 for t in tokens if t in self.relevance_keywords)
        relevance = min(10, keyword_hits * 2)

        # Strength based on structure and evidence language
        strength = 0
        if sentence_count >= 2:
            strength += 4
        elif sentence_count == 1:
            strength += 2

        evidence_phrases = ['because', 'therefore', 'thus', 'consequently', 'evidence', 'data', 'research', 'fact']
        evidence_score = sum(1 for p in evidence_phrases if p in text.lower())
        strength += min(6, evidence_score * 2)
        strength = min(10, strength)

        total = clarity + relevance + strength

        feedback_msgs = []
        if clarity < 6:
            feedback_msgs.append('Clarify your point with more complete sentences.')
        if relevance < 6:
            feedback_msgs.append('Add more topic-specific evidence or keywords.')
        if strength < 6:
            feedback_msgs.append('Use stronger reasoning and explicit evidence terms.')
        if not feedback_msgs:
            feedback = 'Strong argument: clear, relevant, and robust.'
        else:
            feedback = ' '.join(feedback_msgs)

        return {
            'clarity': clarity,
            'relevance': relevance,
            'strength': strength,
            'total': total,
            'feedback': feedback
        }

