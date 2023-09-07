import hikari
import tanjun
import logging
from pathlib import Path

from HomeworkBot.core.api import apiInterface

import tanjun
from hikari import Embed
from hikari import Color
import miru

logger = logging.getLogger(__name__)

async def error_hook(ctx: tanjun.abc.Context, error: Exception):
    await ctx.respond(embed=Embed(title="Oh no!", color=Color(0xFF051A), description=error))

class BotCore:
    bot: hikari.GatewayBot
    client: tanjun.Client
    api: apiInterface = apiInterface()

    def __init__(self, TOKEN: str):
        print("Starting Bot, GraphQL interface and logger")
        BotCore.bot = hikari.GatewayBot(TOKEN)
        logger.info("Created `bot`")

        BotCore.client = tanjun.Client.from_gateway_bot(
            BotCore.bot, declare_global_commands=True, mention_prefix=True
        )
        miru.install(BotCore.bot)

        logger.info("Created `client`, loading modules")
        BotCore.client.load_modules(*Path("./HomeworkBot/modules").glob("*.py"))
        hook = tanjun.AnyHooks().set_on_error(error_hook)
        BotCore.client.set_hooks(hook)

        logger.info("Loaded commands, starting bot")        
        BotCore.bot.run()
