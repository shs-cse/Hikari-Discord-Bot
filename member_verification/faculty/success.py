import hikari
from bot_variables import state
from bot_variables.config import ClassType, EnrolmentSprdsht
from wrappers.utils import FormatText
from member_verification.response import build_response


# assign theory/lab roles and section roles to faculty
async def assign_faculty_section_roles(faculty: hikari.Member, initial: str):
    # remove exisiting section role, if any
    for role in faculty.get_roles():
        # TODO: remove student and st roles as well
        is_theory_role = (role == state.faculty_sub_roles[ClassType.THEORY])
        is_lab_role = (role == state.faculty_sub_roles[ClassType.LAB])
        if (role in state.all_sec_roles) or is_theory_role or is_lab_role:
            await faculty.remove_role(role)
    # add new roles # TODO: old code logic
    embed_fields = []
    for ctype in ClassType.BOTH:
        filt = state.df_routine[f"{ctype.title()} Teacher"].str.contains(initial)
        ctype_sections = state.df_routine.loc[filt, EnrolmentSprdsht.Routine.SECTION_COL].values
        ctype_roles = [state.sec_roles[sec][ctype] for sec in ctype_sections]
        for role in ctype_roles:
            await faculty.add_role(role)
        if ctype_sections.any():
            await faculty.add_role(state.faculty_sub_roles[ctype])
        # print information
        all_ctype_roles = "\u200b" if not ctype_roles else ", ".join(
                role.mention for role in ctype_roles)
        embed_fields.append(hikari.EmbedField(name=f"{ctype.title()} Sections", 
                                              value=all_ctype_roles))
    print(FormatText.status(f"Assigned Roles: {', '.join(role.name for role in faculty.get_roles())}"))
    comment = "You have been given the following sections."
    return build_response(comment, success_level=1, inline_embed_fields=embed_fields)