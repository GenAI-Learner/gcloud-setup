# Google Cloud CLI Setup Tutorial

This tutorial walks you through installing and configuring the Google Cloud CLI (`gcloud`) on **macOS**. By the end, you will have `gcloud` ready to interact with your Google Cloud project for the GenAI class.

---

## Prerequisites

- A Mac with **macOS** (Intel or Apple Silicon)
- A **Google account** with access to your class Google Cloud project
- Your **Google Cloud Project ID** (provided by the instructor, e.g., `statg529300220261-01d2`)

---

## Step 1: Download the Google Cloud CLI

1. Open your browser and go to: https://cloud.google.com/sdk/docs/install
2. Under **macOS**, download the package that matches your Mac's chip:
   - **Apple Silicon (M1/M2/M3/M4):** `macOS 64-bit (ARM64, Apple Silicon)`
   - **Intel:** `macOS 64-bit (x86_64)`

   > **Tip:** Not sure which chip you have? Click the Apple menu () > **About This Mac**. If it says "Apple M1" (or M2, M3, M4), choose ARM64. If it says "Intel", choose x86_64.

3. The download will be a `.tar.gz` file (e.g., `google-cloud-cli-558.0.0-darwin-arm.tar.gz`).

---

## Step 2: Extract and Install

1. Open **Terminal** (search for "Terminal" in Spotlight with `Cmd + Space`).

2. Navigate to your Downloads folder:
   ```bash
   cd ~/Downloads
   ```

3. Extract the archive:
   ```bash
   tar -xzf google-cloud-cli-*.tar.gz
   ```

4. Run the installer:
   ```bash
   ./google-cloud-sdk/install.sh
   ```

5. The installer will ask you several questions. Answer as follows:

   **"Modify profile to update your $PATH and enable shell command completion?"**
   Type `Y` and press Enter.

   **"Enter a path to an rc file to update, or leave blank to use [/Users/YOUR_USERNAME/.zshrc]:"**
   Press Enter to accept the default (leave blank).

   **"Download and run Python 3.13 installer?"**
   Type `Y` and press Enter. You may be prompted for your Mac password — this is normal.

6. Wait for the installation to finish. You will see a message:
   ```
   ==> Start a new shell for the changes to take effect.
   ```

---

## Step 3: Activate `gcloud` in Your Terminal

After installation, `gcloud` won't be available in your current terminal session. You have two options:

**Option A — Open a new terminal window** (recommended):
Simply close your terminal and open a new one.

**Option B — Reload your shell profile:**
```bash
source ~/.zshrc
```

Verify the installation by running:
```bash
gcloud version
```

You should see output like:
```
Google Cloud SDK 558.0.0
bq 2.1.28
core 2026.02.20
...
```

> **Troubleshooting:** If you get `zsh: command not found: gcloud`, make sure you opened a **new** terminal window or ran `source ~/.zshrc`.

---

## Step 4: Initialize `gcloud`

Run the initialization command:
```bash
gcloud init
```

This starts an interactive setup. Follow the prompts:

### 4a. Pick a configuration

If this is your first time, you will be asked to create a configuration. Select:
```
[1] Create a new configuration
```

If you already have configurations, select:
```
[2] Create a new configuration
```

When prompted for a configuration name, type something descriptive like:
```
genai-class
```

### 4b. Choose your account

You will be asked to log in. Select:
```
[1] Sign in with a new Google Account
```

This will open your **browser**. Sign in with your **Columbia/school email** (the one that has access to the class project).

### 4c. Select your project

After authentication, you'll be asked to pick a project. If the class project appears in the list, select it. If not (or if you see an error like `invalid_grant`), you can type the project ID directly:

```
Enter project ID you would like to use:  YOUR_PROJECT_ID
```

Replace `YOUR_PROJECT_ID` with the project ID provided by the instructor.

### 4d. Set default region and zone

If prompted to set a default Compute Engine region and zone:
- Select a region close to you, such as `us-central1` or `us-east1`
- Select a zone like `us-central1-a` or `us-east1-b`

> **Note:** If the Compute Engine API is not enabled, you may see a message saying it can't set defaults. That's okay — you can set them later.

---

## Step 5: Authenticate (Fix Token Issues)

If during `gcloud init` you saw this warning:

```
WARNING: Listing available projects failed: There was a problem refreshing
your current auth tokens: ('invalid_grant: Bad Request', ...)
```

This means your saved credentials have expired. Fix this by re-authenticating:

```bash
gcloud auth login
```

This will open your browser again. Sign in with the **same account** you selected in Step 4b.

After logging in, you should see:
```
You are now logged in as [your_email@columbia.edu].
```

---

## Step 6: Verify Your Setup

Run these commands to confirm everything is configured correctly:

### Check your active account:
```bash
gcloud config get-value account
```
Expected output: your school email (e.g., `your_email@columbia.edu`)

### Check your active project:
```bash
gcloud config get-value project
```
Expected output: your project ID (e.g., `statg529300220261-01d2`)

### List your configurations:
```bash
gcloud config configurations list
```
You should see your configuration listed as `IS_ACTIVE: True`.

### Test that authentication works:
```bash
gcloud projects describe $(gcloud config get-value project)
```
This should return details about your project without any errors.

---

## Step 7: Set Application Default Credentials (for Python/SDK usage)

If you'll be writing Python code that uses Google Cloud APIs (e.g., Vertex AI, BigQuery), you also need to set **Application Default Credentials (ADC)**:

```bash
gcloud auth application-default login
```

This opens your browser one more time. Sign in with the same account. Once complete, your Python code can automatically authenticate with Google Cloud.

---

## Quick Reference

| Task | Command |
|------|---------|
| Check current config | `gcloud config list` |
| Switch project | `gcloud config set project PROJECT_ID` |
| Switch account | `gcloud config set account EMAIL` |
| Re-authenticate | `gcloud auth login` |
| Set default region | `gcloud config set compute/region us-central1` |
| Set default zone | `gcloud config set compute/zone us-central1-a` |
| Update gcloud | `gcloud components update` |
| List all configurations | `gcloud config configurations list` |
| Create new configuration | `gcloud config configurations create CONFIG_NAME` |
| Activate a configuration | `gcloud config configurations activate CONFIG_NAME` |

---

## Common Issues and Fixes

### `zsh: command not found: gcloud`
Your shell doesn't know where `gcloud` is. Fix by opening a new terminal or running:
```bash
source ~/.zshrc
```

### `invalid_grant: Bad Request`
Your auth tokens have expired. Re-authenticate:
```bash
gcloud auth login
```

### Wrong project is selected
Switch to the correct project:
```bash
gcloud config set project YOUR_PROJECT_ID
```

### Permission denied errors
Make sure you are logged in with the correct account:
```bash
gcloud auth list
```
If the wrong account is active (marked with `*`), switch:
```bash
gcloud config set account your_email@columbia.edu
```

### Python code can't authenticate
Set up Application Default Credentials:
```bash
gcloud auth application-default login
```

---

## Next Steps

Once your `gcloud` CLI is set up, you are ready to:
- Use Google Cloud APIs from Python (Vertex AI, BigQuery, etc.)
- Create and manage cloud resources from the command line
- Deploy applications to Google Cloud

If you run into issues, check the official documentation: https://cloud.google.com/sdk/docs
