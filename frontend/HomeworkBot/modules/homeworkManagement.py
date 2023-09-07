"""Homework commands for HomeworkBot"""
import tanjun
import hikari
from HomeworkBot.core.bot import BotCore
from HomeworkBot.core.api import ApiUser
from HomeworkBot.helpers.homework_views import HomeworkView
from HomeworkBot.helpers.homework_modals import HomeworkModal
import miru
from miru.ext import nav

component = tanjun.Component(name="homework")
homework = tanjun.slash_command_group(
    "homework", "homework commands", default_to_ephemeral=False
)


@component.with_slash_command
@homework.as_sub_command("create", "Create a homework.")
async def create(ctx: tanjun.abc.Context) -> None:
    view = HomeworkView()
    message = await ctx.respond("Please select homework type", components=view, ensure_result=True)
    await view.start(message)

@component.with_slash_command
@homework.as_sub_command("list", "List remaining homework.")
async def list(ctx: tanjun.abc.Context) -> None:
    homeworks = BotCore.api.get_user_homework(discord_id=ctx.author.id)

    pages = []

    for homework in homeworks:
        pages.append(
            hikari.Embed(
                title=homework["homework"]["name"],
                description=homework["homework"]["link"],
            )
            .set_author(name=homework["homework"]["subject"])
            .set_footer(text=f"Created at {homework['homework']['created_at']}")
        )

    navigator = nav.NavigatorView(pages=pages)

    message = await ctx.respond(
        embed=pages[0], components=navigator, ensure_result=True
    )
    await navigator.start(message=message)


loader = component.load_from_scope().make_loader()
