from fastapi import FastAPI
from .database import Base, engine
from .routers import (
    faelle,
    befunde,
    beweismittel,
    gutachter,
    gutachten,
    reports
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CaseReporter", version="1.0.0")

# Domain-Router
app.include_router(faelle.router)
app.include_router(befunde.router)
app.include_router(beweismittel.router)
app.include_router(gutachter.router)
app.include_router(gutachten.router)

# KI-gesteuerte Report-Router
app.include_router(reports.router)

# Ein einfacher Health-Check
@app.get("/")
async def root():
    return {"message": "CaseReporter läuft"}