from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import logging

from app.interfaces.home_service_interface import HomeServiceInterface
from app.models.home_model import Home
from app.schemas.home_schema import HomeCreate
from app.utils.exception_helper import NotFoundException

# Set up logging
logger = logging.getLogger(__name__)

class HomeService(HomeServiceInterface):    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_home(self, home_data: HomeCreate) -> Home:

        if home_data is None:
            logger.error("Home data is None")
            raise ValueError("Home data must not be None")
        
        try:
            logger.debug(f"Creating home with data: {home_data}")
            home = Home(**home_data.model_dump())

            self.db.add(home)
            await self.db.flush()
            await self.db.refresh(home)

            logger.info(f"Home profile created successfully - ID: {home.id}")
            return home
        
        except Exception as e:
            logger.error(f"Error creating home profile: {str(e)}", exc_info=True)
            raise
    

    async def get_home(self, home_id: str) -> Home:
        if home_id is None:
            logger.error("Home id is null")
            raise ValueError("Home id can't be null")
        
        try:            
            result = await self.db.execute(
                select(Home).where(Home.id == home_id)
            )
            home = result.scalar_one_or_none()
            
            if not home:
               return None
            
            return home
        
        except Exception as e:
            logger.error(f"Error fetching home profile {home_id}: {str(e)}", exc_info=True)
            raise
    
    