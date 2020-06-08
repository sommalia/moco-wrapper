from .base import BaseGenerator


class PurchaseItemGenerator(BaseGenerator):
    """
    Class for generating items for purchase creation
    """

    def generate_item(
        self,
        title: str,
        total: float,
        tax: float,
        tax_included: bool = None
    ) -> dict:
        """
        Generates a single item

        :param title: Title of the item
        :param total: Item total
        :param tax: Tax percentage
        :param tax_included: Specify if the total included the tax or not (default ``None``)

        :type title: str
        :type total: float
        :type tax: float
        :type tax_included: bool

        :returns: Dictionary the be used in the items parameter of :meth:`moco_wrapper.models.Purchase.create`
        """
        item = {
            "title": title,
            "total": total,
            "tax": tax,
        }

        for key, value in (
            ("tax_included", tax_included),
        ):
            if value is not None:
                item[key] = value

        return item
