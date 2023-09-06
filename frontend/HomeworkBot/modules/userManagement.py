"""User commands for HomeworkBot"""
import tanjun
import hikari
from HomeworkBot.core.bot import BotCore
from HomeworkBot.core.api import ApiUser

component = tanjun.Component(name="user")


@component.with_slash_command
@tanjun.with_str_slash_option("nickname", "What should the bot call you?")
@tanjun.as_slash_command("register", "Register yourself as a user.")
async def register(ctx: tanjun.abc.Context, nickname: str) -> None:
    user = ApiUser(
        connection=BotCore.api.connection,
        nickname=nickname,
        username=ctx.author.username,
        discord_id=ctx.author.id,
    ).create()
    await ctx.respond(
        embed=hikari.Embed(
            title="Created user!",
            color=hikari.Color(0x008000),
            description=str(user.db_id),
        )
    )


@component.with_slash_command
@tanjun.as_slash_command("user", "get your user.")
async def user(ctx: tanjun.abc.Context) -> None:
    user = BotCore.api.get_user(discord_id=ctx.author.id)
    await ctx.respond(
        embed=hikari.Embed(title="Created hhhh", description=str(user.nickname))
    )


@component.with_slash_command
@tanjun.as_slash_command("all", "get all users.")
async def all(ctx: tanjun.abc.Context) -> None:
    users = BotCore.api.get_users()
    hah = ""
    for user in users:
        hah += user.username + ", "
    await ctx.respond(embed=hikari.Embed(title="All users:", description=hah))


loader = component.load_from_scope().make_loader()
