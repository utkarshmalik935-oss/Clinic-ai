# Deploying Clinic AI on Render (easy)

App name: **clinic-ai**

## Required environment variables (set on Render dashboard)
- `DATABASE_URL` (optional) — Postgres URL. If not set, app will use SQLite.
- `OPENAI_API_KEY` (optional) — your OpenAI API key for report summarization.
- `SECRET_KEY` (recommended) — Flask secret key.
- `PORT` — Render sets this automatically.

## Steps (Render)
1. Create a free account at https://render.com
2. Click **New** → **Service** → **Web Service**
3. Connect your GitHub repo (or drag & drop this project folder as a repo using Render's guides).
4. Name the service `clinic-ai` (or accept default).
5. For Environment choose **Docker** (we included Dockerfile).
6. For Build/Start command leave defaults (Render will use Dockerfile).
7. In Environment > Environment Variables add `OPENAI_API_KEY` and `DATABASE_URL` if available.
8. Click **Create Web Service** — Render will build and deploy.
9. After deploy, Render will give a public URL like `https://clinic-ai.onrender.com`.

## Local testing (before deploy)
- Install dependencies: `pip install -r requirements.txt`
- Run locally: `gunicorn app:app --bind 0.0.0.0:5000 --workers 3`
- Or: `flask run --host=0.0.0.0 --port=5000` (development)

## WhatsApp integration
You selected **later** for WhatsApp. When ready, configure Twilio or Meta Cloud and set `WHATSAPP_API_URL` and related creds.

