import enum
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID

from app.models.home_model import HeatingType, InsulationLevel, WindowsType, RoofType


# Base schema
class HomeBase(BaseModel):
    size_sqft: int = Field(..., gt=0, description="Home size in square feet")
    year_built: int = Field(..., ge=1800, le=2025, description="Year built")
    heating_type: HeatingType
    insulation_level: InsulationLevel
    windows_type: WindowsType
    roof_type: RoofType
    num_occupants: int = Field(..., gt=0, description="Number of occupants")
    monthly_energy_bill: float = Field(..., ge=0, description="Monthly energy bill")
    location: Optional[str] = Field(None,  description="Location")

    @field_validator('monthly_energy_bill')
    @classmethod
    def validate_bill(cls, v: float) -> float:
        if v > 10000:
            raise ValueError('Monthly bill seems unusually high')
        return round(v, 2)


# Schema for creating a home
class HomeCreate(HomeBase):
    pass


# Schema for response
class HomeResponse(HomeBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

