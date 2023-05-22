import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

system_prompt = "You are an AI Assistant"

prompt = [
    {"role": "system", "content": system_prompt},
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=prompt,
    temperature=0.5,
)

print(response["choices"][0]["message"]["content"])
