from collections import deque
from typing import List, Tuple

class ConversationMemory:
    """
    A lightweight memory module that stores the last 5 debate exchanges.
    Each exchange includes the user's argument and the AI's response.
    """

    def __init__(self, max_exchanges: int = 5) -> None:
        """
        Initializes the conversation memory.

        Args:
            max_exchanges (int): Maximum number of exchanges to store. Default is 5.
        """
        self.max_exchanges = max_exchanges
        # Use deque for efficient removal of oldest items when limit is reached
        self.exchanges: deque = deque(maxlen=max_exchanges)

    def add_to_memory(self, user_input: str, ai_response: str) -> None:
        """
        Adds an exchange (user input and AI response) to memory.
        Automatically removes the oldest exchange if max_exchanges is exceeded.

        Args:
            user_input (str): The user's argument.
            ai_response (str): The AI's response.
        """
        exchange = {
            "user": user_input,
            "ai": ai_response
        }
        # deque automatically removes oldest item when maxlen is exceeded
        self.exchanges.append(exchange)

    def get_context(self) -> str:
        """
        Returns a formatted string of all past exchanges for context.

        Returns:
            str: Formatted conversation history.
        """
        if not self.exchanges:
            return "No previous exchanges."

        context = "=== Conversation History ===\n"
        for idx, exchange in enumerate(self.exchanges, 1):
            context += f"\nExchange {idx}:\n"
            context += f"User: {exchange['user']}\n"
            context += f"AI: {exchange['ai']}\n"
            context += "-" * 40 + "\n"

        return context

    def clear_memory(self) -> None:
        """Clears all stored exchanges."""
        self.exchanges.clear()

    def get_exchanges(self) -> List[Tuple[str, str]]:
        """
        Returns all stored exchanges as a list of tuples.

        Returns:
            List[Tuple[str, str]]: List of (user_input, ai_response) tuples.
        """
        return [(exchange["user"], exchange["ai"]) for exchange in self.exchanges]
