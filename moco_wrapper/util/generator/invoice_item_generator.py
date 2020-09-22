from .base import BaseGenerator


class InvoiceItemGenerator(BaseGenerator):
    def generate_item(
        self,
        title: str,
        quantity: float = None,
        unit: str = None,
        unit_price: float = None,
        net_total: float = None,
        activity_ids: list = None,
        expense_ids: list = None
    ) -> dict:
        """
        Generate an invoice item.

        :param title: Title of the item
        :param quantity: Quantity of the supplied item
        :param unit: Unit name of the supplied item
        :param unit_price: Unit price of the supplied item
        :param net_total: Net total sum (either this is supplied or unit, unit_price, and quantity)
        :param activity_ids: Ids of the activities billed by this item
        :param expense_ids: Ids of the expenses billed by this item

        :type title: str
        :type quantity: float
        :type unit: str
        :type unit_price: float
        :type net_total: float
        :type activity_ids: list
        :type expense_ids: list

        :returns: The generated item

        This is the base function for generating positions in an invoice. There are two types of positions. Postions that can be itemized (see  :meth:`.generate_detail_postion`) and positions that do not have to be itemized ( :meth:`.generate_lump_position`).

        .. seealso::

            :meth:`.generate_detail_postion` and :meth:`.generate_lump_position`

        """
        data = {
            "type": "item",
            "title": title
        }

        for key, value in (
            ("quantity", quantity),
            ("unit", unit),
            ("unit_price", unit_price),
            ("net_total", net_total),
            ("activity_ids", activity_ids),
            ("expense_ids", expense_ids)
        ):
            if value is not None:
                data[key] = value

        return data

    def generate_detail_position(
        self,
        title: str,
        quantity: float,
        unit: str,
        unit_price: float,
        activity_ids: list = None,
        expense_ids: list = None
    ) -> dict:
        """
        Generates a detailed position item to be used in an offer items list (for example hours are a perfect example that can be split into units (a single hours set the unit, unit_price, and quantity)).

        :param title: Title of the position item
        :param quantity: How many of the things (i.e. how many hours)
        :param unit: What is the thing (i.e. hours)
        :param unit_price: Price of a single thing (i.e. price of a single hour)
        :param activity_ids: Ids of the activities billed by this item
        :param expense_ids: Ids of the expenses billed by this item

        :type title: str
        :type quantity: float
        :type unit: str
        :type unit_price: float
        :type activity_ids: list
        :type expense_ids: list

        :returns: The generated item

        .. seealso::

            :meth:`.generate_item`
        """
        return self.generate_item(title, quantity=quantity, unit=unit, unit_price=unit_price, activity_ids=activity_ids, expense_ids=expense_ids)

    def generate_lump_position(
        self,
        title: str,
        net_total: float
    ) -> dict:
        """
        Generates a general position item to be used in a offer list (use this if the postion cannot (or do not want) to split the position into units).

        :param title: Title of the position
        :param net_total: Total price of the postion

        :type title: str
        :type net_total: float

        :returns: The generated item

        .. seealso::

            :meth:`.generate_item`
        """

        return self.generate_item(title, net_total=net_total)

    def generate_title(
        self,
        title: str
    ) -> dict:
        """
        Generate an item of type ``title``

        :param title: Title the item should have

        :type title: str

        :returns: The generated item

        """
        return {
            "type": "title",
            "title": title
        }

    def generate_description(
        self,
        description: str
    ) -> dict:
        """
        Generate an item of type ``description``

        :param description: Description the item should have

        :type description: str

        :returns: The generated item
        """
        return {
            "type": "description",
            "description": description
        }

    def generate_pagebreak(self) -> dict:
        """
        Generate an item of type ``page-break``

        :returns: The generated item
        """
        return {
            "type": "page-break"
        }

    def generate_subtotal(
        self,
        title: str
    ) -> dict:
        """
        Generate an item of type ``subtotal``

        :param title: The title of the subtotal

        :type title: str

        :returns: The generated item
        """
        return {
            "title": title,
            "type": "subtotal"
        }

    def generate_separator(
        self,
    ) -> dict:
        """
        Generate an item of type ``separator``

        :returns: The generated item
        """
        return {
            "type": "separator"
        }
