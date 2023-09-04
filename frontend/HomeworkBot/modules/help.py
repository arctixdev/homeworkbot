"""Help command for HomeworkBot"""
import tanjun
import hikari

component = tanjun.Component(name="help")


@component.with_slash_command
@tanjun.as_slash_command("help", "Get help about the bot.")
async def help(ctx: tanjun.abc.Context) -> None:
    await ctx.respond(embed=hikari.Embed(title="Help", description="This is the homework bot. It is a bot for managing homework."))


loader = component.load_from_scope().make_loader()
