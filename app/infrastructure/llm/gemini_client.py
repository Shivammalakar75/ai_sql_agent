# app/infrastructure/llm/gemini_client.py

from groq import Groq
from app.shared.config import settings
from app.shared.constants import LLM_MODEL, LLM_MAX_TOKENS, LLM_TEMPERATURE
from app.shared.logger import get_logger
from app.shared.exceptions import IntentParsingError

logger = get_logger(__name__)


class LLMClient:

    def __init__(self):
        self._client = Groq(api_key=settings.groq_api_key)
        logger.info(f"Groq client ready | model: {LLM_MODEL}")

    def generate(self, prompt: str) -> str:
        try:
            response = self._client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=LLM_MAX_TOKENS,
                temperature=LLM_TEMPERATURE,
            )
            result = response.choices[0].message.content.strip()
            logger.debug(f"Groq response: {result[:100]}...")
            return result

        except Exception as e:
            logger.error(f"Groq call failed: {e}")
            raise IntentParsingError(
                message="Groq se response nahi aaya",
                details={"error": str(e)},
            )


# Naam same rakha taaki baaki koi file na badle
gemini_client = LLMClient()