from openai import AsyncOpenAI
from app.core.config import ai_config
import logging

logger = logging.getLogger(__name__)


class AIContentService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=ai_config.openai_api_key)
        self.default_model = ai_config.openai_model
        self.default_max_tokens = ai_config.openai_max_tokens
        self.default_temperature = ai_config.openai_temperature

    async def generate_content(
            self,
            prompt: str,
            document_type: str,
            max_tokens: int = None,
            temperature: float = None
    ) -> str:
        """
        Генерация контента через OpenAI API
        """
        try:
            max_tokens = max_tokens or self.default_max_tokens
            temperature = temperature or self.default_temperature

            system_prompts = {
                "article": "Ты профессиональный копирайтер. Создай качественную, структурированную статью на заданную тему.",
                "social_media": "Ты SMM специалист. Создай engaging пост для социальных сетей.",
                "email": "Ты email маркетолог. Напиши эффективное email письмо.",
                "ad_copy": "Ты креативный директор. Создай продающий рекламный текст.",
                "product_description": "Ты продуктовый маркетолог. Напиши compelling описание продукта."
            }

            system_prompt = system_prompts.get(document_type, "Ты помощник по созданию контента.")

            response = await self.client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"AI generation error: {str(e)}")
            raise Exception(f"AI service error: {str(e)}")


# Глобальный экземпляр сервиса
ai_service = AIContentService()