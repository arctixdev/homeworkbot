import hikari
import tanjun
import logging
from pathlib import Path

import HomeworkBot.modules
from HomeworkBot.core.api import apiInterface

logger = logging.getLogger(__name__)

class HomeworkBot:
    bot: hikari.GatewayBot
    client: tanjun.Client
    apiInterface: apiInterface

    def __init__(self, TOKEN: str):
        print("Starting Bot, GraphQL interface and logger")
        HomeworkBot.apiInterface = apiInterface()
        HomeworkBot.bot = hikari.GatewayBot(TOKEN)
        logger.info("Created `bot`")

        HomeworkBot.apiInterface.get_users()

        HomeworkBot.client = tanjun.Client.from_gateway_bot(HomeworkBot.bot, declare_global_commands=True, mention_prefix=True)
        logger.info("Created `client`, loading modules")
        HomeworkBot.client.load_modules(*Path("./HomeworkBot/modules").glob("*.py"))
        logger.info("Loaded commands, starting bot")
        HomeworkBot.bot.run()