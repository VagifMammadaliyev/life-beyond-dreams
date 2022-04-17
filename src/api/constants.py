from enum import Enum


class SlackEventHookType(str, Enum):
    URL_VERIFICATION = "url_verification"
    EVENT_CALLBACK = "event_callback"


class SlackEventType(str, Enum):
    BOT_MESSAGE = "bot_message"
    MESSAGE = "message"
