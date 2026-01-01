from sqlalchemy import Column, String, Integer, Float, DateTime, UUID, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
import enum
from uuid import uuid4
from app.shared.database import Base


class HeatingType(str, enum.Enum):
    GAS = "gas"
    ELECTRIC = "electric"
    OIL = "oil"
    HEAT_PUMP = "heat_pump"
    SOLAR = "solar"


class InsulationLevel(str, enum.Enum):
    MINIMAL = "minimal"
    MODERATE = "moderate"
    GOOD = "good"
    EXCELLENT = "excellent"


class WindowsType(str, enum.Enum):
    SINGLE = "single"
    DOUBLE = "double"
    TRIPLE = "triple"

class RoofType(str, enum.Enum):
    FLAT = "flat"
    PITCHED = "pitched"
    METAL = "metal"
    TILE = "tile"

class Home(Base):
    __tablename__ = "homes"

    id = Column(UUID, primary_key=True, index=True, default=uuid4, unique=True, nullable=False)
    size_sqft = Column(Integer, nullable=False)
    year_built = Column(Integer, nullable=False)
    heating_type = Column(SQLEnum(HeatingType), nullable=False)
    insulation_level = Column(SQLEnum(InsulationLevel), nullable=False)
    windows_type = Column(SQLEnum(WindowsType), nullable=False)
    roof_type = Column(SQLEnum(RoofType), nullable=False)
    num_occupants = Column(Integer, nullable=False)
    monthly_energy_bill = Column(Float, nullable=False)
    location = Column(String, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Home {self.id} - {self.location}>"