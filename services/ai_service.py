from openai import OpenAI
from core.settings import settings

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=settings.GROQ_API_KEY
)


async def get_ai_response(message: str):
    if len(message) > 500:
        return "Message is too long, make it short"
    response = client.chat.completions.create(
        model="allam-2-7b",
        messages=[{"role": "system", "content": "You must answer the user query in very simple words"}, {"role": "user", "content": message}]
    )
    return response.choices[0].message.content