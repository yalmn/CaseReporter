from .crud import get_fall, get_befunde, get_beweismittel
from .llm_client import LLMClient
from .database import get_db
from . import models
import jinja2
from .utils import generate_pdf_from_markdown
from sqlalchemy.orm import Session

class ReportService:
    def __init__(self, db: Session):
        self.db = db
        self.llm = LLMClient()
        loader = jinja2.FileSystemLoader(searchpath="./templates")
        self.jinja = jinja2.Environment(loader=loader)
        self.template = self.jinja.get_template("gutachten_template.md")

    def create_report(self, case_id: str):
        case = get_fall(self.db, case_id)
        if not case:
            raise ValueError(f"Fall {case_id} nicht gefunden")

        befunde = get_befunde(self.db, case.id)
        beweismittel = get_beweismittel(self.db, case.id)

        # 1. Basis-Template füllen (ohne Fazit)
        base_md = self.template.render(
            fall_id=case.fall_id,
            einleitung=case.untersuchungsziel or "",
            vorgeschwindigkeit="",  # ggf. anpassen
            befundsliste=[{"beschreibung": b.beschreibung, "zeitstempel": b.zeitstempel} for b in befunde],
            ki_fazit=""  
        )

        # 2. KI-Fazit generieren
        prompt = f"{base_md}\n\n## 4. Fazit & Empfehlungen:\n"
        ki_fazit = self.llm.generate_fazit(prompt)

        # 3. Volles Template mit Fazit
        full_md = self.template.render(
            fall_id=case.fall_id,
            einleitung=case.untersuchungsziel or "",
            vorgeschwindigkeit="",
            befundsliste=[{"beschreibung": b.beschreibung, "zeitstempel": b.zeitstempel} for b in befunde],
            ki_fazit=ki_fazit
        )

        # 4. PDF erzeugen
        pdf_path = generate_pdf_from_markdown(full_md)
        return pdf_path, ki_fazit