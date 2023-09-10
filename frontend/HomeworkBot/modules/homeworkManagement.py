"""Homework commands for HomeworkBot"""
import tanjun
import hikari
from HomeworkBot.core.bot import BotCore
from HomeworkBot.core.api import ApiUser
from HomeworkBot.helpers.homework_modals import HomeworkAddModal
import miru
from miru.ext import nav

component = tanjun.Component(name="homework")
homework = tanjun.slash_command_group(
    "homework", "homework commands", default_to_ephemeral=False
)


@component.with_slash_command
@homework.as_sub_command("create", "Create a homework.")
async def create(ctx: tanjun.abc.AppCommandContext) -> None:
    modal = HomeworkAddModal(title="Add Homework")
    await modal.send(ctx.interaction)

@component.with_slash_command
@homework.as_sub_command("list", "List remaining homework.")
async def list(ctx: tanjun.abc.AppCommandContext) -> None:
    homeworks = BotCore.api.get_user_homework(discord_id=ctx.author.id)

    pages = []

    for homework in homeworks:
        if not homework['progress'] == 0:
            continue
        pages.append(
            hikari.Embed(
                title=homework["homework"]["name"],
                description=homework["homework"]["link"],
            )
            .set_author(name=homework["homework"]["subject"])
            .set_footer(text=f"Created at {homework['homework']['created_at']}")
        )


    if len(pages) > 0:
        navigator = nav.NavigatorView(pages=pages)

        await navigator.send(to=ctx.interaction, ephemeral=False)
    else:
        await ctx.respond(embed=hikari.Embed(title="No homework", description="You have no homework.", color=hikari.Color(0xFF0000)))

@component.with_slash_command
@tanjun.with_str_slash_option("homework", "The homework to mark finished.")
@homework.as_sub_command("finish", "Mark a homework finished.")
async def finish(ctx: tanjun.abc.AppCommandContext, homework) -> None:
    homework = BotCore.api.finish_homework(homework_id=homework)

    if homework:
        await ctx.respond(embed=hikari.Embed(title="Finished homework", description=f"Finished homework {homework['homework']['name']}."))
    else:
        await ctx.respond(embed=hikari.Embed(title="Error", description="Couldn't finish homework.", color=hikari.Color(0xFF0000)))

@finish.with_str_autocomplete("homework")
async def homework_autocomplete(ctx: tanjun.abc.AutocompleteContext, value: str):
    homeworks = BotCore.api.get_user_homework(discord_id=ctx.author.id)
    
    homework_options = {}

    for homework in homeworks:
        homework_options[str(homework['homework']["name"])] = homework["id"]

    await ctx.set_choices(homework_options)


loader = component.load_from_scope().make_loader()
