#!/usr/bin/env bash
set -e

# 1. Python Virtual Environment anlegen
python3 -m venv venv
source venv/bin/activate

# 2. pip auf neueste Version bringen
pip install --upgrade pip

# 3. Abhängigkeiten installieren
pip install -r requirements.txt

# 4. Alembic-Migrationen ausführen
alembic upgrade head

# 5. Service starten
echo "Starting CaseReporter..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload