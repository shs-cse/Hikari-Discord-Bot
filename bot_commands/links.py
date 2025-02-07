import hikari, crescent
from bot_variables import state
from bot_variables.config import RolePermissions, InfoField
from wrappers.pygs import get_link_from_sheet_id

plugin = crescent.Plugin[hikari.GatewayBot, None]()

faculty_link_group = crescent.Group("link", default_member_permissions=RolePermissions.FACULTY)

@plugin.include
@faculty_link_group.child
@crescent.command(name='invite')
async def get_invite_link(ctx: crescent.Context) -> None:
    link = state.info[InfoField.INVITE_LINK]
    await ctx.respond(f"Discord server invitation link:\n## {link}", ephemeral=True)
  
  
@plugin.include
@faculty_link_group.child
@crescent.command(name='enrolment')
async def get_enrolment_link(ctx: crescent.Context) -> None:
    sheet_id = state.info[InfoField.ENROLMENT_SHEET_ID]
    link = get_link_from_sheet_id(sheet_id)
    await ctx.respond(f"Enrolment spreadsheet link:\n## {link}", ephemeral=True)
  
  
@plugin.include
@faculty_link_group.child
@crescent.command(name='marks')
class MarksSheetLink:
    section = crescent.option(int)

    async def callback(self, ctx: crescent.Context) -> None:
        await ctx.defer(ephemeral=True)
        if self.section in state.available_sections:
            sheet_id = state.info[InfoField.MARKS_SHEET_IDS][str(self.section)]
            link = get_link_from_sheet_id(sheet_id)
            await ctx.respond(f"Marks spreadheet link for **section {self.section}**:\n## {link}")
        else:
            await ctx.respond(f"Section {self.section} does not exist.")
  
