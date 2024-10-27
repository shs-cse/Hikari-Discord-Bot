import hikari, crescent
from bot_variables import state
from bot_variables.config import RolePermissions, InfoField
from setup_validation.google_sheets import check_marks_groups, check_marks_sheet
from wrappers import jsonc

plugin = crescent.Plugin[hikari.GatewayBot, None]()

bot_admin_marks_group = crescent.Group("marks", default_member_permissions=RolePermissions.BOT_ADMIN) 
# faculty_post_group = crescent.Group("publish", default_member_permissions=RolePermissions.FACULTY)

@plugin.include
@bot_admin_marks_group.child
@crescent.command(name='enable')
async def enable_marks(ctx: crescent.Context) -> None:
        await ctx.defer()
        jsonc.update_info_field(InfoField.MARKS_ENABLED, True)
        ... # TODO: init/delete marks things
        check_marks_groups(state.info[InfoField.ENROLMENT_SHEET_ID])
        for email, marks_group in state.info[InfoField.MARKS_GROUPS].items():
            for section in marks_group:
                check_marks_sheet(section, email, marks_group, 
                                state.info[InfoField.MARKS_SHEET_IDS].copy())
        ...
        await ctx.respond("Marks spreadsheets are enabled for all sections.")
        
        
# @plugin.include
# @bot_admin_marks_group.child
# @crescent.command(name='disable')
# async def disable_marks(ctx: crescent.Context) -> None:
#         await ctx.defer()
#         jsonc.update_info_field(InfoField.MARKS_ENABLED, False)
#         ... # TODO: init/delete marks things
#         await ctx.respond("Marks spreadsheets are disabled for all sections.")
        
        

# @plugin.include
# @faculty_post_group.child
# @crescent.command(name="marks")
# async def post_marks(ctx: crescent.Context) -> None:
#     await ctx.defer(ephemeral=True)
#     await ctx.respond(f"Not implemented yet.")