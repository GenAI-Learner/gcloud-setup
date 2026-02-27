# Gemini 3.1 Pro Preview — Vertex AI Tutorial

A step-by-step guide to using Google's **Gemini 3.1 Pro Preview** model via Vertex AI, both through the API (curl) and the Python Gen AI SDK.

---

## Table of Contents

1. [Prerequisites](#step-1-prerequisites)
2. [Enable the Vertex AI API](#step-2-enable-the-vertex-ai-api)
3. [Set Up Application Default Credentials](#step-3-set-up-application-default-credentials)
4. [Test with curl](#step-4-test-with-curl)
5. [Install the Python Gen AI SDK](#step-5-install-the-python-gen-ai-sdk)
6. [Test with Python — Text Prompt](#step-6-test-with-python--text-prompt)
7. [Test with Python — Multimodal (Image)](#step-7-test-with-python--multimodal-image)
8. [Using Thinking Mode](#step-8-using-thinking-mode)
9. [Model Reference](#model-reference)
10. [Troubleshooting](#troubleshooting)

---

## Step 1: Prerequisites

Before you begin, make sure you have completed the following:

- [x] Google Cloud CLI (`gcloud`) installed and configured (see `gcloud-setup-tutorial.md`)
- [x] Logged in with `gcloud init` and selected your project
- [ ] Python 3.9+ installed
- [ ] `pip3` available in your terminal

Verify your gcloud setup:

```bash
# Check your active project
gcloud config get-value project
# Expected: statg529300220261-01d2  (or your project ID)

# Check your active account
gcloud config get-value account
# Expected: your_email@columbia.edu
```

---

## Step 2: Enable the Vertex AI API

The Vertex AI API must be enabled in your Google Cloud project before you can call any models.

### Option A: Via the Console (browser)

1. Go to: https://console.cloud.google.com/apis/library/aiplatform.googleapis.com
2. Make sure your project is selected in the top dropdown.
3. Click **Enable**.

### Option B: Via the command line

```bash
gcloud services enable aiplatform.googleapis.com
```

Verify it's enabled:

```bash
gcloud services list --enabled --filter="name:aiplatform.googleapis.com"
```

You should see `aiplatform.googleapis.com` in the output.

---

## Step 3: Set Up Application Default Credentials

Application Default Credentials (ADC) let both `curl` and Python code authenticate with Google Cloud automatically.

```bash
gcloud auth application-default login
```

This will open your browser. Sign in with your **school email** (the same account linked to your project). After signing in, you'll see:

```
Credentials saved to file: [/Users/YOUR_USERNAME/.config/gcloud/application_default_credentials.json]
```

Verify it works:

```bash
gcloud auth application-default print-access-token
```

This should print a long token string (not an error).

---

## Step 4: Test with curl

Let's test the Gemini 3.1 Pro Preview model with a simple text prompt using `curl`.

### 4a. Set environment variables

```bash
MODEL_ID="gemini-3.1-pro-preview"
PROJECT_ID="$(gcloud config get-value project)"
```

### 4b. Send a request

```bash
curl -s \
  -X POST \
  -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
  -H "Content-Type: application/json" \
  "https://aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/global/publishers/google/models/${MODEL_ID}:generateContent" \
  -d '{
    "contents": {
      "role": "user",
      "parts": [
        {
          "text": "Explain what generative AI is in 3 sentences."
        }
      ]
    }
  }'
```

You should get a JSON response containing the model's answer.

> **Tip:** If you want streamed output (tokens arriving progressively), replace `:generateContent` with `:streamGenerateContent` in the URL.

---

## Step 5: Install the Python Gen AI SDK

The `google-genai` SDK provides a unified Python interface for Vertex AI.

### 5a. (Recommended) Create a virtual environment

```bash
cd /Users/chenw615/code/Python/GenAI-Learner/gcloud-setup
python3 -m venv .venv
source .venv/bin/activate
```

### 5b. Install the SDK

```bash
pip3 install --upgrade google-genai
```

Verify:

```bash
python3 -c "import google.genai; print('google-genai installed successfully')"
```

---

## Step 6: Test with Python — Text Prompt

Create a file called `test_gemini.py`:

```python
from google import genai

# Initialize the client for Vertex AI
client = genai.Client(
    vertexai=True,
    project="statg529300220261-01d2",  # Replace with your project ID
    location="global",
)

# Send a simple text prompt
model = "gemini-3.1-pro-preview"
response = client.models.generate_content(
    model=model,
    contents="Explain what generative AI is in 3 sentences.",
)

print(response.text)
```

Run it:

```bash
python3 test_gemini.py
```

You should see the model's response printed to your terminal.

---

## Step 7: Test with Python — Multimodal (Image)

Gemini 3.1 Pro can understand images. Create a file called `test_gemini_image.py`:

```python
from google import genai
from google.genai import types

# Initialize the client for Vertex AI
client = genai.Client(
    vertexai=True,
    project="statg529300220261-01d2",  # Replace with your project ID
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
```

Run it:

```bash
python3 test_gemini_image.py
```

---

## Step 8: Using Thinking Mode

Gemini 3.1 Pro is a "thinking" model — it can reason through its thoughts before responding. You can control the thinking depth with the `thinking_level` parameter.

| Thinking Level | Best For | Trade-off |
|---|---|---|
| `LOW` | Simple tasks, chat, fast responses | Minimal reasoning, lowest latency/cost |
| `MEDIUM` | Balanced tasks | Moderate reasoning depth |
| `HIGH` (default) | Complex reasoning, math, coding | Deepest reasoning, higher latency |

Create a file called `test_gemini_thinking.py`:

```python
from google import genai
from google.genai import types

client = genai.Client(
    vertexai=True,
    project="statg529300220261-01d2",  # Replace with your project ID
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
```

Run it:

```bash
python3 test_gemini_thinking.py
```

Try changing `thinking_level` to `"LOW"` or `"HIGH"` and compare the outputs.

> **Note:** Do NOT use the legacy `thinking_budget` parameter together with `thinking_level` — this will return a 400 error.

---

## Model Reference

### Model Details

| Property | Value |
|---|---|
| Model ID | `gemini-3.1-pro-preview` |
| Input types | Audio, images, video, text, PDF |
| Output type | Text |
| Input token limit | 1,000,000 (1M) |
| Output token limit | 64,000 (64K) |
| Release date | 2026-02-19 |
| Stage | Preview |

### Supported Features

- Thinking mode (LOW / MEDIUM / HIGH)
- Grounding with Google Search (Search as a Tool)
- Vertex AI RAG Engine
- URL Context
- Code Execution
- Structured Output
- Context Caching / Implicit Caching
- Batch Prediction
- Provisioned Throughput

### Media Resolution Defaults

| Resolution Setting | Image tokens | Video tokens | PDF tokens |
|---|---|---|---|
| DEFAULT | 1120 | 70 | 560 |
| LOW | 280 | 70 | 280 |
| MEDIUM | 560 | 70 | 560 |
| HIGH | 1120 | 280 | 1120 |

---

## Troubleshooting

### "Your default credentials were not found"
Run:
```bash
gcloud auth application-default login
```

### "Permission denied" or "403 Forbidden"
- Verify you're using the correct project: `gcloud config get-value project`
- Verify the Vertex AI API is enabled: `gcloud services list --enabled --filter="name:aiplatform.googleapis.com"`
- Re-authenticate: `gcloud auth login` then `gcloud auth application-default login`

### "Model not found" or "404"
- Make sure you're using the exact model ID: `gemini-3.1-pro-preview`
- Make sure `location` is set to `"global"` (not a specific region like `us-central1`)

### "400 error" with thinking
- Do NOT mix `thinking_budget` and `thinking_level` in the same request
- Valid thinking levels are: `LOW`, `MEDIUM`, `HIGH`

### Python import errors
- Make sure you installed the SDK: `pip3 install --upgrade google-genai`
- Make sure your virtual environment is activated: `source .venv/bin/activate`

---

## Links

- [Gemini 3.1 Pro in Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/gemini-3.1-pro-preview)
- [Vertex AI Studio](https://console.cloud.google.com/vertex-ai/studio) — Test prompts in the browser
- [Gen AI SDK Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/sdks/overview)
- [Gemini API Reference](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/inference)
