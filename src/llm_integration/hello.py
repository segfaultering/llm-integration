from dotenv import load_dotenv
from google.genai import Client, types

load_dotenv()

with Client() as client:
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=types.Part.from_text(text="Reply with exactly one word: ready"),
        config=types.GenerateContentConfig(temperature=0, top_p=0.95, top_k=20),
    )

print(response.text)
