
from fastapi import Depends
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.database import AsyncSessionLocal
from app.services.home_service import HomeService
from app.services.llm_service import LLMService
from app.interfaces.home_service_interface import HomeServiceInterface
from app.interfaces.llm_service_interface import LLMServiceInterface


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_home_service(
    db: AsyncSession = Depends(get_db)
) -> HomeServiceInterface:
    return HomeService(db)


def get_llm_service() -> LLMServiceInterface:
    return LLMService()


# Import Depends from FastAPI
from fastapi import Depends
