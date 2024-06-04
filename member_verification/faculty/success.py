import hikari
from bot_variables import state
from bot_variables.config import ClassType, EnrolmentSprdsht, SpecialChars
from wrappers.utils import FormatText
from member_verification.response import Response


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
        ctype_faculty_col = EnrolmentSprdsht.Routine.CLASS_TYPE_FACULTY_COL[ctype]
        filt = state.df_routine[ctype_faculty_col].str.contains(initial)
        ctype_sections = state.df_routine.loc[filt, EnrolmentSprdsht.Routine.SECTION_COL].values
        ctype_sec_roles = [state.sec_roles[sec][ctype] for sec in ctype_sections]
        for role in ctype_sec_roles:
            print(FormatText.status(f"Assigning Section Role: @{role.name}"))
            await faculty.add_role(role)
        if ctype_sections.any():
            role = state.faculty_sub_roles[ctype]
            print(FormatText.status(f"Assigning Faculty Role: @{role.name}"))
            await faculty.add_role(role)
        # print information
        embed_field_title = f"{ctype.title()} Sections"
        if ctype_sec_roles:
            all_ctype_role_names = ", ".join('@'+role.name for role in ctype_sec_roles)
            all_ctype_role_mentions = ", ".join(role.mention for role in ctype_sec_roles)
            embed_fields.append(hikari.EmbedField(name=embed_field_title, 
                                                  value=all_ctype_role_mentions))
        else:
            embed_fields.append(hikari.EmbedField(name=embed_field_title, 
                                                  value=SpecialChars.ZERO_WIDTH_SPACE))
    comment = "You have been assigned the following sections."
    return Response(comment, kind=Response.Kind.SUCCESSFUL, inline_embed_fields=embed_fields)