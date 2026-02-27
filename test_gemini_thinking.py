from google import genai
from google.genai import types

client = genai.Client(
    vertexai=True,
    project="statg529300220261-01d2",
    location="global",
)

model = "gemini-3.1-pro-preview"

# Use thinking mode with MEDIUM level
response = client.models.generate_content(
    model=model,
    contents="What is the sum of the first 50 prime numbers?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="MEDIUM",
        ),
    ),
)

# Print the thinking process and the final answer
for part in response.candidates[0].content.parts:
    if part.thought:
        print("=== MODEL THINKING ===")
        print(part.text)
        print("=== END THINKING ===\n")
    else:
        print("=== FINAL ANSWER ===")
        print(part.text)
