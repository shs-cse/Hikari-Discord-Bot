import hikari, crescent
from bot_variables import state
from bot_variables.config import InfoField, RolePermissions
from wrappers.jsonc import update_info_field
from setup_validation.google_sheets import check_marks_groups_and_sheets

plugin = crescent.Plugin[hikari.GatewayBot, None]()

bot_admin_marks_group = crescent.Group(
    "marks", default_member_permissions=RolePermissions.BOT_ADMIN
)


# @admin enable marks -> check and be ready to load marks.
@plugin.include
@bot_admin_marks_group.child
@crescent.command(name="enable")
async def marks_enable(ctx: crescent.Context) -> None:
    await ctx.defer(ephemeral=True)
    if state.info[InfoField.MARKS_ENABLED]:
        msg = "Marks feature is already enabled."
    else:
        update_info_field(InfoField.MARKS_ENABLED, True)
        check_marks_groups_and_sheets()
        msg = "Marks feature has been enabled."
        msg += " All previously published marks has to be republished by faculties."
    await ctx.respond(msg)


# @admin disable marks -> turn off all button, clear variables to save memory.
@plugin.include
@bot_admin_marks_group.child
@crescent.command(name="disable")
async def marks_disable(ctx: crescent.Context) -> None:
    await ctx.defer(ephemeral=True)
    if not state.info[InfoField.MARKS_ENABLED]:
        msg = "Marks feature is already disabled."
    else:
        update_info_field(InfoField.MARKS_ENABLED, False)
        ...  # TODO: delete variables to save memory
        msg = "Marks feature has been disabled."
    await ctx.respond(msg)


# TODO: @faculty publish marks -> print and post error if marks not enabled, else post marks button

# faculty_post_group = crescent.Group("publish", default_member_permissions=RolePermissions.FACULTY)

# @plugin.include
# @faculty_post_group.child
# @crescent.command(name="marks")
# async def post_marks(ctx: crescent.Context) -> None:
#     await ctx.defer(ephemeral=True)
#     await ctx.respond(f"Not implemented yet.")
