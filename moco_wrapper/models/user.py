import datetime

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH


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
        :param active: If the user should be activated or not (default ``None``)
        :param external: If the user is an employee or an external employee
            (his user id will now show up in reports etc.) (default ``None``)
        :param language: de, de-AT, de-CH, en, it or fr (default ``None``)
        :param mobile_phone: Mobile phone number (default ``None``)
        :param work_phone: Work phone number (default ``None``)
        :param home_address: Physical home address (default ``None``)
        :param birthday: Birthday date (default ``None``)
        :param custom_properties: Custom fields to add to the user (default ``None``)
        :param info: Additional information about the user (default ``None``)

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
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """

        data = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
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
        user_id,
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

        :param user_id: the Id of the user
        :param firstname: First name of the user (default ``None``)
        :param lastname: Last name of the user (default ``None``)
        :param email: Email address (default ``None``)
        :param password: Password to use when creating the user (default ``None``)
        :param unit_id: Id of the unit/team the user belongs to (default ``None``)
        :param active: If the user should be activated or not (default ``None``)
        :param external: If the user is an employee or an external employee
            (his user id will now show up in reports etc.) (default ``None``)
        :param language: de, de-AT, de-CH, en, it or fr (default ``None``)
        :param mobile_phone: Mobile phone number (default ``None``)
        :param work_phone: Work phone number (default ``None``)
        :param home_address: Physical home address (default ``None``)
        :param birthday: Birthday date (default ``None``)
        :param custom_properties: Custom fields to add to the user (default ``None``)
        :param info: Additional information about the user (default ``None``)

        :type user_id: int
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
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
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

        return self._moco.put(API_PATH["user_update"].format(id=user_id), data=data)

    def delete(
        self,
        user_id: int
    ):
        """
        Deletes an existing user.

        :param user_id: Id of the user to delete

        :type user_id: int

        :returns: Empty response on success
        :rtype: :class:`moco_wrapper.util.response.EmptyResponse`
        """

        return self._moco.delete(API_PATH["user_delete"].format(id=user_id))

    def get(
        self,
        user_id: int
    ):
        """
        Get a single user.

        :param user_id: Id of the user

        :type user_id: int

        :returns: Single user object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        return self._moco.get(API_PATH["user_get"].format(id=user_id))

    def getlist(
        self,
        include_archived: bool = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Get a list of users.

        :param include_archived: Include archived users in the list (default ``None``)
        :param sort_by: Sort by key (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type include_archived: bool
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of users
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`
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
