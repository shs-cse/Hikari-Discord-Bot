from wrappers.utils import FormatText
from wrappers.discord import get_role_by_name
from bot_variables import state
from bot_variables.config import RoleName, ClassType
from validation.discord_sec import check_discord_sec


async def now():
    print(FormatText.wait("Syncing roles..."))
    state.admin_role = get_role_by_name(RoleName.ADMIN)
    state.bot_admin_role = get_role_by_name(RoleName.BOT_ADMIN)
    state.faculty_role = get_role_by_name(RoleName.FACULTY)
    state.faculty_sub_roles[ClassType.THEORY] = get_role_by_name(RoleName.THEORY_FACULTY)
    state.faculty_sub_roles[ClassType.LAB] = get_role_by_name(RoleName.LAB_FACULTY)
    state.st_role = get_role_by_name(RoleName.STUDENT_TUTOR)
    state.student_role = get_role_by_name(RoleName.STUDENT)
    await check_discord_sec()
    state.all_sec_roles = {roles[class_type] 
                           for roles in state.sec_roles.values()
                           for class_type in ClassType.BOTH}
    print(FormatText.success("Syncing roles complete."))