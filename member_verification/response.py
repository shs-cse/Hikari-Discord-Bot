import hikari, miru
from bot_variables import state

# Raise this error after building a response if a check fails.
# As a result, following checks are not performed and immediately responded.
class VerificationFailure(Exception):
    def __init__(self, response: dict) -> None:
        self.response = response
        

# build response from comment and embed fields
def build_response(comment: str, 
                   success_level: float = 0, # 0: fail, 0.5: warn, 1: success
                   inline_embed_fields: list[hikari.EmbedField] = None,
                   components: miru.View = None):
    if success_level >= 1:
        embed = hikari.Embed(title=":white_check_mark: Your account has been verified",
                                description=comment, color=0x43B581)
    elif success_level <= 0:
        embed = hikari.Embed(title=":x: Your account could not be verified",
                                description=comment, color=0xF04747)
    else:
        embed = hikari.Embed(title=":warning: Waiting for your response (Timer: 30 sec)",
                                description=comment, color=0xFFC72B)
    if inline_embed_fields:
        for field in inline_embed_fields:
            embed.add_field(field.name, field.value, inline=True)
    if components:
        state.miru_client.start_view(components)
    return {'embed': embed, 'components': components}



def get_generic_response_for_verification_error(error: Exception, func):
    comment = "Something went wrong while verifying you." 
    comment += " Please show this message to admins."
    comment += f"\nEncountered error while calling `{func.__name__}(...)`:"
    comment += f"\n```py\n{type(error).__name__}\n{error}```"
    return build_response(comment)