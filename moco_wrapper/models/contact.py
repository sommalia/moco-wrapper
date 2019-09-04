from .base import MocoBase

class Contact(MocoBase):
    """Class for handling contacts"""

    def __init__(self, moco):
        """Initialize a contact instance
        
        :param moco: An instance of :class Moco

        """

        self._moco = moco

    def create(
        self,
        firstname,
        lastname,
        gender,
        customer_id = None,
        title = None,
        mobile_phone = None,
        work_fax = None,
        work_phone = None,
        work_email = None,
        work_address = None,
        home_address = None,
        birthday = None,
        info = None,
        tags = None):
        """Create a single contact.

        :param firstname: The first name of the contact
        :param lastname: The last name of the contact
        :param gender: either F, M, U
        :param customer_id: Id of the customer the contact belongs to
        :param title: Title the contact has
        :param mobile_phone: Mobile phone number the contact has
        :param work_fax: Fax number for work purposes
        :param work_phone: Phone number for work purposes
        :param work_email: Work email address
        :param work_address: Work address
        :param home_address: Home address
        :param birthday: Birthday (format YYYY-MM-DD)
        :param info: More information about the contact
        :param tags: Array of additional tags 

        """
        data = {
            "firstname" : firstname,
            "lastname" : lastname,
            "gender" : gender
        }

        for key, value in (
            ("customer_id", customer_id),
            ("title", title),
            ("mobile_phone", mobile_phone),
            ("work_fax", work_fax),
            ("work_phone", work_phone),
            ("work_email", work_email),
            ("work_address", work_address),
            ("home_address", home_address),
            ("birthday", birthday),
            ("info", info),
            ("tags", tags)
        ):
            if value is not None:
                data[key] = value

        return self._moco.post("/contacts/people", data=data);

