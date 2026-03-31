#!/usr/bin/env python3
"""
Simple test script for the DebateEngine module.
"""

from debate_engine import DebateEngine

def test_debate_engine():
    """Test the DebateEngine with a sample topic and arguments."""
    # Create a debate engine
    engine = DebateEngine(topic="Should social media be banned?", user_side="for")

    print("Topic:", engine.topic)
    print("User side:", engine.user_side)
    print("AI side:", engine.ai_side)
    print()

    # Test with a user argument
    user_arg = "Social media connects people and spreads information quickly."
    print("User argument:", user_arg)
    print()

    response = engine.generate_response(user_arg)
    print("AI Response:")
    print(response)

if __name__ == "__main__":
    test_debate_engine()