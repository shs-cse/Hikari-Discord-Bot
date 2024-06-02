import hikari.emojis
import hikari, miru
from member_verification.response import build_response
from member_verification.student.check import check_student
from wrappers.utils import FormatText


class VerificationButtonView(miru.View):
    timeout = None
        
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
            response = await check_student(ctx.member, self.student_id.value, 
                                              self.retyped_id.value)
        except Exception as error:
            response = get_response_for_error(error, 'check_student')
            print(FormatText.error(f"Student Verification: raised an error while trying to submit a modal for {self.student_id.value}/{self.retyped_id.value}."))
        await ctx.respond(**response, flags=hikari.MessageFlag.EPHEMERAL)


def get_response_for_error(error: Exception, function_name: str):
    comment = "Something went wrong while verifying you." 
    comment += " Please show this message to admins."
    comment += f"\nEncountered error while calling `{function_name}(...)`:"
    comment += f"\n```py\n{type(error).__name__}\n{error}```"
    return build_response(comment)