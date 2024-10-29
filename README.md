# ASYNC TG LOGGER

**A package designed for asynchronous logging in telegram bot**

### Example usage:

```bash
pip install git+https://github.com/MiMoody/async_tg_logger.git
```

```python
import asyncio
import logging


from async_logger import AsyncTgLoggerHandler
from async_logger.formatters import DefaultFormatter

logger = logging.getLogger("test_async_logger")


def setup_logger():
    """Set base logger settings"""

    tg_handler = AsyncTgLoggerHandler(
        token="BOT_TOKEN",
        users=[123456, 654321],
        parse_mode="HTML",
    )
    tg_handler.setFormatter(DefaultFormatter())
    tg_handler.setLevel(logging.ERROR)
    logger.addHandler(tg_handler)
    logger.setLevel(logging.INFO)


async def main():
    """Example of logging to Telegram"""
    setup_logger()

    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
```
