import hikari
from bot_variables.config import ClassType
# everything passed to info json file
info : dict = {}
# guild related objects
guild : hikari.Guild = None
eee_guild : hikari.Guild = None

sec_template = {ClassType.THEORY: {}, ClassType.LAB: {}}

faculty_role : hikari.Role = None
faculty_sub_roles : dict = {}
st_role : hikari.Role = None
admin_role : hikari.Role = None
bot_admin_role : hikari.Role = None
student_role : hikari.Role = None

available_sections : list = []