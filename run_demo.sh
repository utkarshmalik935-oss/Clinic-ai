#!/usr/bin/env bash
export FLASK_APP=app.py
export FLASK_ENV=development
# optional: export OPENAI_API_KEY=sk-...
python -m pip install -r requirements.txt
flask run --host=0.0.0.0 --port=5000
