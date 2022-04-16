from fastapi.routing import APIRouter

from api.endpoints import slack_router


router = APIRouter()
router.include_router(slack_router)
