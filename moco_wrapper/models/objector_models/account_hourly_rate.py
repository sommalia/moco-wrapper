class SingleRate(object):
    def __init__(self, currency, hourly_rate):
        self.currency = currency
        self.hourly_rate = hourly_rate

    def __str__(self):
        return "SingleRate(currency={0}, hourly_rate={1})".format(self.currency, self.hourly_rate)


class TaskRate(object):
    def __init__(self, id, name, raw_rates):
        self.id = id
        self.name = name

        self.rates = []
        for raw_rate in raw_rates:
            sr = SingleRate(**raw_rate)
            self.rates.append(sr)

    def __str__(self):
        return "TaskRate(id={0}, name={1}, rates=[ {2} ])".format(
            self.id,
            self.name,
            ", ".join([str(x) for x in self.rates])
        )


class UserRate(object):
    def __init__(self, id, full_name, raw_rates):
        self.id = id
        self.full_name = full_name

        self.rates = []
        for raw_rate in raw_rates:
            sr = SingleRate(**raw_rate)
            self.rates.append(sr)

    def __str__(self):
        return "UserRate(id={0}, full_name={1}, rates=[{2}])".format(
            self.id,
            self.full_name,
            ", ".join([str(x) for x in self.rates])
        )


class AccountHourlyRate(object):
    def __init__(self, **kwargs):
        nk = kwargs

        if "tasks" in kwargs.keys() and kwargs["tasks"] is not None:
            task_rates = []

            for task_rate in kwargs["tasks"]:
                obj = TaskRate(
                    id=task_rate["id"],
                    name=task_rate["name"],
                    raw_rates=task_rate["rates"]
                )
                task_rates.append(obj)

            nk["tasks"] = task_rates

        if "users" in kwargs.keys() and kwargs["users"] is not None:
            user_rates = []

            for user_rate in kwargs["users"]:
                obj = UserRate(
                    id=user_rate["id"],
                    full_name=user_rate["full_name"],
                    raw_rates=task_rate["rates"]
                )
                user_rates.append(obj)

            nk["users"] = user_rates

        if "defaults_rates" in kwargs.keys() and kwargs["defaults_rates"] is not None:
            default_rates = []

            for default_rate in kwargs["defaults_rates"]:
                obj = SingleRate(**default_rate)
                default_rates.append(obj)

            nk["defaults_rates"] = default_rates

        self.__dict__.update(nk)
