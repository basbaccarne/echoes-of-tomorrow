from openai import OpenAI

client = OpenAI(api_key="jouw-api-key")

def chat_openai(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Snel en goedkoop
        messages=[
            {"role": "system", "content": "Je bent een behulpzame assistent in een Belgische bibliotheek. Antwoord altijd in het Nederlands."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

answer = chat_openai("Hallo, hoe gaat het?")
print(answer)