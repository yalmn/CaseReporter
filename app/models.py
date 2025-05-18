from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Fall(Base):
    __tablename__ = "faelle"
    id = Column(Integer, primary_key=True, index=True)
    fall_id = Column(String(50), unique=True, nullable=False, index=True)
    untersuchungsziel = Column(Text)
    erstellt_am = Column(DateTime, default=datetime.utcnow)

    befunde = relationship(
        "Befund", back_populates="fall", cascade="all, delete-orphan"
    )
    beweismittel = relationship(
        "Beweismittel", back_populates="fall", cascade="all, delete-orphan"
    )
    gutachten = relationship(
        "Gutachten", back_populates="fall", uselist=False
    )

class Befund(Base):
    __tablename__ = "befunde"
    id = Column(Integer, primary_key=True, index=True)
    fall_id = Column(Integer, ForeignKey("faelle.id"), nullable=False)
    beschreibung = Column(Text, nullable=False)
    zeitstempel = Column(DateTime, nullable=False)

    fall = relationship("Fall", back_populates="befunde")

class Beweismittel(Base):
    __tablename__ = "beweismittel"
    id = Column(Integer, primary_key=True, index=True)
    fall_id = Column(Integer, ForeignKey("faelle.id"), nullable=False)
    typ = Column(String(50))
    uri = Column(String(256))
    metadaten = Column(Text)

    fall = relationship("Fall", back_populates="beweismittel")

class Gutachter(Base):
    __tablename__ = "gutachter"
    id = Column(Integer, primary_key=True, index=True)
    mitarbeiter_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(100))
    rolle = Column(String(50))

    gutachten = relationship("Gutachten", back_populates="gutachter")

class Gutachten(Base):
    __tablename__ = "gutachten"
    id = Column(Integer, primary_key=True, index=True)
    fall_id = Column(Integer, ForeignKey("faelle.id"), nullable=False, unique=True)
    gutachten_id = Column(String(50), unique=True, nullable=False)
    erstellt_am = Column(DateTime, default=datetime.utcnow)
    inhalt = Column(Text)
    gutachter_id = Column(Integer, ForeignKey("gutachter.id"), nullable=False)

    fall = relationship("Fall", back_populates="gutachten")
    gutachter = relationship("Gutachter", back_populates="gutachten")