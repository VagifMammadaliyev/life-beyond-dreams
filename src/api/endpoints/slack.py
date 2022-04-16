import slack
from fastapi import Response
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from core import SLACK_VERIFICATION_TOKEN, SLACK_BOT_TOKEN
from api.schemas import SlackEventHookRequest
from api.constants import SlackEventHookType, SlackEventType


router = APIRouter(prefix="/slack", tags=["slack"])


@router.post("/event-hook")
def event_hook(event_hook_request: SlackEventHookRequest):
    slack_client = slack.WebClient(token=SLACK_BOT_TOKEN)
    if event_hook_request.token != SLACK_VERIFICATION_TOKEN:
        raise HTTPException(status_code=403)

    if event_hook_request.type == SlackEventHookType.URL_VERIFICATION:
        return {"challenge": event_hook_request.challenge}

    event = event_hook_request.event
    if event and event.type == SlackEventType.BOT_MESSAGE:
        return Response()
    if event and event.type == SlackEventType.MESSAGE and event.bot_profile:
        return Response()
    if event and event.type == SlackEventType.MESSAGE and not event.bot_profile:
        slack_client.chat_postMessage(
            channel=event.channel,
            text=f"Another message for {event.user}: {event.text}",
        )
        return Response()

    raise HTTPException(status_code=500, detail="Failed to handle hook")
