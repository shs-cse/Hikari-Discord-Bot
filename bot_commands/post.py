import hikari, crescent
from bot_variables import state
from bot_variables.config import RolePermissions
from view_components.student_verification.modal_and_button import VerificationButtonView
from view_components.faculty_verification.assign_sec_button import AssignSectionsButtonView
from member_verification.student.check import check_student_verification

plugin = crescent.Plugin[hikari.GatewayBot, None]()

faculty_post_group = crescent.Group("post", default_member_permissions=RolePermissions.FACULTY)

@plugin.include
@faculty_post_group.child
@crescent.command(name="marks")
async def post_marks(ctx: crescent.Context) -> None:
    await ctx.defer(ephemeral=True)
    await ctx.respond(f"Not implemented yet.")
    

bot_admin_post_group = crescent.Group("post", default_member_permissions=RolePermissions.BOT_ADMIN)
bot_admin_post_button_sub_group =  bot_admin_post_group.sub_group("button")


@plugin.include
@bot_admin_post_button_sub_group.child
@crescent.command(name="student-verification")
async def post_student_verification_button(ctx: crescent.Context) -> None:
    await ctx.defer()
    view = VerificationButtonView()
    await ctx.respond(view.post_content, components=view)
    state.miru_client.start_view(view, bind_to=None)
    
    
@plugin.include
@bot_admin_post_button_sub_group.child
@crescent.command(name="faculty-assign-sections")
async def post_faculty_section_assignment_button(ctx: crescent.Context) -> None:
    await ctx.defer()
    view = AssignSectionsButtonView()
    await ctx.respond(view.post_content, components=view)
    state.miru_client.start_view(view, bind_to=None)
    