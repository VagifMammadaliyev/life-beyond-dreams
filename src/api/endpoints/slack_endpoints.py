from typing import Dict, Any

import slack
from fastapi import Response
from fastapi.routing import APIRouter

from api.constants import SlackEventHookType, SlackEventType
from api.exceptions import ForbiddenError, ServerError, ClientError
from api.schemas import SlackEventHookRequest
from core import conf
from services.bot import Bot


router = APIRouter(prefix="/slack", tags=["slack"])
slack_client = slack.WebClient(token=conf.SLACK_BOT_TOKEN)


def _handle_url_verification(
    event_hook_request: SlackEventHookRequest,
) -> Dict[str, Any]:
    return {"challenge": event_hook_request.challenge}


async def _handle_event_callback(event_hook_request: SlackEventHookRequest) -> Response:
    event = event_hook_request.event
    if not event:
        raise ClientError(error_data={"event": "field is missing"})
    if event.type == SlackEventType.BOT_MESSAGE:
        return Response()
    if event.type == SlackEventType.MESSAGE:
        if event.bot_profile:
            return Response()
        bot_message = await Bot().respond(event.user, event.text)
        slack_client.chat_postMessage(channel=event.channel, text=bot_message)
        return Response()
    raise ServerError(
        detail="Cannot handle this event",
        error_data={"event_type": event.type},
    )


@router.post("/event-hook")
async def event_hook(event_hook_request: SlackEventHookRequest):
    if event_hook_request.token != conf.SLACK_VERIFICATION_TOKEN:
        raise ForbiddenError

    if event_hook_request.type == SlackEventHookType.URL_VERIFICATION:
        return _handle_url_verification(event_hook_request)

    if event_hook_request.type == SlackEventHookType.EVENT_CALLBACK:
        return await _handle_event_callback(event_hook_request)

    raise ServerError(
        detail="Cannot handle this event hook",
        error_data={"event_hook_type": event_hook_request.type},
    )
