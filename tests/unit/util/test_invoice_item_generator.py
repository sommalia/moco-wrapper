from moco_wrapper.util import InvoiceItemGenerator

class TestInvoiceItemGenerator(object):
    def setup(self):
        self.generator = InvoiceItemGenerator()

    def test_generate_title(self):
        title_text = "this is the content"

        item = self.generator.generate_title(title_text)

        assert item["title"] == title_text
        assert item["type"] == "title"

    def test_generate_description(self):
        description_text = "this is the content"

        item = self.generator.generate_description(description_text)

        assert item["description"] == description_text
        assert item["type"] == "description"

    def test_generate_item(self):
        title = "this is the title"
        unit = "this is the unit"
        unit_price = 55
        net_total = 44
        quantity = 3

        item = self.generator.generate_item(title, quantity=quantity, unit=unit, unit_price=unit_price, net_total=net_total)

        assert item["title"] == title
        assert item["unit"] == unit
        assert item["unit_price"] == unit_price
        assert item["quantity"] == quantity
        assert item["net_total"] == net_total

    def test_generate_seperator(self):
        item = self.generator.generate_seperator()

        assert item["type"] == "seperator"
