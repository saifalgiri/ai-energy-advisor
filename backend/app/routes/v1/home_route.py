from fastapi import APIRouter, Depends, HTTPException, status, Query
import logging

from app.schemas.home_schema import HomeCreate, HomeResponse
from app.interfaces.home_service_interface import HomeServiceInterface
from app.shared.dependencies import get_home_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/",
    response_model=HomeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new home profile"
)
async def create_home(
    home_data: HomeCreate,
    home_service: HomeServiceInterface = Depends(get_home_service)
):
    """
    Create a new home profile with all the details:
    
    - **size_sqft**: Home size in square feet
    - **year_built**: Year the home was built
    - **heating_type**: Type of heating system
    - **insulation_level**: Current insulation quality
    - **windows_type**: Type of windows installed
    - **roof_type**: Type of roof
    - **num_occupants**: Number of people living in the home
    - **monthly_energy_bill**: Average monthly energy cost
    - **location**: City and state
    """
    try:
        home = await home_service.create_home(home_data)
        if home is None:
            raise HTTPException(status_code=404, detail="Home not found")
        return home
    except Exception:
        logger.exception(f"Unexpected error creating home")
    raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{home_id}",
    response_model=HomeResponse,
    summary="Get a home profile"
)
async def get_home(
    home_id: str,
    home_service: HomeServiceInterface = Depends(get_home_service)
):
    if home_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details= "Home id is required!" )
     
    try:
        home = await home_service.get_home(home_id)
        if home is None:
            raise HTTPException(status_code=404, detail=f"Home with ID {home_id} not found")
        
        return home
    except Exception:
        logger.exception(f"Unexpected error fetching home {home_id}", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

