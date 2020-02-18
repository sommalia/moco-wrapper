class ItemGenerator(object):

    def generate_title(
        self,
        title
        ):
        """generate an invoice item of type "title"
        
        :param title: title the item should have
        :returns: the item

        """
        return {
            "type": "title",
            "title": title
        }

    def generate_description(
        self,
        description
        ):
        """generate an invoice item of type "description"

        :param description: description the item should have
        :returns: the item
        """
        return {
            "type" : "description",
            "description": description
        }

    def generate_pagebreak(self):
        return {
            "type": "page-break"
        }

    def generate_subtotal(self, title):
        return {
            "title": title,
            "type": "subtotal"    
        }

    def generate_separator(
        self,
        ):
        """generate an invoice item of type "separator"

        :returns: the item
        """
        return {
            "type": "separator"
        }
        


class OfferItemGenerator(ItemGenerator):
    def generate_item(
        self,
        title: str,
        quantity: float = None,
        unit: int = None ,
        unit_price: float= None,
        net_total: float = None,
        optional = False
        ):
        """generate an invoice if tyoe "item"

        :param title: title of the item
        :param quantity: quantity of the supplied item
        :param unit: unit name of the supplied item
        :param unit_price: unit price of the supplied item
        :param net_total: net total sum (either this is supplied or unit, unit_price, and quantity)
        :param optional: wehter the item is an optional item or not (default False)
        :returns: the item
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

    def generate_detail_postion(
        self,
        title: str,
        quantity: float,
        unit: str,
        unit_price: float,
        optional: bool = False
    ):
        """
        generates a detailed position item to be used in an offer items list (for example hours are a perfect example that can be split into units (a single hours set the unit, unit_price, and quantity))

        :param title: title of the position item
        :param quantity: how many of the things (i.e. how many hours)
        :param unit: what is the thing (i.e. hours)
        :param unit_price: price of a single thing (i.e. price of a single hour)
        :param optional: if the position is optional or not (default False)
        """
        return self.generate_item(title, quantity=quantity, unit=unit, unit_price=unit_price, optional=optional)

    def generate_lump_position(
        self,
        title: str,
        net_total: float,
        optional: bool = False
    ):
        """
        generates a general position item to be used in a offer list (use this if the postion cannot (or do not want) to split the position into units)

        :param title: title of the position
        :param net_total: total price of the postion
        :param optional: if the position is optional or not (default False)
        """

        return self.generate_item(title, net_total=net_total, optional=optional)


class InvoiceItemGenerator(ItemGenerator):
    def generate_item(
        self,
        title: str,
        quantity: float = None,
        unit: str = None,
        unit_price: float = None,
        net_total: float = None
        ):
        """generate an invoice if tyoe "item"

        :param title: title of the item
        :param quantity: quantity of the supplied item
        :param unit: unit name of the supplied item
        :param unit_price: unit price of the supplied item
        :param net_total: net total sum (either this is supplied or unit, unit_price, and quantity)
        :returns: the item
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
        ):
            if value is not None:
                data[key] = value

        return data

    def generate_detail_postion(
        self,
        title: str,
        quantity: float,
        unit: str,
        unit_price: float
    ):
        """
        generates a detailed position item to be used in an offer items list (for example hours are a perfect example that can be split into units (a single hours set the unit, unit_price, and quantity))

        :param title: title of the position item
        :param quantity: how many of the things (i.e. how many hours)
        :param unit: what is the thing (i.e. hours)
        :param unit_price: price of a single thing (i.e. price of a single hour)
        :param optional: if the position is optional or not (default False)
        """
        return self.generate_item(title, quantity=quantity, unit=unit, unit_price=unit_price)

    def generate_lump_position(
        self,
        title: str,
        net_total: float
    ):
        """
        generates a general position item to be used in a offer list (use this if the postion cannot (or do not want) to split the position into units)

        :param title: title of the position
        :param net_total: total price of the postion
        :param optional: if the position is optional or not (default False)
        """

        return self.generate_item(title, net_total=net_total)



