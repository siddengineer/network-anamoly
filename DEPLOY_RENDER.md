# Deploying NetGuard AI to Render (Free Tier Guide)

This guide walks you through deploying **NetGuard AI** to [Render](https://render.com) so anyone with a web browser can access and use your application online.

---

## Architecture on Render

NetGuard AI is architected as a **Unified Full-Stack Web Service**:
- FastAPI serves both the **API routes** (`/api/...`) and the **compiled React production SPA** (`frontend/dist`) under a single domain (e.g. `https://netguard-ai.onrender.com`).
- **Benefits**:
  - Uses only **1 free Render Web Service** instance.
  - Zero CORS configuration required.
  - Faster load times and unified SSL certificate.
  - The SQLite database and trained ML models live alongside the backend service.

---

## Step 1: Push Project to GitHub

If you haven’t already pushed your code to GitHub:

1. Open PowerShell in the project directory:
   ```powershell
   cd c:\Users\K\Desktop\netguard
   ```

2. Initialize Git (if not done already) and commit:
   ```powershell
   git init
   git add .
   git commit -m "NetGuard AI: Production release with Render deployment config"
   ```

3. Create a new repository on [GitHub](https://github.com/new) (e.g., `netguard-ai`).
4. Link and push:
   ```powershell
   git remote add origin https://github.com/YOUR_USERNAME/netguard-ai.git
   git branch -M main
   git push -u origin main
   ```

---

## Step 2: Create a Web Service on Render

1. Go to [https://dashboard.render.com](https://dashboard.render.com) and log in (or sign up with GitHub).
2. Click the **"New +"** button in the top navigation and select **"Web Service"**.
3. Choose **"Build and deploy from a Git repository"** and connect your `netguard-ai` repository.

---

## Step 3: Configure Service Settings

Fill in the settings as follows:

| Field | Value |
|---|---|
| **Name** | `netguard-ai` (or your preferred name) |
| **Language / Runtime** | `Python` |
| **Region** | `Oregon (US West)` or closest to your audience |
| **Branch** | `main` |
| **Build Command** | `pip install -r backend/requirements.txt && python backend/train_models.py && npm --prefix frontend install && npm --prefix frontend run build` |
| **Start Command** | `uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` |

> **Alternative Build Command**: If you prefer using the script, you can set the Build Command to:
> `chmod +x build.sh && ./build.sh`

---

## Step 4: Add Environment Variables

Scroll down to the **"Environment Variables"** section and click **"Add Environment Variable"**:

1. **`GROQ_API_KEY`**:
   - Value: `your_groq_api_key_here` (paste your real Groq API key here)
2. **`GROQ_MODEL`**:
   - Value: `openai/gpt-oss-120b`
3. **`PYTHON_VERSION`**:
   - Value: `3.12.2`
4. **`NODE_VERSION`**:
   - Value: `20.17.0`

---

## Step 5: Deploy & Test Live

1. Click **"Deploy Web Service"**.
2. Render will stream the build log:
   - Installing Python requirements
   - Training Random Forest & Isolation Forest on `CIC-IDS2017.xlsx`
   - Building the React frontend into `frontend/dist`
   - Starting Uvicorn on `$PORT`
3. Once the status turns to **"Live"**, your URL will appear at the top (e.g. `https://netguard-ai.onrender.com`).
4. Click the link to open **NetGuard AI** in your browser.

---

## Tips for Render Free Tier

- **Cold Starts**: Render free instances spin down after 15 minutes of inactivity. When someone visits the site after a period of dormancy, it may take 30–50 seconds to wake up. Once awake, performance is immediate.
- **Persistence**: SQLite database changes persist while the container runs. If Render restarts the container, the initial state is automatically reseeded from `CIC-IDS2017.xlsx`.
