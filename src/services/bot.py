import random
from typing import Tuple
from enum import Enum

from services.utils import compare_str, analyze_words, update_stats
from repositories.dreams_repository import DreamsRepository
from repositories.stats_repository import StatsRepository
from core import db


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

    async def handle_command(self, command: BotCommand, user: str, message: str) -> str:
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
            await self.dreams_repository.save_dream(user=user, dream=message)
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

    async def respond(self, user: str, message: str) -> str:
        recognition = self.recognize_command(message)
        if recognition:
            command, message = recognition
            return await self.handle_command(command, user, message)
        return "I am not sure what you mean"
