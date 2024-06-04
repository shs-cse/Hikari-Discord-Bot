import hikari.emojis
import hikari, miru
from sync_with_servers.sheets import update_routine
from member_verification.response import get_generic_error_response_while_verifying
from member_verification.faculty.check import try_faculty_verification
from wrappers.utils import FormatText


class AssignSectionsButtonView(miru.View):
    def __init__(self) -> None:
        self.post_content = "## You *should* able to see your assigned sections.\n"
        self.post_content += "If not, (maybe there has been a change in the routine),"
        self.post_content += " please press the button below."
        super().__init__(timeout=None)
    
    
    @miru.button(label="Assign Me Sections (again...)", 
                 emoji='🧑‍🏫',
                 custom_id="faculty_assign_sections_button",
                 style=hikari.ButtonStyle.SUCCESS)
    async def faculty_assign_sections_button(self, ctx: miru.ViewContext, button: miru.Button):
        await ctx.defer(hikari.ResponseType.DEFERRED_MESSAGE_CREATE, 
                        flags=hikari.MessageFlag.EPHEMERAL)
        try:
            update_routine()
            response = await try_faculty_verification(ctx.member)
        except Exception as error:
            response = get_generic_error_response_while_verifying(error, try_faculty_verification)
            msg = f"Faculty Verification: raised an error while trying to assgin sections to {ctx.member.display_name} {ctx.member.mention}."
            print(FormatText.error(msg))
        await ctx.respond(**response)