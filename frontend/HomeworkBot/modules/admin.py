"""Reload command for HomeworkBot"""
from typing import Union
import tanjun
import hikari
from pathlib import Path
import os
import logging

from HomeworkBot.core.bot import BotCore
from HomeworkBot.core.api import ApiUser

component = tanjun.Component(name="reload")
admin = tanjun.slash_command_group("admin", "admin commands", default_member_permissions=hikari.Permissions.ADMINISTRATOR, default_to_ephemeral=True)
logger = logging.getLogger(__name__)

def get_modules():
    files = os.listdir('./HomeworkBot/modules/')
    files_no_extention = [x.split('.')[0] for x in files]
    choices = {}
    for module in files_no_extention:
        choices[str(module)] = str(module)
    choices["all"] = "all"
    choices.pop("__pycache__")
    return choices


@tanjun.with_str_slash_option("module", "The module to reload.")
@admin.as_sub_command("reload", "Reloads a specific module.")
async def reload_module(
    ctx: tanjun.abc.SlashContext, module: str, client: tanjun.Client = tanjun.injected(type=tanjun.Client)
):
    """Reload a module in Tanjun"""
    if module == "all":
        try:
            client.reload_modules(*Path("./HomeworkBot/modules").glob("*.py"))
        except ValueError as e:
            logger.exception(e)
            await ctx.respond("Couldn't reload module...")
            return
    else:
        try:
            client.reload_modules(Path(f'./HomeworkBot/modules/{module}.py'))
        except ValueError as e:
            logger.exception(e)
            await ctx.respond("Couldn't reload module...")
            return

    await client.declare_global_commands()
    await ctx.respond("Reloaded!")


@tanjun.with_str_slash_option("module", "The module to unload.")
@admin.as_sub_command("unload", "Unload a module.")
async def unload_module(
    ctx: tanjun.abc.SlashContext, module: str, client: tanjun.Client = tanjun.injected(type=tanjun.Client)
):
    """Unload a module in Tanjun"""
    if module == "all":
        try:
            client.unload_modules(*Path("./HomeworkBot/modules").glob("*.py"))
        except ValueError as e:
            logger.exception(e)
            await ctx.respond("Couldn't unload module...")
            return
    else:
        try:
            client.unload_modules(Path(f'./HomeworkBot/modules/{module}.py'))
        except ValueError as e:
            logger.exception(e)
            await ctx.respond("Couldn't unload module...")
            return

    await client.declare_global_commands()
    await ctx.respond("Unloaded!")

@tanjun.with_str_slash_option("module", "The module to load.")
@admin.as_sub_command("load", "Load a module.")
async def load_module(
    ctx: tanjun.abc.SlashContext, module: str, client: tanjun.Client = tanjun.injected(type=tanjun.Client)
):
    """Unload a module in Tanjun"""
    if module == "all":
        try:
            client.load_modules(*Path("./HomeworkBot/modules").glob("*.py"))
        except ValueError as e:
            logger.exception(e)
            await ctx.respond("Couldn't load module...")
            return
    else:
        try:
            client.load_modules(Path(f'./HomeworkBot/modules/{module}.py'))
        except ValueError as e:
            logger.exception(e)
            await ctx.respond("Couldn't load module...")
            return

    await client.declare_global_commands()
    await ctx.respond("Loaded module!")

@load_module.with_str_autocomplete("module")
@unload_module.with_str_autocomplete("module")
@reload_module.with_str_autocomplete("module")
async def modules_autocomplete(ctx: tanjun.abc.AutocompleteContext, value: str):
    await ctx.set_choices(get_modules())


@tanjun.with_user_slash_option("user", "The user to delete.")
@admin.as_sub_command("delete_user", "Load a module.")
async def load_module(
    ctx: tanjun.abc.SlashContext, user: Union[hikari.InteractionMember, hikari.User], client: tanjun.Client = tanjun.injected(type=tanjun.Client)
):
    """Delete a user"""
    deleted_user = BotCore.api.delete_user(user.id)
    print(deleted_user)
    if type(deleted_user) == ApiUser:
        print(deleted_user.username)
        await ctx.respond(embed=hikari.Embed(title="Deleted user", color=hikari.Color(0x008000), description=f"Deleted account for {deleted_user.username}."))
    else:
        await ctx.respond(embed=hikari.Embed(title="Could not delete user", color=hikari.Color(0xFF051A), description="Are you sure the user has registered an account?"))

loader = component.load_from_scope().make_loader()