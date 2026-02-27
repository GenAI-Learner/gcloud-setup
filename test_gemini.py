from google import genai

# Initialize the client for Vertex AI
client = genai.Client(
    vertexai=True,
    project="statg529300220261-01d2",
    location="global",
)

# Send a simple text prompt
model = "gemini-3.1-pro-preview"
response = client.models.generate_content(
    model=model,
    contents="Explain what generative AI is in 3 sentences.",
)

print(response.text)
