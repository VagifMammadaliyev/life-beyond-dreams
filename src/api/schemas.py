from typing import Any, Optional

from pydantic import *

from api.constants import SlackEventHookType, SlackEventType


class SlackEvent(BaseModel):
    type: SlackEventType
    user: str
    text: str
    channel: str
    bot_profile: Optional[Any]


class SlackEventHookRequest(BaseModel):
    token: str
    type: SlackEventHookType
    challenge: Optional[Any]
    event: Optional[SlackEvent]
