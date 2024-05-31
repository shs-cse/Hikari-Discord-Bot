import hikari
from bot_variables import state
from bot_variables.config import ClassType, RoleName, ChannelName
from wrappers.utils import FormatText, get_role_by_name, create_role_from_template, get_channel_by_name, create_channel_from_template


def get_sec_role_name(section: int, class_type: ClassType):
    return RoleName.SECTION[class_type].format(section)

def get_sec_role(section: int, class_type: ClassType):
    return get_role_by_name(get_sec_role_name(section, class_type))

def get_sec_category_name(section: int, class_type: ClassType):
    return ChannelName.SECTION[class_type].format(section)

def get_sec_category(section: int, class_type: ClassType):
    return get_channel_by_name(get_sec_category_name(section, class_type))

# check if all sections' (except sec 01) roles and channels are in server
async def check_discord_sec():
    for class_type in ClassType.BOTH:
        for sec in state.available_sections[1:]:
            role = get_sec_role(sec, class_type)
            if not role:
                role = await create_sec_role(sec, class_type)
            category: hikari.GuildCategory = get_sec_category(sec, class_type)
            if not category:
                category = await create_sec_category(sec, class_type, role)
        # reorder sec 01 lab after all theories
        if class_type == ClassType.THEORY:
            last_theory_category = category
    await get_sec_category(1,ClassType.LAB).edit(position=last_theory_category.position+1)


async def create_sec_role(section: int, class_type: ClassType):
    template_role = get_sec_role(1, class_type)
    role_name = get_sec_role_name(section, class_type)
    new_role = await create_role_from_template(role_name, template_role)
    return new_role


def load_sec_template(class_type: ClassType):
    if state.sec_template[class_type]:
        return
    # fetch template
    template_role = get_sec_role(1, class_type)
    template_category = get_sec_category(1, class_type)
    # update state variable
    state.sec_template[class_type] = {
        'role': template_role,
        'category': template_category,
        'channels': [
            channel for _, channel in state.guild.get_channels().items()
                if channel.parent_id == template_category.id
        ]
    }


async def create_sec_category(section: int, class_type: ClassType, new_role: hikari.Role):
    # fetch template from section 01
    load_sec_template(class_type)
    # clone category with permissions
    category_name = get_sec_category_name(section, class_type)
    new_category = await create_channel_from_template(category_name, 
                                                      new_role, 
                                                      state.sec_template[class_type]['category'], 
                                                      state.sec_template[class_type]['role'])
    # clone channels under template category
    for template_channel in state.sec_template[class_type]['channels']:
        await create_channel_from_template(template_channel.name, 
                                           new_role,
                                           template_channel, 
                                           state.sec_template[class_type]['role'], 
                                           new_category)
    return new_category