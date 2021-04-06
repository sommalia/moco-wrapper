class AccountInternalHourlyRateItemGenerator(object):

    def generate(
        self,
        user_id: int,
        rate: float
    ):
        """
        Generates an item than can be used to update an internal rate

        :param user_id: User id to apply the rate
        :param rate: Rate to apply

        :type user_id: int
        :type rate: float

        :returns: Item to update the interal rates of a user
        :rtype: dict
        """
        return {
            "user_id": user_id,
            "rate": rate
        }
