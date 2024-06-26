from classes.printer import *
from classes.enumDefinitions import *
import datetime


class PermissionCode(db.Entity):
    code = Required(str, unique=True)
    """The actual code. Can be any string"""
    name = Required(str, unique=True)
    """Friendly name of the code."""
    description = Optional(str)
    """Optional description."""
    contact_info = Optional(str)
    """Optional contact info."""
    start_date = Optional(datetime.date)
    """Date the key beings being valid."""
    end_date = Optional(datetime.date)
    """Date the key stops being valid."""
    print_jobs = Set('PrintJob')
    """Used to relate print jobs to this permission code. Not an actual field, just a Pony ORM thing"""


    @staticmethod
    @db_session
    def Get_All(serialize=False):
        query_result = select(p for p in PermissionCode)
        codes = []
        for c in query_result:
            codes.append(c)
        if serialize:
            return PermissionCode.Serialize_Codes_For_Permission_Code_Menu(codes)
        return codes

    @staticmethod
    @db_session
    def Get_By_Id(permission_code_id):
        return PermissionCode.get(id=permission_code_id)

    @staticmethod
    @db_session
    def Get_All_Active():
        now = datetime.date.today()
        query_result = select(c for c in PermissionCode if (c.start_date is None or c.start_date <= now) and (c.end_date is None or now <= c.end_date))
        codes = []
        for c in query_result:
            codes.append(c)
        return codes

    @staticmethod
    def Map_Request(code, form_data):
        """
        Maps request data to a permission code object.
        """
        code.name = form_data['name']
        code.code = form_data['code']
        code.description = form_data['description']
        code.contact_info = form_data['contact_info']
        try:
            code.start_date = datetime.datetime.fromisoformat(form_data['start_date'])
        except:
            code.start_date = None
        try:
            code.end_date = datetime.datetime.fromisoformat(form_data['end_date'])
        except:
            code.end_date = None

        if code.start_date and code.end_date and code.start_date > code.end_date:
            raise Exception

    @staticmethod
    @db_session
    def Add_From_Request(form_data):
        """
        Maps request data to a permission code object.
        """
        name = form_data['name']
        code = form_data['code']
        description = form_data['description']
        contact_info = form_data['contact_info']
        try:
            start_date = datetime.datetime.fromisoformat(form_data['start_date'])
        except:
            start_date = None
        try:
            end_date = datetime.datetime.fromisoformat(form_data['end_date'])
        except:
            end_date = None

        if start_date and end_date and start_date > end_date:
            raise Exception

        PermissionCode(name=name, code=code, description=description, contact_info=contact_info, start_date=start_date, end_date=end_date)

    @staticmethod
    @db_session
    def Validate_Permission_Code(code):
        """
        Checks if a given permission code is valid.
        """
        if code == 'INVALID':  # ID 1 is always invalid.
            return PermissionCodeStates.INVALID
        all_codes = PermissionCode.Get_All()
        today = datetime.date.today()
        for c in all_codes:
            if code == c.code:
                if (c.start_date is None or c.start_date <= today) and (c.end_date is None or today <= c.end_date):
                    return PermissionCodeStates.VALID
                elif c.start_date > today:
                    return PermissionCodeStates.NOT_YET_ACTIVE
                elif c.end_date < today:
                    return PermissionCodeStates.EXPIRED
        return PermissionCodeStates.INVALID

    @staticmethod
    @db_session
    def Use_Validation_Module(module, code):
        # Uses system-specific validators to check a code. Still returns VALID and INVALID states, could be used on its own
        # in possible architectures
        print("Attempting to validate the code %s"%code)
        if module.is_valid(code):
            return PermissionCodeStates.VALID
        else:
            # Must return VALIDATOR_FAIL not INVALID; INVALID only appears when code is not in internal list
            return PermissionCodeStates.VALIDATOR_FAIL

    @staticmethod
    def Serialize_Codes_For_Permission_Code_Menu(codes):
        result = []
        for c in codes:
            if c.id != 1:
                result.append(c.To_Dict_For_Permission_Code_Menu())
        return json.dumps(result)
    def To_Dict_For_Permission_Code_Menu(self):
        result = {
            'id': self.id,
            'name': self.name
        }
        return result

