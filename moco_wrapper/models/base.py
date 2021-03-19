import datetime
from moco_wrapper.util.endpoint import Endpoint


class MWRAPBase(object):
    """
    Base class all other model classes inherit
    """

    def _convert_date_to_iso(self, date_to_convert: datetime.date):
        """
        Converts a datetime object to iso format need by the api

        :param date_to_convert: datetime.date object to convert

        :type date_to_convert: datetime.date

        :returns: Date in iso format (YYYY-MM-DD)
        :rtype: str
        """
        return datetime.date(
            date_to_convert.year,
            date_to_convert.month,
            date_to_convert.day
        ).isoformat()

    @staticmethod
    def endpoints() -> [Endpoint]:
        """
        Returns all models associated with the model

        :returns: List of endpoint objects
        :rtype: list
        """
        return []
