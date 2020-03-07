import datetime

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH

from enum import Enum

class User(MWRAPBase):
    """
    Class for handling users.    
    """

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def create(
        self,
        firstname: str,
        lastname: str,
        email: str,
        password: str,
        unit_id: int,
        active: bool = None,
        external: bool = None,
        language: str = None,
        mobile_phone: str = None,
        work_phone: str = None,
        home_address: str = None,
        birthday: datetime.date = None,
        custom_properties: dict = None,
        info: str = None,
        ):
        """
        Creates a new user.

        :param firstname: First name of the user
        :param lastname: Last name of the user
        :param email: Email address
        :param password: Password to use when creating the user
        :param unit_id: Id of the unit/team the user belongs to
        :param active: If the user should be activated or not
        :param external: If the user is an employee or an external employee (his user id will now show up in reports etc.)
        :param language: de, de-AT, de-CH, en, it or fr
        :param mobile_phone: Mobile phone number
        :param work_phone: Work phone number
        :param home_address: Phyical home address 
        :param birthday: Birthday date
        :param custom_properties: Custom fields to add to the user
        :param info: Additional information about the user

        :type firstname: str
        :type lastname: str
        :type email: str
        :type password: str
        :type unit_id: int
        :type active: bool
        :type external: bool
        :type language: str
        :type mobile_phone: str
        :type work_phone: str
        :type home_address: str
        :type birthday: datetime.date, str
        :type custom_properties: dict
        :type info: str

        :returns: The created user object
        """

        
        data = {
            "firstname" : firstname,
            "lastname": lastname,
            "email" : email,
            "password": password,
            "unit_id": unit_id
        }

        for key, value in (
            ("active", active),
            ("external", external),
            ("language", language),
            ("mobile_phone", mobile_phone),
            ("work_phone", work_phone),
            ("home_address", home_address),
            ("bday", birthday),
            ("custom_properties", custom_properties),
            ("info", info)
        ):
            if value is not None:
                    
                if key in ["bday"] and isinstance(value, datetime.date):
                    data[key] = self._convert_date_to_iso(value)
                else:
                    data[key] = value

        return self._moco.post(API_PATH["user_create"], data=data)

    def update(
        self,
        id,
        firstname: str = None,
        lastname: str = None,
        email: str = None,
        password: str = None,
        unit_id: int = None,
        active: bool = None,
        external: bool = None,
        language: str = None,
        mobile_phone: str = None,
        work_phone: str = None,
        home_address: str = None,
        birthday: datetime.date = None,
        custom_properties: dict = None,
        info: str = None,
        ):
        """
        Updates an existing user.

        :param id: the Id of the user
        :param firstname: First name of the user
        :param lastname: Last name of the user
        :param email: Email address
        :param password: Password to use when creating the user
        :param unit_id: Id of the unit/team the user belongs to
        :param active: If the user should be activated or not
        :param external: If the user is an employee or an external employee (his user id will now show up in reports etc.)
        :param language: de, de-AT, de-CH, en, it or fr
        :param mobile_phone: Mobile phone number
        :param work_phone: Work phone number
        :param home_address: Physical home address 
        :param birthday: Birthday date
        :param custom_properties: Custom fields to add to the user
        :param info: Additional information abotu the user

        :type id: int
        :type firstname: str
        :type lastname: str
        :type email: str
        :type password: str
        :type unit_id: int
        :type active: bool
        :type external: bool
        :type language: str
        :type mobile_phone: str
        :type work_phone: str
        :type home_address: str
        :type birthday: datetime.date, str
        :type custom_properties: dict
        :type info: str

        :returns: The updated user object

        """
        data = {}
        for key, value in (
            ("firstname", firstname),
            ("lastname", lastname),
            ("email", email),
            ("password", password),
            ("unit_id", unit_id),
            ("active", active),
            ("external", external),
            ("language", language),
            ("mobile_phone", mobile_phone),
            ("work_phone", work_phone),
            ("home_address", home_address),
            ("bday", birthday),
            ("custom_properties", custom_properties),
            ("info", info)
        ):
            if value is not None:
                if key in ["bday"] and isinstance(value, datetime.date):
                    data[key] = self._convert_date_to_iso(value)
                else:
                    data[key] = value

        #check if length > 0 TODO
        return self._moco.put(API_PATH["user_update"].format(id=id), data=data)

    def delete(
        self,
        id: int
        ):
        """
        Deletes an existing user.

        :param id: Id of the user to delete

        :type id: int

        :returns: Empty response on success
        """

        return self._moco.delete(API_PATH["user_delete"].format(id=id))

    def get(
        self,
        id: int
        ):
        """
        Get a single user.

        :param id: Id of the user

        :type id: int

        :returns: Single user object
        """
        return self._moco.get(API_PATH["user_get"].format(id=id))

    def getlist(
        self,
        include_archived: bool = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
        ):
        """
        Get a list of users.

        :param include_archived: Include archived users in the list
        :param sort_by: Sort by key
        :param sort_order: asc or desc (default asc)
        :param page: Page number (default 1)

        :type include_archived: bool
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of users
        """
               
        params = {}
        for key, value in (
            ("include_archived", include_archived),
            ("page", page),
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["user_getlist"], params=params)