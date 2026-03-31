import re
from memory import ConversationMemory
from chatbot import get_generator
from fallacy_detector import FallacyDetector

class DebateEngine:
    """
    A debate engine that generates counter-arguments using AI.
    The AI automatically takes the opposite side of the user.
    Includes memory of past exchanges to provide contextual responses.
    """

    def __init__(self, topic: str, user_side: str, personality: str = 'calm', difficulty: str = 'medium', ai_role: str = 'opponent', debug: bool = False) -> None:
        """
        Initializes the debate engine.

        Args:
            topic (str): The debate topic.
            user_side (str): The user's position ('for' or 'against').
            personality (str): AI style ('aggressive', 'calm', 'witty').
            difficulty (str): Argument complexity ('easy', 'medium', 'hard').
            ai_role (str): AI role ('opponent' or 'support').
            debug (bool): Enable debug prints. Default is False.
        """
        self.topic = topic
        self.user_side = user_side
        self.personality = personality.lower()
        self.difficulty = difficulty.lower()
        self.ai_role = ai_role.lower()
        self.debug = debug

        if self.ai_role == 'support':
            self.ai_side = user_side
        else:
            self.ai_side = "against" if user_side == "for" else "for"

        # Reuse the shared model pipeline from ChatBot to avoid double loading
        self.generator = get_generator()
        # Initialize memory to store conversation exchanges
        self.memory = ConversationMemory(max_exchanges=5)
        # Initialize fallacy detector to assess user arguments
        self.fallacy_detector = FallacyDetector()

    def generate_response(self, user_argument: str) -> str:
        """
        Generates a structured response countering the user's argument.
        Uses conversation memory to refer to previous arguments and avoid repetition.

        Args:
            user_argument (str): The user's argument.

        Returns:
            str: A formatted response with Claim, Reason, and Example.
        """
        # Detect fallacy in user argument
        fallacy_type, explanation, suggestion = self.fallacy_detector.detect_fallacy(user_argument)

        # Get context from previous exchanges
        context = self.memory.get_context()
        
        # Debug: Show memory context and fallacy info being used
        if self.debug:
            print("\n[DEBUG] Memory Context:")
            print(context)
            print("[DEBUG] End of Context\n")
            print("[DEBUG] Fallacy Detection:")
            print(f"Detected: {fallacy_type or 'None'}")
            print(f"Explanation: {explanation}")
            print(f"Suggestion: {suggestion}\n")

        # Personality prompt section
        personality_map = {
            'aggressive': 'Answer sharply and assertively with a challenging tone.',
            'calm': 'Answer respectfully and balanced in tone.',
            'witty': 'Answer cleverly with a light humorous tone.'
        }
        personality_direction = personality_map.get(self.personality, personality_map['calm'])

        # Difficulty prompt section
        difficulty_map = {
            'easy': 'Keep the argument simple and straightforward.',
            'medium': 'Use moderate reasoning and moderately complex logic.',
            'hard': 'Use advanced reasoning with strong nuanced arguments and evidence.'
        }
        difficulty_direction = difficulty_map.get(self.difficulty, difficulty_map['medium'])

        # Craft a prompt that includes conversation history, personality, difficulty, and context
        prompt = f"""Topic: {self.topic}
You are arguing {self.ai_side} the topic.
Personality: {self.personality.capitalize()} ({personality_direction})
Difficulty: {self.difficulty.capitalize()} ({difficulty_direction})

Previous Discussion:
{context}

Current User Argument: {user_argument}

Instructions:
- Answer in clear, correct English only.
- Make the response topic-related (mention sustainability/environment if that is the topic).
- If ai_role is support, make a supporting argument; if opponent, make a counter-argument.
- Must be logically coherent and brief.
- Fallback always includes a structured response if generation is bad.

Provide a response that follows this exact format:
1. Claim: [Your main claim]
2. Reason: [Why this claim is valid]
3. Example: [A specific example]

Response:
1. Claim: """

        # Generate response
        response = self.generator(prompt, max_length=200, num_return_sequences=1, temperature=0.5, do_sample=True)

        # Extract the generated text
        generated_text = response[0]['generated_text']
        
        # Extract only the counter-argument part (after the prompt)
        if prompt in generated_text:
            formatted_response = "1. Claim: " + generated_text[len(prompt):].strip()
        else:
            formatted_response = generated_text.strip()

        # Ensure format starts with "1. Claim:" and is in English 
        if not formatted_response.startswith("1.") or re.search(r"[^\x00-\x7F]", formatted_response):
            formatted_response = (
                "1. Claim: Sustainability protects natural ecosystems and community health.\n"
                "2. Reason: Environment-friendly practices reduce pollution and resource depletion, improving long-term resilience.\n"
                "3. Example: Replacing fossil fuels with renewables in cities cuts emissions and preserves biodiversity."
            )

        # Additional simple topic check and fallback if response is content-irrelevant
        topic_lower = self.topic.lower()
        response_lower = formatted_response.lower()
        if topic_lower and all(key not in response_lower for key in topic_lower.split() if len(key) > 3):
            # build a generic topic-aware fallback using the current topic keywords
            main_topic = self.topic.split(':')[-1].strip() if ':' in self.topic else self.topic.strip()
            main_topic = main_topic if main_topic else self.topic
            formatted_response = (
                f"1. Claim: The discussion about {main_topic} is important for society today.\n"
                f"2. Reason: Understanding and improving {main_topic} helps reduce harm and increase benefits for people.\n"
                f"3. Example: Effective policies and awareness campaigns around {main_topic} can shape better outcomes."
            )

        # Debug: Show generated response
        if self.debug:
            print(f"[DEBUG] Generated Response:\n{formatted_response}\n")
        
        # Add to memory for future context
        self.memory.add_to_memory(user_argument, formatted_response)
        
        if self.debug:
            print(f"[DEBUG] Exchange added to memory. Total exchanges: {len(self.memory.get_exchanges())}\n")

        # Add fallacy feedback to output
        fallacy_summary = fallacy_type if fallacy_type else "No major fallacy detected"
        final_output = (
            f"AI Debate Response:\n{formatted_response}\n\n"
            f"Fallacy detected: {fallacy_summary}\n"
            f"Explanation: {explanation}\n"
            f"Suggestion: {suggestion}"
        )

        return final_output

    def clear_memory(self) -> None:
        """Clears the conversation memory."""
        self.memory.clear_memory()
        if self.debug:
            print("[DEBUG] Memory cleared.\n")
