from .base import BaseGenerator


class OfferItemGenerator(BaseGenerator):
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

    def generate_item(
        self,
        title: str,
        quantity: float = None,
        unit: str = None,
        unit_price: float = None,
        net_total: float = None,
        optional=False
    ) -> dict:
        """
        Generate an offer item

        :param title: Title of the item
        :param quantity: Quantity of the supplied item
        :param unit: Unit name of the supplied item
        :param unit_price: Unit price of the supplied item
        :param net_total: Net total sum (either this is supplied or unit, unit_price, and quantity)
        :param optional: Whether the item is an optional item or not (default False)

        :type title: str
        :type quantity: float
        :type unit: str
        :type unit_price: float
        :type net_total: float
        :type optional: bool

        :returns: The generated item

        This is the base function for generating positions in an offer. There are two types of positions. Postions that can be itemized (see  :meth:`.generate_detail_postion`) and positions that do not have to be itemized ( :meth:`.generate_lump_position`).

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
            ("optional", optional)
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
        optional: bool = False
    ) -> dict:
        """
        Generates a detailed position item to be used in an offer items list (for example work hours are a perfect example that can be split into units (a single hours set the unit, unit_price, and quantity))

        :param title: Title of the position item
        :param quantity: How many of the things (i.e. how many hours)
        :param unit: What is the thing (i.e. hours)
        :param unit_price: Price of a single thing (i.e. price of a single hour)
        :param optional: If the position is optional or not (default False)

        :type title: str
        :type quantity: float
        :type unit: str
        :type unit_price: float
        :type optional: bool

        :returns: The generated item

        .. seealso::

            :meth:`.generate_item`
        """
        return self.generate_item(title, quantity=quantity, unit=unit, unit_price=unit_price, optional=optional)

    def generate_lump_position(
        self,
        title: str,
        net_total: float,
        optional: bool = False
    ) -> dict:
        """
        Generates a general position item to be used in a offer list (use this if the postion cannot (or do not want) to split the position into units)

        :param title: Title of the position
        :param net_total: Total price of the postion
        :param optional: If the position is optional or not (default False)

        :type title: str
        :type net_total: float
        :type optional: bool

        :returns: The generated item

        .. seealso::

            :meth:`.generate_item`
        """

        return self.generate_item(title, net_total=net_total, optional=optional)
