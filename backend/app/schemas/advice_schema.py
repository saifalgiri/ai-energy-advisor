
# from pydantic import BaseModel
# from typing import Optional
# from datetime import datetime
# from enum import Enum


# class MessageType(str, Enum):
#     CONNECTED = "connected"
#     TOKEN = "token"
#     COMPLETE = "complete"
#     ERROR = "error"


# class SSEMessage(BaseModel):
#     type: MessageType
#     content: Optional[str] = None
#     home_id: Optional[str] = None
#     error: Optional[str] = None


# class AdviceResponse(BaseModel):
#     home_id: str
#     recommendations: str
#     estimated_savings: Optional[str] = None
#     generated_at: datetime

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class MessageType(str, Enum):
    CONNECTED = "connected"
    RECOMMENDATION = "recommendation"
    COMPLETE = "complete"
    ERROR = "error"


class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Category(str, Enum):
    HEATING = "heating"
    INSULATION = "insulation"
    WINDOWS = "windows"
    APPLIANCES = "appliances"
    HABITS = "habits"
    RENEWABLE = "renewable"


class Recommendation(BaseModel):
    id: str
    title: str
    description: str
    estimated_cost: str
    estimated_savings: str
    priority: Priority
    category: Category


class SSEMessage(BaseModel):
    type: MessageType
    recommendation: Optional[Recommendation] = None
    home_id: Optional[str] = None
    error: Optional[str] = None


class AdviceResponse(BaseModel):
    home_id: str
    recommendations: List[Recommendation]
    generated_at: datetime