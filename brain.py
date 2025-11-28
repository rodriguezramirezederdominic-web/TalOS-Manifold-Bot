import openai
from config import OPENAI_API_KEY

class MarketBrain:
    def __init__(self):
        if not OPENAI_API_KEY:
            print("Warning: No OpenAI Key found. Brain is lobotomized (random mode).")
            self.client = None
        else:
            self.client = openai.OpenAI(api_key=OPENAI_API_KEY)

    def analyze_market(self, question, description, current_prob):
        """
        Uses an LLM to analyze the market question and return a probability.
        """
        if not self.client:
            return 0.5 # Fallback if no API key

        # The system prompt is kept in English for better GPT model performance
        system_prompt = (
            "You are a superforecaster for prediction markets. "
            "You provide calibrated probabilities for binary events. "
            "You rely on logic, world knowledge, and base rates. "
            "Output strictly a number between 0.01 and 0.99."
        )

        user_prompt = f"""
        Market Question: {question}
        Description: {description}
        Current Market Probability: {current_prob}

        Task:
        1. Identify the reference class for this event.
        2. Analyze reasons why the answer might be YES.
        3. Analyze reasons why the answer might be NO.
        4. Synthesize this into a final probability estimate.

        Return ONLY the probability as a float.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4", # Or gpt-4-turbo / gpt-3.5-turbo
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2, # Low temperature for analytical consistency
            )
            content = response.choices[0].message.content.strip()
            # Clean string to get only the float number
            prob = float(''.join(c for c in content if c.isdigit() or c == '.'))
            return max(0.01, min(0.99, prob))
            
        except Exception as e:
            print(f"Brain Error: {e}")
            return current_prob # Neutralize if error (do not bet)