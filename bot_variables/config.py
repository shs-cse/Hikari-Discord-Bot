import hikari

# aka ECT-BC server
class EEEGuild:
    Id = 815535685959811083
    
class SpecialChars:
    ZERO_WIDTH_SPACE = '\u200b'

class ClassType:
    THEORY = 'theory'
    LAB = 'lab'
    BOTH = [THEORY, LAB]

class InfoField:
    COURSE_CODE = 'course_code'
    COURSE_NAME = 'course_name'
    SEMESTER = 'semester'
    NUM_SECTIONS = 'n_sections'
    MISSING_SECTIONS = 'missing_sections'
    # tokens and ids
    ROUTINE_SHEET_ID = 'routine_sheet_id'
    MARKS_FOLDER_ID = 'enrolment_and_marks_folder_id'
    GUILD_ID = 'guild_id'
    BOT_TOKEN = 'bot_token'
    # autogenerated fields
    MARKS_ENABLED = 'marks_enabled'
    MARKS_GROUPS = 'marks_groups'
    INVITE_LINK = 'invite'
    ENROLMENT_SHEET_ID = 'enrolment'
    MARKS_SHEET_IDS = 'marks'
    
    
class RolePermissions:
    STUDENT_TUTOR = hikari.Permissions.PRIORITY_SPEAKER
    FACULTY = STUDENT_TUTOR | hikari.Permissions.MANAGE_MESSAGES | hikari.Permissions.MODERATE_MEMBERS
    BOT_ADMIN = FACULTY | hikari.Permissions.MANAGE_GUILD
    ADMIN = BOT_ADMIN | hikari.Permissions.ADMINISTRATOR


class FileName:
    GOOGLE_CREDENTIALS = 'credentials.json'
    SHEETS_CREDENTIALS = 'sheets.googleapis.com-python.json'
    INFO_JSON = 'info.jsonc'
    VALID_JSON = 'valid_info.jsonc'
    ATTENDANCE_FOLDER = 'attendance_sheets'
    COMMANDS_FOLDER = 'bot_commands'
    EVENTS_FOLDER = 'bot_events'
    BULK_DELETE = f'{COMMANDS_FOLDER}.bulk_delete'
    DISCORD_WRAPPER = 'wrappers.discord'
    DISCORD_SECTION_VALIDATION = 'setup_validation.discord_sec'


class TemplateLinks:
    GUILD = 'https://discord.new/RVh3qBrGcsxA'
    ENROLMENT_SHEET = '1rcB4O36pWhpttSiFiWyiTrDewxYTbptJDFi6HS6cekI' # '1HzCwb68D3L2sC4WFEBYajz4co5sQvtgSpp2fIf8aMqc'
    MARKS_SHEET = '1wfamZfPPXvYxHegBEngxonPtBmJBiFT5D0WAvwLchY0' # TODO: change to latest file
    

class RegexPattern:
    # course details
    COURSE_CODE = r'CSE[0-9]{3}'
    COURSE_NAME = r'(?!<).+'
    SEMESTER = r'(Fall|Spring|Summer) 20[0-9]{2}'
    # student details
    STUDENT_ID = r'[0-9]{8}'
    STUDENT_NICKNAME = r'\[[0-9]{8}\].+'
    # faculty details
    FACULTY_NICKNAME = r'^\[([A-Z0-9]{3,4})\].+'
    # google drive file/folder id
    GOOGLE_DRIVE_LINK_ID = r'(?<=/)[\w_-]{15,}|^[\w_-]{15,}'
    # discord id
    DISCORD_ID = r'[0-9]{17,19}'
    # DISCORD_BOT_TOKEN = r'^([MN][\w-]{23,25})\.([\w-]{6})\.([\w-]{27,39})$' # discord keeps changing this
    

class PullMarksGroupsFrom:
    WRKSHT = 'Routine'
    CELL = 'L2'
    
    
# all special channel names in this guild
class ChannelName:
    WELCOME = '👏🏻welcome✌🏻'
    ADMIN_HELP = '💁🏻admin-help'
    GENERAL_ANNOUNCEMENT = '📣general-announcements'
    SECTION_CATEGORY = {
        ClassType.THEORY: 'SECTION {:02d} THEORY',
        ClassType.LAB: 'SECTION {:02d} LAB',
    }
    
# all special role names in this guild
class RoleName:
    ADMIN = 'admin'
    BOT_ADMIN = 'bot-admin'
    BOT = 'bot'
    FACULTY = 'faculty'
    THEORY_FACULTY = 'theory-faculty'
    LAB_FACULTY = 'lab-faculty'
    STUDENT_TUTOR = 'student-tutor'
    STUDENT = 'student'
    SECTION = {
        ClassType.THEORY: 'sec-{:02d}',
        ClassType.LAB: 'sec-{:02d}-lab',
    }
    

class EnrolmentSprdsht:
    TITLE = '{course_code} {semester} Enrolment Manager'
    
    class StudentList:
        TITLE = 'StudentList'
        SECTION_COL = 'Section'
        STUDENT_ID_COL = 'Student ID'
        NAME_COL = 'Name'
        DISCORD_ID_COL = 'Discord ID'
        VIRTUAL_MARKS_SEC_COL = 'Marks Section'
        ADVISING_DISCORD_ID_COL = 'Discord ID (Adv. Verified)'
        
    class Routine:
        TITLE = 'Routine'
        SECTION_COL = 'Section'
        CLASS_TYPE_FACULTY_COL = {
            ClassType.THEORY: 'Theory Teacher',
            ClassType.LAB: 'Lab Teacher'
        }
        
    class UsisBefore:
        TITLE = 'USIS (before)'
        RANGE = 'B2:D'
        SECTION_COL = 'Section'
    
    class Discord:
        TITLE = 'Discord'
        RANGE = 'C2:H'
        
    class CourseInfo:
        TITLE = 'Course Info'
        CELL_TO_FILED_DICT = {
            'B2': InfoField.COURSE_CODE,
            'B3': InfoField.COURSE_NAME,
            'B6': InfoField.SEMESTER,
            'B4': InfoField.NUM_SECTIONS,
            'B5': InfoField.MISSING_SECTIONS,
            'B16': InfoField.ROUTINE_SHEET_ID
        }
    

class MarksSprdsht:
    TITLE = '{course_code}-{sections} Marks Gradesheet {semester}'
    
    class Meta:
        TITLE = 'Meta'
        CELL_TO_FILED_DICT = {
            'K2': InfoField.ENROLMENT_SHEET_ID
        }
        
    class SecXX:
        TITLE = 'Sec {:02d}'

    
# TODO: make it into class?
info_row_dict = {'Helper Text': 4, 'Parent Column': 9, 'Self Column': 14, 'Depth': 23,
                 'Total Marks': 5, 'Publish?': 1, 'Actual Marks?': 22, 'Children Columns': 17}
