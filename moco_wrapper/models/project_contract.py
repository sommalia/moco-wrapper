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

        :param project: Id of the project
        :param user_id: User id of the person to assign
        :param billable: If the contract is billable
        :param active: If the contract is active
        :param budget: Contract budget
        :param hourly_rate: Contract hourly rate
        :returns: Created contract object
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
        billable: bool= None,
        active: bool = None,
        budget: float = None,
        hourly_rate: float = None
        ):
        """
        Update an existing project contract.

        :param project_id: Id of the project to update the contract for
        :param contract_id: Id of the contract to update
        :param billable: If the contract is billable
        :param active: If the contract is active
        :param budget: Contract budget
        :param hourly_rate: Contract hourly rate
        :returns: The updated project contract
        """

        data = {}
        for key,value in (
            ("billable", billable),
            ("active", active),
            ("budget", budget),
            ("hourly_rate", hourly_rate)
        ):
            if value is not None:
                data[key] = value

        return self._moco.put(API_PATH["project_contract_update"].format(project_id=project_id, contract_id=contract_id), data=data)

    def get(
        self,
        project_id: int,
        contract_id: int
        ):
        """
        Retrieve a project contract.

        :param project_id: Id of the project
        :param contract_id: Id of the contract
        :returns: The contract object
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
        :param sort_by: Sort by field
        :param sort_order: asc or desc (default asc)
        :param page: Page number (default 1)
        :returns: List of contract objects
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

        Deleting a staff assignment is only possible as long as there no hours tracked from the assinged person for the project.

        :param project_id: Id of the project
        :param contract_id: Id of the contract to delete
        :returns: Empty response on success
        """

        return self._moco.delete(API_PATH["project_contract_delete"].format(project_id=project_id, contract_id=contract_id))




