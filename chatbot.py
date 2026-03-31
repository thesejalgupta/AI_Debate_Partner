from transformers import pipeline

# Shared pipeline to avoid loading the model multiple times.
_shared_generator = None

def get_generator():
    """Return a singleton text-generation pipeline to avoid duplicate model loads."""
    global _shared_generator
    if _shared_generator is None:
        print("Loading AI model...")
        _shared_generator = pipeline("text-generation", model="gpt2")
        print("Model loaded successfully!\n")
    return _shared_generator

class ChatBot:
    """
    A simple chatbot class that uses Hugging Face's GPT-2 model for text generation.
    """

    def __init__(self) -> None:
        """
        Initializes the chatbot by reusing the shared GPT-2 model pipeline.
        """
        self.generator = get_generator()

    def get_response(self, user_input: str) -> str:
        """
        Generates a response based on the user's input.

        Args:
            user_input (str): The input text from the user.

        Returns:
            str: The generated response text.
        """
        response = self.generator(user_input, max_length=50, num_return_sequences=1)
        return response[0]['generated_text']
