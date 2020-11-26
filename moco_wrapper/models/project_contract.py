from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH


class ProjectContract(MWRAPBase):
    """
    Class for handling project contracts.

    When a user gets assigned to a project, that is called a project contract. This can be done with this model.
    """

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def create(
        self,
        project_id: int,
        user_id: int,
        billable: bool = None,
        active: bool = None,
        budget: float = None,
        hourly_rate: float = None
    ):
        """
        Assign a user to a project.

        :param project_id: Id of the project
        :param user_id: User id of the person to assign
        :param billable: If the contract is billable (default ``None``)
        :param active: If the contract is active (default ``None``)
        :param budget: Contract budget (default ``None``)
        :param hourly_rate: Contract hourly rate (default ``None``)

        :type project_id: int
        :type user_id: int
        :type billable: bool
        :type active: bool
        :type budget: float
        :type hourly_rate: float

        :returns: Created contract object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        data = {
            "user_id": user_id
        }

        for key, value in (
            ("billable", billable),
            ("active", active),
            ("budget", budget),
            ("hourly_rate", hourly_rate)
        ):
            if value is not None:
                data[key] = value

        return self._moco.post(API_PATH["project_contract_create"].format(project_id=project_id), data=data)

    def update(
        self,
        project_id: int,
        contract_id: int,
        billable: bool = None,
        active: bool = None,
        budget: float = None,
        hourly_rate: float = None
    ):
        """
        Update an existing project contract.

        :param project_id: Id of the project to update the contract for
        :param contract_id: Id of the contract to update
        :param billable: If the contract is billable (default ``None``)
        :param active: If the contract is active (default ``None``)
        :param budget: Contract budget (default ``None``)
        :param hourly_rate: Contract hourly rate (default ``None``)

        :type project_id: int
        :type contract_id: int
        :type billable: bool
        :type active: bool
        :type budget: float
        :type hourly_rate: float

        :returns: The updated project contract
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """

        data = {}
        for key, value in (
            ("billable", billable),
            ("active", active),
            ("budget", budget),
            ("hourly_rate", hourly_rate)
        ):
            if value is not None:
                data[key] = value

        return self._moco.put(
            API_PATH["project_contract_update"].format(project_id=project_id, contract_id=contract_id), data=data)

    def get(
        self,
        project_id: int,
        contract_id: int
    ):
        """
        Retrieve a project contract.

        :param project_id: Id of the project
        :param contract_id: Id of the contract

        :type project_id: int
        :type contract_id: int

        :returns: The contract object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """

        return self._moco.get(API_PATH["project_contract_get"].format(project_id=project_id, contract_id=contract_id))

    def getlist(
        self,
        project_id: int,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Retrieve all active contracts for a project.

        :param project_id: Id of the project
        :param sort_by: Sort by field (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type project_id: int
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of contract objects
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`
        """

        params = {}

        for key, value in (
            ("page", page),
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["project_contract_getlist"].format(project_id=project_id), params=params)

    def delete(
        self,
        project_id: int,
        contract_id: int,
    ):
        """
        Delete a project contract.

        Deleting a staff assignment is only possible as long as there no hours tracked from the assigned person for
        the project.

        :param project_id: Id of the project
        :param contract_id: Id of the contract to delete

        :type project_id: int
        :type contract_id: int

        :returns: Empty response on success
        :rtype: :class:`moco_wrapper.util.response.EmptyResponse`
        """

        return self._moco.delete(
            API_PATH["project_contract_delete"].format(project_id=project_id, contract_id=contract_id))
