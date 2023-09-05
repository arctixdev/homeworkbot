"""User commands for HomeworkBot"""
import tanjun
import hikari
from HomeworkBot.core.bot import HomeworkBot
from HomeworkBot.core.api import User

component = tanjun.Component(name="user")


@component.with_slash_command
@tanjun.with_str_slash_option("nickname", "What the bot should call you.")
@tanjun.as_slash_command("registrer", "Create a user.")
async def help(ctx: tanjun.abc.Context, nickname: str) -> None:
    userid = User(nickname=nickname, username=ctx.author.username, discord_id=ctx.author.id).create()
    await ctx.respond(embed=hikari.Embed(title="Created user", description=str(userid)))


loader = component.load_from_scope().make_loader()
