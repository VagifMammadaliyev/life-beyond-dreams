import asyncio
import random
from enum import Enum
from typing import Tuple

import slack

from core import conf, db
from repositories.dreams_repository import DreamsRepository
from repositories.stats_repository import StatsRepository
from services.utils import analyze_words, compare_str, update_stats

slack_client = slack.WebClient(token=conf.SLACK_BOT_TOKEN)


class BotCommand(str, Enum):
    GREET = "greet"
    SAVE_DREAM = "save_dream"
    STATS = "stats"

    def get_variants(self):
        if self == BotCommand.GREET:
            return (
                "hi",
                "hello",
                "good morning",
                "morning",
            )
        elif self == BotCommand.SAVE_DREAM:
            return (
                "here is my dream",
                "dream",
                "my dream",
                "i dreamed tonight",
                "i dreamed this",
                "i dreamed",
                "my dream was",
            )
        elif self == BotCommand.STATS:
            return (
                "show stats",
                "show most used words",
                "what i see the most",
                "what my stats",
                "show numbers",
                "show words",
                "analyze my dreams",
                "popular words",
            )


class Bot:
    def __init__(self):
        self.dreams_repository = DreamsRepository(db.db_engine)
        self.stats_repository = StatsRepository(db.db_engine)

    async def notify_to_check_reality(self):
        channels = await self.dreams_repository.get_distinct_channels()
        for channel in channels:
            slack_client.chat_postMessage(
                channel=channel,
                text="Check your surroundings to confirm you are awake",
            )

    def recognize_command(self, message: str) -> Tuple[BotCommand, str]:
        splitted_message = message.split("\n")
        if len(splitted_message) > 1:
            first_line, *rest_of_message = message.split("\n")
        else:
            first_line = splitted_message[0]
            rest_of_message = first_line
        for command in BotCommand:
            if compare_str(first_line, command.get_variants()):
                if command == BotCommand.SAVE_DREAM:
                    return (command, "\n".join(rest_of_message))
                return (command, message)

    async def handle_command(
        self, command: BotCommand, channel: str, user: str, message: str
    ) -> str:
        if command == BotCommand.GREET:
            return random.choice(
                (
                    "Hello",
                    "Nice to meet you",
                    "Good morning",
                    "Morning, my dreamer",
                )
            )
        elif command == BotCommand.SAVE_DREAM:
            additional_stats = analyze_words(message)
            current_stats = await self.stats_repository.get_stats(user=user)
            new_stats = update_stats(current_stats, additional_stats)
            await self.stats_repository.save_stats(user=user, stats=new_stats)
            await self.dreams_repository.save_dream(
                user=user, channel=channel, dream=message
            )
            return "Saved your dream"
        elif command == BotCommand.STATS:
            current_stats = await self.stats_repository.get_stats(user=user)
            response_message_lines = []
            for word, count in sorted(
                current_stats.items(),
                key=lambda s: s[1],
                reverse=True,
            ):
                response_message_lines.append(f"{word} => {count}")
            return "\n".join(response_message_lines)
        return "Somehow this line is reached..."

    async def respond(self, channel: str, user: str, message: str) -> str:
        recognition = self.recognize_command(message)
        if recognition:
            command, message = recognition
            response = await self.handle_command(command, channel, user, message)
            slack_client.chat_postMessage(channel=channel, text=response)
        return "I am not sure what you mean"


async def notify_to_check_reality():
    while True:
        await Bot().notify_to_check_reality()
        await asyncio.sleep(30 * 60)


event_loop = asyncio.get_event_loop()
event_loop.create_task(notify_to_check_reality())
