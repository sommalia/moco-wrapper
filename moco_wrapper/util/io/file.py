from base64 import b64encode
from os.path import basename


class File(object):
    """
    Helper class for handling files
    """

    def __init__(self, file_path, file_name=None):
        """
        Class Constructor

        :param file_path: Path to the file on disk
        :param file_name: Name of the file (default ``None``)

        :type file_path: str
        :type file_name: str

        .. node::
            When not supplying a ``file_name``, the basename of the file will be used
        """
        self.path = file_path
        self.name = file_name

        # if no name was set for the file, use the basename
        if file_name is None:
            with open(self.path, "r") as f:
                self.name = basename(f.name)

    def to_base64(self):
        """
        Converts the content of the file to its base64 representation.

        :returns: File content as base64
        :rtype: str
        """
        with open(self.path, "rb") as f:
            return b64encode(f.read()).decode("utf-8")

    @classmethod
    def load(cls, path):
        """
        Helper method to create a :class:`.File` object from a path.

        :returns: :class:`.PurchaseFile` object
        :rtype: :class:`.PurchaseFile`
        """
        return cls(path)
