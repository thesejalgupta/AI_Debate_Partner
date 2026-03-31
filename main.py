from chatbot import ChatBot
from debate_engine import DebateEngine

def chat_mode(bot: ChatBot) -> None:
    """
    Normal chat mode where the user converses with the AI chatbot.

    Args:
        bot (ChatBot): An instance of the ChatBot class.
    """
    print("\n--- Chat Mode ---")
    print("Type 'exit' to return to main menu\n")

    while True:
        user_input = input("You: ")

        # Check for exit command
        if user_input.lower() in ("exit", "quit"):
            print("Returning to main menu...\n")
            break

        # Get response from the chatbot
        response = bot.get_response(user_input)
        print("AI:", response)


def debate_mode() -> None:
    """
    Debate mode where the user debates with the AI on a chosen topic.
    The AI automatically takes the opposite side of the user.
    Uses conversation memory to track exchanges and provide contextual responses.
    """
    print("\n--- Debate Mode ---")

    # Get topic from user
    topic = input("\nEnter the debate topic: ").strip()
    if not topic:
        print("Topic cannot be empty. Returning to main menu...\n")
        return

    # Get user's side
    print("Choose your side:")
    print("1. For (pro)")
    print("2. Against (con)")
    side_choice = input("Enter your choice (1 or 2): ").strip()

    if side_choice == "1":
        user_side = "for"
    elif side_choice == "2":
        user_side = "against"
    else:
        print("Invalid choice. Returning to main menu...\n")
        return

    # Choose personality style
    print("Choose AI personality style:")
    print("1. Aggressive")
    print("2. Calm")
    print("3. Witty")
    personality_choice = input("Enter your choice (1, 2, or 3): ").strip()

    if personality_choice == "1":
        personality = "aggressive"
    elif personality_choice == "2":
        personality = "calm"
    elif personality_choice == "3":
        personality = "witty"
    else:
        print("Invalid choice, defaulting to calm.\n")
        personality = "calm"

    # Choose difficulty level
    print("\nChoose difficulty level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    difficulty_choice = input("Enter your choice (1, 2, or 3): ").strip()

    if difficulty_choice == "1":
        difficulty = "easy"
    elif difficulty_choice == "2":
        difficulty = "medium"
    elif difficulty_choice == "3":
        difficulty = "hard"
    else:
        print("Invalid choice, defaulting to medium.\n")
        difficulty = "medium"

    # Initialize the debate engine
    engine = DebateEngine(topic, user_side, personality=personality, difficulty=difficulty, debug=False)
    print(f"\nTopic: {topic}")
    print(f"Your side: {user_side}")
    print(f"AI side: {engine.ai_side} ({engine.personality}, {engine.difficulty})")
    print("\nCommands:")
    print("  Type your argument and press Enter")
    print("  Type 'memory' to view conversation history")
    print("  Type 'exit' to return to main menu\n")

    # Debate loop
    while True:
        user_input = input("Your argument: ").strip()

        # Check for special commands
        if user_input.lower() in ("exit", "quit"):
            print("Returning to main menu...\n")
            break
        
        # Show memory/conversation history
        if user_input.lower() == "memory":
            print("\n" + engine.memory.get_context())
            print("(Tip: Each exchange is used by the AI to provide contextual responses)\n")
            continue

        if not user_input:
            print("Argument cannot be empty. Try again.\n")
            continue

        # Generate AI response (memory context is included in the prompt)
        ai_response = engine.generate_response(user_input)
        print("\nAI Counter-argument:")
        print(ai_response)
        print()


def main() -> None:
    """
    Main function displaying the menu and handling mode selection.
    """
    # Create a single instance of ChatBot (reused across sessions)
    bot = ChatBot()

    print("=" * 50)
    print("AI Debate Partner")
    print("=" * 50)

    # Main menu loop
    while True:
        print("\nMain Menu:")
        print("1. Normal Chat")
        print("2. Debate Mode")
        print("3. Exit")

        choice = input("\nEnter your choice (1, 2, or 3): ").strip()

        if choice == "1":
            chat_mode(bot)
        elif choice == "2":
            debate_mode()
        elif choice == "3":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()