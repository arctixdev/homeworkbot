import miru
import hikari
from HomeworkBot.helpers.homework_modals import HomeworkModal

class HomeworkView(miru.View):
    @miru.button(label="Normal homework", emoji="📝")
    async def add_homework_two(self, button: miru.Button, ctx: miru.ViewContext):
        modal = HomeworkModal(title="Add Homework")
        await ctx.respond_with_modal(modal)