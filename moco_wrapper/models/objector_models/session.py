class SessionAuthentication(object):
    def __init__(
        self,
        api_key,
        user_id
    ):
        self.api_key = api_key
        self.user_id = user_id

    def __str__(self):
        return "SessionAuthentication(api_key={0}, user_id={1})".format(
            self.api_key,
            self.user_id
        )


class SessionVerification(object):

    def __init__(
        self,
        id,
        uuid,
    ):
        self.id = id
        self.uuid = uuid

    def __str__(self):
        return "SessionVerification(id={0}, uuid={1})".format(
            self.id,
            self.uuid
        )
