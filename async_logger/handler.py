import asyncio
from enum import Enum
import io
import logging
from logging import StreamHandler

import aiogram
from aiogram.enums import ParseMode
from aiogram.types import BufferedInputFile

# logging setup
logger = logging.getLogger(__name__)


class TypeMessage(Enum):
    AUTO = "auto"
    TEXT = "text"
    DOCUMENT = "document"


class AsyncTgLoggerHandler(StreamHandler):
    """Logger handler for async_logger"""

    def __init__(
        self,
        token: str,
        users: list[int],
        loop: asyncio.AbstractEventLoop | None = None,
        parse_mode: ParseMode | None = None,
        type_message: TypeMessage = TypeMessage.AUTO,
        max_length_message: int = 4096,
    ):
        """
        Setup TgLoggerHandler class

        :param token: tg bot token to log form
        :param users: list of used_id to log to
        :param timeout: seconds for retrying to send log if error occupied
        """

        super().__init__()
        self._token = token
        self._users = users
        self._parse_mode = parse_mode
        self._type_message = type_message
        self._max_length_message: int = max_length_message
        self.setFormatter

        self._loop = loop or asyncio.get_running_loop()
        self.bot = aiogram.Bot(token=self._token)

    async def _send_message(self, user_id: int, message: str) -> None:
        await self.bot.send_message(
            user_id,
            message[: self._max_length_message],
            parse_mode=self._parse_mode,
        )

    async def _send_document(self, user_id: int, message: str) -> None:
        file_data = io.BytesIO(initial_bytes=message.encode(encoding="utf-8"))
        file_data.name = "log.txt"
        await self.bot.send_document(
            user_id,
            document=BufferedInputFile(
                filename=file_data.name, file=file_data.getvalue()
            ),
            parse_mode=self._parse_mode,
        )

    async def _send_log(self, user_id: int, message: str) -> None:
        if self._type_message == TypeMessage.TEXT:
            await self._send_message(user_id=user_id, message=message)
        elif self._type_message == TypeMessage.DOCUMENT:
            await self._send_document(user_id=user_id, message=message)
        elif self._type_message == TypeMessage.AUTO:
            if len(message) > self._max_length_message:
                await self._send_document(user_id=user_id, message=message)
            else:
                await self._send_message(user_id=user_id, message=message)
        else:
            raise ValueError("Invalid type_message value")

    async def _process_message(self, msg: str) -> None:
        for user_id in self._users:
            retry_count: int = 3
            while retry_count > 0:
                try:
                    await self._send_log(user_id, msg)
                    await asyncio.sleep(0.1)
                    break
                except Exception as exc:
                    logger.exception("Exception while sending %s to %s:", exc, user_id)
                    retry_count -= 1
                    await asyncio.sleep(0.2)

    def emit(self, record):
        self._loop.create_task(self._process_message(self.format(record)))
