from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class BefundBase(BaseModel):
    beschreibung: str
    zeitstempel: datetime

class BefundCreate(BefundBase):
    pass

class BeweismittelBase(BaseModel):
    typ: Optional[str]
    uri: Optional[str]
    metadaten: Optional[str]

class BeweismittelCreate(BeweismittelBase):
    pass

class GutachterBase(BaseModel):
    mitarbeiter_id: str
    name: Optional[str]
    rolle: Optional[str]

class GutachterCreate(GutachterBase):
    pass

class GutachtenBase(BaseModel):
    gutachten_id: str
    inhalt: str
    gutachter_id: int

class GutachtenCreate(GutachtenBase):
    pass

class FallBase(BaseModel):
    fall_id: str
    untersuchungsziel: Optional[str]

class FallCreate(FallBase):
    befunde: List[BefundCreate] = []
    beweismittel: List[BeweismittelCreate] = []

class Befund(BefundBase):
    id: int
    class Config:
        orm_mode = True

class Beweismittel(BeweismittelBase):
    id: int
    class Config:
        orm_mode = True

class Gutachter(GutachterBase):
    id: int
    class Config:
        orm_mode = True

class Gutachten(GutachtenBase):
    id: int
    erstellt_am: datetime
    class Config:
        orm_mode = True

class Fall(FallBase):
    id: int
    erstellt_am: datetime
    befunde: List[Befund] = []
    beweismittel: List[Beweismittel] = []
    gutachter_id: Optional[int]
    gutachten: Optional[Gutachten] = None
    class Config:
        orm_mode = True