class Invoice(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class InvoiceEmail(object):
    def __init__(self, subject, text, emails_to, emails_cc, emails_bcc):
        self.subject = subject
        self.text = text

        self.emails_to = InvoiceEmail.to_email_list(emails_to)
        self.emails_cc = InvoiceEmail.to_email_list(emails_cc)
        self.emails_bcc = InvoiceEmail.to_email_list(emails_bcc)

    @staticmethod
    def to_email_list(value):
        """
        Formats the value for the emails_to, emails_cc and emails_bcc fields
        """

        if value is None:
            return []
        elif ";" in value:
            # value is a string that represents a list of emails
            return value.split(";")
        else:
            # value is a string without ;
            return [value]
