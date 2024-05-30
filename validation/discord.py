from bot_variables import state
from bot_variables.config import ClassType, RoleName
from wrappers.utils import FormatText, get_role_by_name, create_role_from_template


def get_sec_role_name(section: int, class_type: ClassType):
    return RoleName.SECTION[class_type].format(section)

def get_sec_role(section: int, class_type: ClassType):
    return get_role_by_name(get_sec_role_name(section, class_type))

# check if all sections' (except sec 1) roles and channels are in server
async def check_discord_sec():
    for class_type in ClassType.BOTH:
        for sec in state.available_sections[1:]:
            role = get_sec_role(sec, class_type)
            if not role:
                role = await create_sec_role(sec, class_type)

# async def check_discord_sec(info):
#     # skip section 01, works as template
#     for ctype in literals.class_types:
#         prev_category = get_sec_category(1, ctype)
#         for sec in vars.available_sections[1:]:
#             role = get_sec_role(sec, ctype)
#             if not role:
#                 role = await create_sec_role(sec, ctype)
#             category = get_sec_category(sec, ctype)
#             if not category:
#                 category = await create_sec_category(sec, ctype, role)
#             # reorder: theory of all sections, then labs of all sections
#             await category.move(after=prev_category)
#             prev_category = category


async def create_sec_role(section: int, class_type: ClassType):
    template_role = get_sec_role(1, class_type)
    role_name = get_sec_role_name(section, class_type)
    new_role = await create_role_from_template(role_name, template_role)
    return new_role