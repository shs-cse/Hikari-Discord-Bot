import hikari, miru
from member_verification.response import build_response
from member_verification.student.sucess import verify_student
from wrappers.utils import FormatText


# # TODO: persistent view?
# class VerificationButtonView(miru.View):
#     timeout = None
    
#     @miru.button(label="Verify Me!", style=hikari.ButtonStyle.PRIMARY, custom_id="student_verification_button")
#     async def student_verification_button(self, ctx: miru.ViewContext, button: miru.Button):
#         ctx.respond_with_modal(StudentIdModalView())
        
        
# # TODO: persistent view?
# class StudentIdModalView(miru.Modal):
#     def __init__(self):
#         super().__init__(title="Student Verification Form", timeout=None,
#                          custom_id="student_verification_modal")
#     student_id = miru.TextInput(label="What's your ***Student ID***?",
#                                 custom_id="student_verification_modal_textinput_1",
#                                 placeholder="00000000",
#                                 min_length=8,
#                                 max_length=8,
#                                 required=True)
#     retyped_id = miru.TextInput(label="Retype your ***Student ID***.",
#                                 custom_id="student_verification_modal_textinput_2",
#                                 placeholder="00000000",
#                                 min_length=8,
#                                 max_length=8,
#                                 required=True)
#     async def callback(self, ctx: miru.ModalContext) -> None:
#         await ctx.defer(hikari.ResponseType.DEFERRED_MESSAGE_CREATE, 
#                         flags=hikari.MessageFlag.EPHEMERAL)
#         try:
#             response = await check_student(ctx.member, self.student_id.value, 
#                                               self.retyped_id.value)
#         except Exception as error:
#             response = get_response_for_error(error, 'check_student')
#             print(FormatText.error(f"Student Verification: raised an error while trying to submit a modal for {self.student_id.value}."))
#         await ctx.respond(**response, flags=hikari.MessageFlag.EPHEMERAL)
            
    


class YesNoButtonsView(miru.View): # TODO: shift it to a different folder called view_components
    def __init__(self, member: hikari.Member, student_id: int) -> None:
        self.member = member
        self.student_id = student_id
        # set a timeout of 30 seconds
        super().__init__(timeout=30)
    
    @miru.button(label="YES, Use This Alt Account!", style=hikari.ButtonStyle.DANGER)
    async def yes_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        self.stop()
        try:
            response = await verify_student(self.member, self.student_id)
        except Exception as error:
            response = get_response_for_error(error, 'verify_student')
            print(FormatText.error(f"Student Verification: {self.member.mention} tried to take {self.student_id} with alt account; but raised error."))
        await ctx.edit_response(**response)
        
    @miru.button(label="NO, I'll Use Advising Server Account.", style=hikari.ButtonStyle.PRIMARY)
    async def no_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        self.stop()
        comment = "You selected **\"NO\"**. Please try again with your **advising server account**."
        print(FormatText.success(FormatText.dim(f"Student Verification: {self.member.mention} chose to take {self.student_id} with advising server account.")))
        response = build_response(comment)
        await ctx.edit_response(**response)
        
        
def get_response_for_error(error: Exception, function_name: str):
    comment = "Something went wrong while verifying you." 
    comment += " Please show this message to admins."
    comment += f"\nEncountered error while calling `{function_name}(...)`:"
    comment += f"\n```py\n{type(error).__name__}\n{error}```"
    return build_response(comment)
    