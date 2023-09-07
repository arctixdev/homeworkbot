import miru
import hikari

from HomeworkBot.core.bot import BotCore

class HomeworkModal(miru.Modal):
    subject = miru.TextInput(label="Subject", placeholder="ex: Dansk", min_length=3, max_length=20, required=True)
    name = miru.TextInput(label="Name", placeholder="ex: Analyser en eller anden dødsyg tekst", required=True)
    link = miru.TextInput(label="Link", placeholder="ex: https://skoleportal.easyiqcloud.dk/bla", required=False)
    description = miru.TextInput(label="Description", placeholder="ex: Analyser den der random tekst om balkjoler skrevet af whatever", required=True, style=hikari.TextInputStyle.PARAGRAPH)
    date = miru.TextInput(label="Date", placeholder="format: YYYY-MM-DD, ex: 2023-09-21", required=True, min_length=10, max_length=10)

    async def callback(self, ctx: miru.ModalContext) -> None:
        BotCore.api.create_homework(
            subject=self.subject.value,
            name=self.name.value,
            link=self.link.value,
            description=self.description.value,
            date_due=self.date.value,
        )
        await ctx.respond(embed=hikari.Embed(title="Created homework!", color=hikari.Color(0x008000), description="Created homework!").add_field(name="Subject", value=self.subject.value).add_field(name="Name", value=self.name.value).add_field(name="Link", value=self.link.value).add_field(name="Description", value=self.description.value).add_field(name="Date", value=self.date.value))
