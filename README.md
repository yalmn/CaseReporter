# CaseReporter

CaseReporter ist ein modular aufgebauter Microservice zur automatischen Erstellung forensischer Gutachten basierend auf Falldaten und KI-gestützter Fazit-Generierung.

## Inhalte

- **Datenmodelle & Datenbank**: PostgreSQL (Tabellen: Fälle, Befunde, Beweismittel, Gutachter, Gutachten)
- **API-Layer**: FastAPI + Uvicorn (ASGI)
- **ORM**: SQLAlchemy für DB-Zugriff
- **Migrations**: Alembic für Schema-Änderungen
- **Template-Engine**: Jinja2 für Markdown-Gutachten-Vorlage
- **LLM-Client**: Hugging Face Transformers + bitsandbytes zum Ausführen von quantisiertem LLaMA 2 (7B)
- **PDF-Generator**: Pandoc + XeLaTeX via ein Utility

## Abhängigkeiten und deren Zweck

| Paket             | Zweck                                               |
| ----------------- | --------------------------------------------------- |
| fastapi           | Web-Framework für API-Endpoints (async, performant) |
| uvicorn[standard] | ASGI-Server für FastAPI                             |
| sqlalchemy        | ORM für relationale DB-Zugriffe                     |
| alembic           | Versionsverwaltung / Migration für DB-Schema        |
| pydantic          | Validierung und Serialisierung von JSON-Requests    |
| psycopg2-binary   | PostgreSQL-Treiber für Python                       |
| transformers      | LLM-Modelle, Tokenizer-API („Llama 2 Chat“)         |
| bitsandbytes      | 8-Bit-Quantisierung für effiziente LLM-Inferenz     |
| jinja2            | Template-Engine für Markdown-Vorlagen               |

## Funktionalitäten

1. **Falldaten verwalten**: CRUD-Endpunkte für Fälle, Befunde, Beweismittel, Gutachter, Gutachten.
2. **KI-Report generieren**:
   - `/reports/{case_id}`: Generiert ein PDF-Gutachten mit KI-Fazit für den angegebenen Fall.
   - `/reports/{case_id}/fazit`: Liefert nur den KI-generierten Text.
3. **Menschliche Review-Schicht**: Externe Reviewer-Oberfläche integriert via API.
4. **Automatische DB-Migration**: Alembic steuert Schema-Updates.

## Installation & Ausführung

1. **Setup-Skript** ausführbar machen:
   ```bash
   chmod +x setup.sh
   ```
2. **Alles in einem Schritt installieren und starten**:
   ```bash
   ./setup.sh
   ```
3. **Service** läuft auf `http://localhost:8000`.

## Beispiel-Szenario

1. **Fall anlegen**:
   ```bash
   curl -X POST "http://localhost:8000/faelle/" \
        -H "Content-Type: application/json" \
        -d '{
              "fall_id": "2025-42-FB",
              "untersuchungsziel": "Analyse von Image XYZ",
              "befunde": [],
              "beweismittel": []
            }'
   ```
2. **Belege hinzufügen**:
   ```bash
   curl -X POST "http://localhost:8000/faelle/1/befunde/" -d '{...}'
   curl -X POST "http://localhost:8000/faelle/1/beweismittel/" -d '{...}'
   ```
3. **KI-Gutachten erzeugen**:
   ```bash
   curl -X GET "http://localhost:8000/reports/2025-42-FB" --output gutachten.pdf
   ```
4. **KI-Fazit abrufen**:
   ```bash
   curl -X POST "http://localhost:8000/reports/2025-42-FB/fazit"
   ```

## CLI-Wrapper: `casereport.sh`

Das Projekt enthält ein CLI-Skript namens `casereport.sh`, das als einfacher Wrapper für die CaseReporter-API dient. Du findest es im Projektstamm neben `setup.sh`. Die wichtigsten Befehle:

- **Report erstellen**: `./casereport.sh --generate <FALL_ID>`
- **KI-Fazit abrufen**: `./casereport.sh --fazit <FALL_ID>`
- **Hilfe anzeigen**: `./casereport.sh --help`

Vor der Nutzung stelle bitte sicher, dass das Skript ausführbar ist:

```bash
chmod +x casereport.sh
```

Damit kannst du ohne direkte API-Calls schnell und unkompliziert Reports und Fazits für beliebige Fälle erzeugen.
