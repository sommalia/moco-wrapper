from moco_wrapper.util.generator import PurchaseItemGenerator

class TestPurchaseItemGenerator(object):
    def setup(self):
        self.generator = PurchaseItemGenerator()

    def test_generate_item(self):
        title = "test title"
        tax = 7.7
        total = 20.3
        tax_included = False

        item = self.generator.generate_item(title, total, tax, tax_included=tax_included)

        assert item["title"] == title
        assert item["tax"] == tax
        assert item["total"] == total
        assert item["tax_included"] == tax_included
