# Clinic AI: Appointment & Report Handling (MVP)
A minimal, local-first scaffold for the Clinic/Doctor workflow:
- Receive WhatsApp (or webhook) messages
- Intent classification + LLM-based replies (placeholder)
- Appointment booking, calendar check (mock)
- Upload lab reports (OCR pipeline stub)
- Human-in-the-loop approval dashboard

## Contents
- `app.py` - Flask app with webhook, admin dashboard.
- `models.py` - SQLAlchemy models.
- `templates/` - simple HTML templates.
- `requirements.txt` - Python deps.
- `docker-compose.yml` & `Dockerfile` - run locally.
- `sample_requests.http` - sample HTTP requests for testing.
- `run_demo.sh` - run the app locally quickly.

## How to run (local)
1. Create a Python virtualenv.
2. `pip install -r requirements.txt`
3. `export FLASK_APP=app.py`
4. `export OPENAI_API_KEY=sk-...` (or leave for mock mode)
5. `flask run --host=0.0.0.0 --port=5000`
6. Visit `http://localhost:5000/admin` to see dashboard.

This scaffold is intentionally minimal and ready to be extended with:
- Real WhatsApp integration via Twilio/Meta Cloud API
- Real LLM provider (OpenAI or self-hosted)
- Production DB (Postgres), background workers, authentication
