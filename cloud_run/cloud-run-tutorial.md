# Deploy a GenAI Chatbot to Cloud Run

A step-by-step guide to deploying a **Flask + Gemini 3.1 Pro** chatbot to **Google Cloud Run** — a fully managed serverless platform.

---

## Table of Contents

1. [Prerequisites](#step-1-prerequisites)
2. [What is Cloud Run?](#step-2-what-is-cloud-run)
3. [Explore the App Code](#step-3-explore-the-app-code)
4. [Test Locally](#step-4-test-locally)
5. [Enable Required APIs](#step-5-enable-required-apis)
6. [Grant Vertex AI Permissions](#step-6-grant-vertex-ai-permissions)
7. [Deploy to Cloud Run](#step-7-deploy-to-cloud-run)
8. [Test the Live App](#step-8-test-the-live-app)
9. [Clean Up](#step-9-clean-up)
10. [Troubleshooting](#troubleshooting)

---

## Step 1: Prerequisites

Before you begin, make sure you have:

- [x] Google Cloud CLI (`gcloud`) installed and configured (see `../gcloud-setup-tutorial.md`)
- [x] Completed the Vertex AI / Gemini tutorial (see `../vertex_ai/gemini-3.1-pro-tutorial.md`)
- [x] Python 3.9+ installed
- [x] Your project ID set in gcloud

Verify your setup:

```bash
# Check your active project
gcloud config get-value project
# Expected: statg529300220261-01d2  (or your project ID)

# Check your active account
gcloud config get-value account
# Expected: your_email@columbia.edu
```

---

## Step 2: What is Cloud Run?

**Cloud Run** is a fully managed serverless platform that runs your containerized applications. Key benefits:

| Feature | Description |
|---|---|
| **Serverless** | No servers to manage — Google handles scaling and infrastructure |
| **Scale to zero** | You only pay when your app is handling requests |
| **Any language** | Package your app in a container and deploy it |
| **HTTPS by default** | Every service gets a unique `*.run.app` URL with TLS |
| **Source deploy** | Deploy directly from source code — Cloud Run builds the container for you |

In this tutorial we deploy a Flask app that uses the Gemini API. Cloud Run will:
1. Build a Docker container from our source code
2. Push it to Artifact Registry
3. Deploy it as a service with a public HTTPS URL

---

## Step 3: Explore the App Code

The app lives in the `app/` folder:

```
cloud_run/app/
├── main.py              # Flask app (routes + Gemini API call)
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container build instructions
└── templates/
    └── index.html       # Chat web UI
```

### `main.py`

Two routes:

- **`GET /`** — Serves the chat web UI (`index.html`)
- **`POST /api/chat`** — Accepts `{"message": "..."}`, calls Gemini 3.1 Pro, returns `{"reply": "..."}`

The app reads the `PROJECT_ID` environment variable (set automatically by the deploy command). The Gemini client is initialized once at startup using the Vertex AI SDK.

### `templates/index.html`

A simple chat interface with:
- Message bubbles (blue for user, white for bot)
- A text input and send button
- Vanilla JavaScript — no frameworks needed

### `Dockerfile`

- Based on `python:3.12-slim`
- Installs dependencies, copies the app code
- Runs with `gunicorn` on the port specified by Cloud Run's `$PORT` variable

---

## Step 4: Test Locally

Before deploying, run the app on your machine to make sure it works.

### 4a. Install dependencies

```bash
cd cloud_run/app

# (Optional) Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### 4b. Set Application Default Credentials

If you haven't already:

```bash
gcloud auth application-default login
```

### 4c. Run the app

```bash
python main.py
```

You should see:

```
 * Running on http://0.0.0.0:8080
```

### 4d. Test it

Open your browser and go to: **http://localhost:8080**

Type a message in the chat box and press Enter. You should see a response from Gemini.

To stop the server, press `Ctrl + C`.

---

## Step 5: Enable Required APIs

Cloud Run needs several APIs enabled. Run this once:

```bash
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  aiplatform.googleapis.com
```

Verify they're enabled:

```bash
gcloud services list --enabled --filter="name:(run OR cloudbuild OR artifactregistry OR aiplatform)"
```

---

## Step 6: Grant Vertex AI Permissions

When your app runs on Cloud Run, it uses a **service account** (not your personal credentials). This service account needs permission to call Vertex AI.

### 6a. Find the default Compute Engine service account

```bash
PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

echo "Service account: ${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
```

### 6b. Grant the Vertex AI User role

```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

This allows the Cloud Run service to call Gemini through Vertex AI.

---

## Step 7: Deploy to Cloud Run

Deploy directly from source — Cloud Run will build the container for you:

```bash
cd cloud_run/app

gcloud run deploy gemini-chatbot \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=$(gcloud config get-value project)
```

What this does:
- `--source .` — Build the container from the current directory (using the Dockerfile)
- `--region us-central1` — Deploy to the `us-central1` region
- `--allow-unauthenticated` — Make the app publicly accessible (no login required)
- `--set-env-vars` — Pass the project ID to the container

The first deploy takes 2-3 minutes (building the container). You'll see output like:

```
Deploying from source...
Building using Dockerfile...
...
Service [gemini-chatbot] revision [gemini-chatbot-00001-xxx] has been deployed
and is serving 100 percent of traffic.

Service URL: https://gemini-chatbot-xxxxxxxxxx-uc.a.run.app
```

Copy the **Service URL** — that's your live app.

---

## Step 8: Test the Live App

### In your browser

Open the Service URL from the deploy output. You should see the same chat UI you tested locally.

### With curl

```bash
SERVICE_URL=$(gcloud run services describe gemini-chatbot \
  --region us-central1 \
  --format="value(status.url)")

curl -s -X POST "$SERVICE_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Cloud Run?"}' | python3 -m json.tool
```

You should see a JSON response with Gemini's reply.

---

## Step 9: Clean Up

To avoid any charges, delete the Cloud Run service when you're done:

```bash
gcloud run services delete gemini-chatbot --region us-central1 --quiet
```

Optionally, delete the container images from Artifact Registry:

```bash
# List repositories
gcloud artifacts repositories list --location us-central1

# Delete the cloud-run-source-deploy repository (if created)
gcloud artifacts repositories delete cloud-run-source-deploy \
  --location us-central1 --quiet
```

---

## Troubleshooting

### "Permission denied" calling Vertex AI from Cloud Run

The Cloud Run service account doesn't have the `roles/aiplatform.user` role. Follow [Step 6](#step-6-grant-vertex-ai-permissions) to grant it.

### Build fails: "failed to build"

- Make sure your `Dockerfile` and `requirements.txt` are in the same directory
- Check that you're running `gcloud run deploy` from the `cloud_run/app/` directory

### "Cloud Run Admin API has not been enabled"

Enable the required APIs:

```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
```

### App deploys but returns 500 errors

Check the logs:

```bash
gcloud run services logs read gemini-chatbot --region us-central1 --limit 20
```

Common causes:
- `PROJECT_ID` environment variable not set (re-deploy with `--set-env-vars`)
- Service account missing Vertex AI permissions

### "Quota exceeded" or rate limit errors

The Gemini API has per-project quotas. If you hit limits:
- Wait a minute and try again
- Check quotas in the [Cloud Console](https://console.cloud.google.com/iam-admin/quotas)

### Local testing works but Cloud Run doesn't

- Locally you use your personal ADC credentials; on Cloud Run the service account is used
- Make sure the service account has `roles/aiplatform.user` (Step 6)

---

## Next Steps

Now that you've deployed a GenAI app to Cloud Run, you can:

- Add **conversation history** (multi-turn chat) by sending previous messages to the API
- Add **streaming responses** for a better chat UX
- Restrict access with **Identity-Aware Proxy (IAP)** or Cloud Run authentication
- Connect a **custom domain** to your service
- Explore [Cloud Run documentation](https://cloud.google.com/run/docs)
