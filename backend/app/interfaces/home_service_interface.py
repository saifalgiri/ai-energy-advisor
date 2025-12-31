
from abc import ABC, abstractmethod

from app.models.home_model import Home
from app.schemas.home_schema import HomeCreate


class HomeServiceInterface(ABC):    
    @abstractmethod
    async def create_home(self, home_data: HomeCreate) -> Home:
        pass
    
    @abstractmethod
    async def get_home(self, home_id: str) -> Home:
        pass
    
