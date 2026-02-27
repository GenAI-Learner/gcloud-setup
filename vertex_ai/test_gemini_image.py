from google import genai
from google.genai import types

# Initialize the client for Vertex AI
client = genai.Client(
    vertexai=True,
    project="statg529300220261-01d2",
    location="global",
)

# Use a sample image from Google Cloud Storage
IMAGE_URI = "gs://generativeai-downloads/images/scones.jpg"

model = "gemini-3.1-pro-preview"
response = client.models.generate_content(
    model=model,
    contents=[
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(file_uri=IMAGE_URI, mime_type="image/jpeg"),
                types.Part.from_text(text="Describe this image in detail."),
            ],
        )
    ],
)

print(response.text)
