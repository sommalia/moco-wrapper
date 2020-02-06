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
        
    def generate_seperator(
        self,
        ):
        """generate an invoice item of type "seperator"

        :returns: the item
        """
        return {
            "type": "seperator"
        }

class OfferItemGenerator(ItemGenerator):
    def generate_item(
        self,
        title,
        quantity = None,
        unit = None,
        unit_price = None,
        net_total = None,
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

class InvoiceItemGenerator(ItemGenerator):
    def generate_item(
        self,
        title,
        quantity = None,
        unit = None,
        unit_price = None,
        net_total = None
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