
from fastapi import APIRouter
from app.routes.v1 import home_route
from app.routes.v1 import advice_route

router = APIRouter()

router.include_router(
    home_route.router,
    prefix="/homes",
    tags=["homes"]
)
router.include_router(
    advice_route.router,
    prefix="/homes",
    tags=["advice"]
)