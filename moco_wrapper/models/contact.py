import datetime
from typing import List

from moco_wrapper.util.endpoint import Endpoint
from moco_wrapper.models import objector_models as om
from moco_wrapper.models.base import MWRAPBase

from enum import Enum


class ContactGender(str, Enum):
    """
    Enumeration for allowed values that can be supplied for the ``gender`` argument in :class:`.Contact.create`
    and :class:`.Contact.update`.

    Example Usage:

    .. code-block:: python

        from moco_wrapper.models.contact import ContactGender
        from moco_wrapper import Moco

        m = Moco()
        new_contact = m.Contact.create(
            ..
            gender = ContactGender.MALE
        )
    """

    MALE = "M"
    FEMALE = "F"
    UNDEFINED = "U"


class Contact(MWRAPBase):
    """
    Class for handling contacts.
    """

    @staticmethod
    def endpoints() -> List[Endpoint]:
        """
        Returns all endpoints associated with the model

        :returns: List of Endpoint objects
        :rtype: :class:`moco_wrapper.util.endpoint.Endpoint`

        """
        return [
            Endpoint("contact_create", "/contacts/people", "POST", om.Contact),
            Endpoint("contact_update", "/contacts/people/{id}", "PUT", om.Contact),
            Endpoint("contact_getlist", "/contacts/people", "GET", om.Contact),
            Endpoint("contact_get", "/contacts/people/{id}", "GET", om.Contact)
        ]

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
        gender: ContactGender,
        company_id: int = None,
        title: str = None,
        job_position: str = None,
        mobile_phone: str = None,
        work_fax: str = None,
        work_phone: str = None,
        work_email: str = None,
        work_address: str = None,
        home_address: str = None,
        home_email: str = None,
        birthday: datetime.date = None,
        info: str = None,
        tags: list = None
    ):
        """
        Creates a contact.

        :param firstname: The first name of the contact
        :param lastname: The last name of the contact
        :param gender: Gender of the contact
        :param company_id: Id of the company the contact belongs to (default ``None``)
        :param title: Job title the contact has (default ``None``)
        :param job_position: Name of the job position this contact has (default ``None``)
        :param mobile_phone: Mobile phone number the contact has (default ``None``)
        :param work_fax: Work fax number (default ``None``)
        :param work_phone: Work phone number (default ``None``)
        :param work_email: Work email address (default ``None``)
        :param work_address: Physical work address (default ``None``)
        :param home_address: Physical home address (default ``None``)
        :param home_email: Home email address (default ``None``)
        :param birthday: Birthday date (default ``None``)
        :param info: More information about the contact (default ``None``)
        :param tags: Array of additional tags (default ``None``)

        :type firstname: str
        :type lastname: str
        :type gender: :class:`.ContactGender`, str
        :type company_id: int
        :type title: str
        :type job_position: str
        :type mobile_phone: str
        :type work_fax: str
        :type work_phone: str
        :type work_email: str
        :type work_address: str
        :type home_address: str
        :type home_email: str
        :type birthday: datetime.date, str
        :type info: str
        :type tags: list

        :returns: The created contact object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """

        data = {
            "firstname": firstname,
            "lastname": lastname,
            "gender": gender
        }

        for key, value in (
            ("company_id", company_id),
            ("title", title),
            ("job_position", job_position),
            ("mobile_phone", mobile_phone),
            ("work_fax", work_fax),
            ("work_phone", work_phone),
            ("work_email", work_email),
            ("work_address", work_address),
            ("home_address", home_address),
            ("home_email", home_email),
            ("birthday", birthday),
            ("info", info),
            ("tags", tags)
        ):
            if value is not None:
                if isinstance(value, datetime.date):
                    data[key] = value.isoformat()
                else:
                    data[key] = value

        return self._moco.post('contact_create', data=data)

    def update(
        self,
        contact_id: int,
        firstname: str = None,
        lastname: str = None,
        gender: ContactGender = None,
        company_id: int = None,
        title: str = None,
        job_position: str = None,
        mobile_phone: str = None,
        work_fax: str = None,
        work_phone: str = None,
        work_email: str = None,
        work_address: str = None,
        home_address: str = None,
        home_email: str = None,
        birthday: datetime.date = None,
        info: str = None,
        tags: list = None
    ):
        """
        Updates a contact.

        :param contact_id: Id of the contact
        :param firstname: The first name of the contact (default ``None``)
        :param lastname: The last name of the contact (default ``None``)
        :param gender: Gender of the contact (default ``None``)
        :param company_id: Id of the company the contact belongs to  (default ``None``)
        :param title: Job title the contact has (default ``None``)
        :param job_position: name of the job position this contact has (default ``None``)
        :param mobile_phone: Mobile phone number the contact has (default ``None``)
        :param work_fax: Work fax number (default ``None``)
        :param work_phone: Work phone number (default ``None``)
        :param work_email: Work email address (default ``None``)
        :param work_address: Physical work address (default ``None``)
        :param home_address: Physical home address (default ``None``)
        :param home_email: Home email address (default ``None``)
        :param birthday: Birthday date (default ``None``)
        :param info: More information about the contact (default ``None``)
        :param tags: Array of additional tags (default ``None``)

        :type contact_id: int
        :type firstname: str
        :type lastname: str
        :type gender: :class:`.ContactGender`, str
        :type company_id: int
        :type title: str
        :type job_position: str
        :type mobile_phone: str
        :type work_fax: str
        :type work_phone: str
        :type work_email: str
        :type work_address: str
        :type home_address: str
        :type home_email: str
        :type birthday: datetime.date, str
        :type info: str
        :type tags: list

        :returns: The updated contact object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """

        ep_params = {
            "id": contact_id
        }

        data = {}
        for key, value in (
            ("firstname", firstname),
            ("lastname", lastname),
            ("gender", gender),
            ("company_id", company_id),
            ("title", title),
            ("job_position", job_position),
            ("mobile_phone", mobile_phone),
            ("work_fax", work_fax),
            ("work_phone", work_phone),
            ("work_email", work_email),
            ("work_address", work_address),
            ("home_address", home_address),
            ("home_email", home_email),
            ("birthday", birthday),
            ("info", info),
            ("tags", tags)
        ):

            if value is not None:
                if key == "birthday" and isinstance(value, datetime.date):
                    data[key] = value.isoformat()
                else:
                    data[key] = value

        return self._moco.put("contact_update", ep_params=ep_params, data=data)

    def get(
        self,
        contact_id: int
    ):
        """
        Retrieve a single contact object

        :param contact_id: Id of the contact

        :type contact_id: int

        :returns: The contact object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        ep_params = {
            "id": contact_id
        }

        return self._moco.get("contact_get", ep_params=ep_params)

    def getlist(
        self,
        tags: list = None,
        term: str = None,
        phone: str = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Retrieve a list of contact objects

        :param tags: Array of tags (default ``None``)
        :param term: Full text search
            (fields that are searched are name, firstname, work_email and company) (default ``None``)
        :param phone: Reverse lookup for work_phone or mobile_phone (default ``None``)
        :param sort_by: Field to the results by (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type tags: list
        :type term: str
        :type phone: str
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of contact objects
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`
        """
        params = {}
        for key, value in (
            ("tags", tags),
            ("term", term),
            ("phone", phone),
            ("page", page)
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get("contact_getlist", params=params)
