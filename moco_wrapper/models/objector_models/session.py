class SessionAuthentication(object):
    def __init__(
        self,
        api_key,
        user_id
    ):
        self.api_key = api_key
        self.user_id = user_id


class SessionVerification(object):

    def __init__(
        self,
        id,
        uuid,
    ):
        self.id = id
        self.uuid = uuid
