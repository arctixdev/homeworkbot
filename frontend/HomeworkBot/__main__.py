"""Run the Discord bot for managing homework."""
import os
from HomeworkBot import __version__
from dotenv import load_dotenv
from HomeworkBot.core.bot import BotCore
import logging

logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = str(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    if os.name != "nt":
        logger.info("Not on Windows. Injecting uvloop")
        import uvloop

        uvloop.install()

    BotCore(TOKEN)
