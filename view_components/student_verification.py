import hikari, miru
from member_verification.response import build_response_for_students, verify_student
from wrappers.utils import FormatText


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
            comment = "Something went wrong while verifying you." 
            comment += " Please show this message to admins."
            comment += "\nEncountered error while calling `verify_student(...)`:"
            comment += f"\n```py\n{type(error).__name__}\n{error}```"
            print(FormatText.error(f"Student Verification: {self.member.mention} tried to take {self.student_id} with alt account; but raised error."))
            response = build_response_for_students(comment)
        await ctx.edit_response(**response)
        
    @miru.button(label="NO, I'll Use Advising Server Account.", style=hikari.ButtonStyle.PRIMARY)
    async def no_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        self.stop()
        comment = "You selected **\"NO\"**. Please try again with your **advising server account**."
        print(FormatText.success(FormatText.dim(f"Student Verification: {self.member.mention} chose to take {self.student_id} with advising server account.")))
        response = build_response_for_students(comment)
        await ctx.edit_response(**response)