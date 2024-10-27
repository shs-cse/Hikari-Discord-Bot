import hikari, crescent
from bot_variables import state
from bot_variables.config import RolePermissions, InfoField
from setup_validation.google_sheets import check_marks_groups, check_marks_sheet
from wrappers import jsonc

plugin = crescent.Plugin[hikari.GatewayBot, None]()

# faculty_post_group = crescent.Group("publish", default_member_permissions=RolePermissions.FACULTY)

@plugin.include
@crescent.command(name='marks', default_member_permissions=RolePermissions.BOT_ADMIN)
class EnableMarks:
    set_to = crescent.option(int, name='set-to',
                             choices=[('enable',1),('disable',0)], 
                             description="Enables or disables marks")
    
    async def callback(self, ctx: crescent.Context) -> None:
        await ctx.defer()
        jsonc.update_info_field(InfoField.MARKS_ENABLED, bool(self.set_to))
        ... # TODO: init/delete marks things
        if state.info[InfoField.MARKS_ENABLED]:
            check_marks_groups(state.info[InfoField.ENROLMENT_SHEET_ID])
            for email, marks_group in state.info[InfoField.MARKS_GROUPS].items():
                for section in marks_group:
                    check_marks_sheet(section, email, marks_group, 
                                    state.info[InfoField.MARKS_SHEET_IDS].copy())
        ...
        msg = 'enabled' if state.info[InfoField.MARKS_ENABLED] else 'disabled'
        await ctx.respond(f"Marks spreadsheets are {msg} for all sections.")

# @plugin.include
# @faculty_post_group.child
# @crescent.command(name="marks")
# async def post_marks(ctx: crescent.Context) -> None:
#     await ctx.defer(ephemeral=True)
#     await ctx.respond(f"Not implemented yet.")