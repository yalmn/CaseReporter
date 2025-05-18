from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

# --- Case CRUD ---

def get_fall(db: Session, fall_id: str):
    return db.query(models.Fall).filter(models.Fall.fall_id == fall_id).first()


def create_fall(db: Session, fall: schemas.FallCreate):
    db_fall = models.Fall(
        fall_id=fall.fall_id,
        untersuchungsziel=fall.untersuchungsziel,
    )
    db.add(db_fall)
    db.commit()
    db.refresh(db_fall)
    for f in fall.befunde:
        db_b = models.Befund(
            fall_id=db_fall.id,
            beschreibung=f.beschreibung,
            zeitstempel=f.zeitstempel
        )
        db.add(db_b)
    for e in fall.beweismittel:
        db_e = models.Beweismittel(
            fall_id=db_fall.id,
            typ=e.typ,
            uri=e.uri,
            metadaten=e.metadaten
        )
        db.add(db_e)
    db.commit()
    db.refresh(db_fall)
    return db_fall

# --- Befund CRUD ---

def get_befunde(db: Session, fall_id: int):
    return db.query(models.Befund).filter(models.Befund.fall_id == fall_id).all()


def create_befund(db: Session, fall_id: int, befund: schemas.BefundCreate):
    db_b = models.Befund(
        fall_id=fall_id,
        beschreibung=befund.beschreibung,
        zeitstempel=befund.zeitstempel
    )
    db.add(db_b)
    db.commit()
    db.refresh(db_b)
    return db_b

# --- Beweismittel CRUD ---

def get_beweismittel(db: Session, fall_id: int):
    return db.query(models.Beweismittel).filter(models.Beweismittel.fall_id == fall_id).all()


def create_beweismittel(db: Session, fall_id: int, beweismittel: schemas.BeweismittelCreate):
    db_e = models.Beweismittel(
        fall_id=fall_id,
        typ=beweismittel.typ,
        uri=beweismittel.uri,
        metadaten=beweismittel.metadaten
    )
    db.add(db_e)
    db.commit()
    db.refresh(db_e)
    return db_e

# --- Gutachter CRUD ---

def get_gutachter(db: Session, gutachter_id: int):
    return db.query(models.Gutachter).filter(models.Gutachter.id == gutachter_id).first()


def create_gutachter(db: Session, gutachter: schemas.GutachterCreate):
    db_g = models.Gutachter(
        mitarbeiter_id=gutachter.mitarbeiter_id,
        name=gutachter.name,
        rolle=gutachter.rolle
    )
    db.add(db_g)
    db.commit()
    db.refresh(db_g)
    return db_g

# --- Gutachten CRUD ---

def get_gutachten_by_case(db: Session, fall_id: int):
    return db.query(models.Gutachten).filter(models.Gutachten.fall_id == fall_id).first()


def create_gutachten(db: Session, fall_id: int, gutachten: schemas.GutachtenCreate):
    db_gt = models.Gutachten(
        fall_id=fall_id,
        gutachten_id=gutachten.gutachten_id,
        inhalt=gutachten.inhalt,
        gutachter_id=gutachten.gutachter_id
    )
    db.add(db_gt)
    db.commit()
    db.refresh(db_gt)
    return db_gt