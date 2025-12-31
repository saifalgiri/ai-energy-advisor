from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from app.interfaces.home_service_interface import HomeServiceInterface
from app.interfaces.llm_service_interface import LLMServiceInterface
from app.shared.dependencies import get_home_service, get_llm_service
from app.utils.exception_helper import NotFoundException

router = APIRouter()


@router.post(
    "/{home_id}/advice",
    summary="Generate energy advice (SSE streaming)"
)
async def get_energy_advice(
    home_id: str,
    home_service: HomeServiceInterface = Depends(get_home_service),
    llm_service: LLMServiceInterface = Depends(get_llm_service)
):
    """
    Generate AI-powered energy efficiency recommendations.
    
    Returns a Server-Sent Events (SSE) stream with real-time recommendations.
    """
    if home_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            details= "Home id is required!"
        )

    try:
        home = await home_service.get_home(home_id)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No home found!"
        )
    
    return StreamingResponse(
        llm_service.generate_recommendations_stream(home),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
