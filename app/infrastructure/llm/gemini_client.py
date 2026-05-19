# app/infrastructure/llm/gemini_client.py

from groq import Groq
from app.core.config import settings
from app.core.logger import get_logger
from app.core.exceptions import IntentParsingError

logger = get_logger(__name__)


class LLMClient:

    def __init__(self):
        self._client = Groq(api_key=settings.groq_api_key)
        logger.info(f"Groq client ready | model: {settings.llm_model}")

    def generate(self, prompt: str) -> str:
        try:
            response = self._client.chat.completions.create(
                model=settings.llm_model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.llm_max_tokens,
                temperature=settings.llm_temperature,
            )
            result = response.choices[0].message.content.strip()
            logger.debug(f"Groq response: {result[:100]}...")
            return result

        except Exception as e:
            logger.error(f"Groq call failed: {e}")
            raise IntentParsingError(
                message="response not recieved from Groq",
                details={"error": str(e)},
            )


gemini_client = LLMClient()