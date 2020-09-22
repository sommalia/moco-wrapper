from moco_wrapper.util.generator import InvoiceItemGenerator

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
        activity_ids = [123, 456]
        expense_ids = [4, 999]

        item = self.generator.generate_item(
            title, 
            quantity=quantity, 
            unit=unit, 
            unit_price=unit_price, 
            net_total=net_total,
            activity_ids=activity_ids,
            expense_ids=expense_ids
        )

        assert item["title"] == title
        assert item["unit"] == unit
        assert item["unit_price"] == unit_price
        assert item["quantity"] == quantity
        assert item["net_total"] == net_total
        assert item["activity_ids"] == activity_ids
        assert item["expense_ids"] == expense_ids

    def test_generate_separator(self):
        item = self.generator.generate_separator()

        assert item["type"] == "separator"

    def test_generate_separator(self):
        item = self.generator.generate_separator()

        assert item["type"] == "separator"

    def test_generate_subtotal(self):
        title = "zwischensumme"
        item = self.generator.generate_subtotal(title)

        assert item["type"] == "subtotal"
        assert item["title"] == title

    def test_generate_pagebreak(self):
        item = self.generator.generate_pagebreak()

        assert item["type"] == "page-break"
