from .base import MWRAPBase
from ..const import API_PATH

class User(MWRAPBase):
    """Class for handling users"""
    def __init__(self, moco):
        self._moco = moco

    def create(
        self,
        firstname,
        lastname,
        email,
        password,
        unit_id,
        active = None,
        external = None,
        language = None,
        mobile_phone = None,
        work_phone = None,
        home_address = None,
        bday = None,
        custom_properties = None,
        info = None,
        ):
        """Creates a new user

        :param firstname: the first name of the user
        :param lastname: the last name of the user
        :param email: user email
        :param password: the password to use when creating the user
        :param unit_it: id of the unit/team the user belongs to
        :param active: true/false if the user should be activated or not
        :param external: true/false if the user is an employee or an external contractor
        :param language: de, de-AT, de-CH, en, it or fr
        :param mobile_phone: users mobile phone number
        :param work_phone: users work phone number
        :param home_address: users home address 
        :param bday: users birthday (format YYYY-MM-DD)
        :param custom_properties: custom fields to add to the user
        :param info: additional information abotu the user
        :returns: the created user object

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
            ("bday", bday),
            ("custom_properties", custom_properties),
            ("info", info)
        ):
            if value is not None:
                data[key] = value

        return self._moco.post(API_PATH["user_create"], data=data)

    def update(
        self,
        id,
        firstname = None,
        lastname = None,
        email = None,
        password = None,
        unit_id = None,
        active = None,
        external = None,
        language = None,
        mobile_phone = None,
        work_phone = None,
        home_address = None,
        bday = None,
        custom_properties = None,
        info = None,
        ):
        """Updates an existing user

        :param id: the id of the user
        :param firstname: the first name of the user
        :param lastname: the last name of the user
        :param email: user email
        :param password: the password to use when creating the user
        :param unit_it: id of the unit/team the user belongs to
        :param active: true/false if the user should be activated or not
        :param external: true/false if the user is an employee or an external contractor
        :param language: de, de-AT, de-CH, en, it or fr
        :param mobile_phone: users mobile phone number
        :param work_phone: users work phone number
        :param home_address: users home address 
        :param bday: users birthday (format YYYY-MM-DD)
        :param custom_properties: custom fields to add to the user
        :param info: additional information abotu the user
        :returns: the created user object

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
            ("bday", bday),
            ("custom_properties", custom_properties),
            ("info", info)
        ):
            if value is not None:
                data[key] = value

        #check if length > 0 TODO
        return self._moco.put(API_PATH["user_update"].format(id=id), data=data)

    def delete(
        self,
        id
        ):
        """Deletes an existing user

        :param id: id of the user to delete
        """

        return self._moco.delete(API_PATH["user_delete"].format(id=id))

    def get(
        self,
        id
        ):
        """Get a single user

        :param id: user id
        :returns: user object
        """
        return self._moco.get(API_PATH["user_get"].format(id=id))

    def getlist(
        self,
        include_archived = None,
        sort_by = None,
        sort_order = 'asc',
        page = 1
        ):
        """Get a list of users

        :param include_archived: true/false include archived users in the list
        :param sort_by: sort by key
        :param sort_order: asc or desc (default asc)
        :param page: page number (default 1)
        :returns: list of users
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