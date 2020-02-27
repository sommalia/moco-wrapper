import datetime

class MWRAPBase(object):
    """
    Base class for all models in MocoWrapper.
    """

    def convert_date_to_iso(self, date_to_convert: datetime.date):
        """
        converts a datetime object to iso format need by the api
        
        :param date_to_convert: date object to convert
        :returns: date in iso format (YYYY-MM-DD)
        """
        return datetime.date(
            date_to_convert.year,
            date_to_convert.month,
            date_to_convert.day
        ).isoformat()