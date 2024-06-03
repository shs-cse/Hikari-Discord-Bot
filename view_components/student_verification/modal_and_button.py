from datetime import timedelta
import hikari.emojis
import hikari, miru
from member_verification.response import get_generic_response_for_verification_error
from member_verification.student.check import check_student_verification
from wrappers.utils import FormatText


class VerificationButtonView(miru.View):
    def __init__(self) -> None:
        self.post_content = "## Please click to *verify* yourself!!\n"
        self.post_content += "Otherwise you **won't** be able to see much of the server,"
        self.post_content += " including your own *section announcements* and *study-materials*."
        super().__init__(timeout=None)
        
    @miru.button(label="I'm an S.T.",
                 emoji='🧑‍🏫', 
                 custom_id="st_verification_button",
                 style=hikari.ButtonStyle.SECONDARY)
    async def st_verification_button(self, ctx: miru.ViewContext, button: miru.Button):
        # await ctx.respond_with_modal(StudentIdModalView())
        from bot_variables import state
        await ctx.respond(f"Report to {state.admin_role.mention}s.", flags=hikari.MessageFlag.EPHEMERAL)
    
    @miru.button(label="I'm a Student", 
                 emoji='🙋',
                 custom_id="student_verification_button",
                 style=hikari.ButtonStyle.SUCCESS)
    async def student_verification_button(self, ctx: miru.ViewContext, button: miru.Button):
        await ctx.respond_with_modal(StudentIdModalView())
        

class StudentIdModalView(miru.Modal):
    def __init__(self):
        super().__init__(title="Student Verification Form", timeout=None,
                         custom_id="student_verification_modal")
    student_id = miru.TextInput(label="What's your ***Student ID***?",
                                custom_id="student_verification_modal_textinput_1",
                                placeholder="00000000",
                                min_length=8,
                                max_length=8,
                                required=True)
    retyped_id = miru.TextInput(label="Retype your ***Student ID***.",
                                custom_id="student_verification_modal_textinput_2",
                                placeholder="00000000",
                                min_length=8,
                                max_length=8,
                                required=True)
    async def callback(self, ctx: miru.ModalContext) -> None:
        await ctx.defer(hikari.ResponseType.DEFERRED_MESSAGE_CREATE, 
                        flags=hikari.MessageFlag.EPHEMERAL)
        try:
            response = await check_student_verification(ctx.member, self.student_id.value, 
                                              self.retyped_id.value)
        except Exception as error:
            response = get_generic_response_for_verification_error(error, check_student_verification)
            print(FormatText.error(f"Student Verification: raised an error while trying to submit a modal for {self.student_id.value}/{self.retyped_id.value}."))
        await ctx.respond(**response, flags=hikari.MessageFlag.EPHEMERAL)