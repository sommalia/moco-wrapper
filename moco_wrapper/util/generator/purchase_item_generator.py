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
        tax_included: bool = None,
        category_id: int = None
    ) -> dict:
        """
        Generates a single item

        :param title: Title of the item
        :param total: Item total
        :param tax: Tax percentage
        :param tax_included: Specify if the total included the tax or not (default ``None``)
        :param category_id: Reference to a purchase category

        :type title: str
        :type total: float
        :type tax: float
        :type tax_included: bool (default ``None``)
        :type category_id: int (default ``None``)

        :returns: Dictionary the be used in the items parameter of :meth:`moco_wrapper.models.Purchase.create`
        """
        item = {
            "title": title,
            "total": total,
            "tax": tax,
        }

        for key, value in (
            ("tax_included", tax_included),
            ("category_id", category_id)
        ):
            if value is not None:
                item[key] = value

        return item
