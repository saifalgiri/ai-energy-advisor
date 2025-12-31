
from abc import ABC, abstractmethod
from typing import AsyncGenerator

from app.models.home_model import Home


class LLMServiceInterface(ABC):    
    @abstractmethod
    def create_energy_prompt(self, home: Home) -> str:
        pass
    
    @abstractmethod
    async def generate_recommendations_stream(
        self, 
        home: Home
    ) -> AsyncGenerator[str, None]:
        pass