import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class SparePart(Document):

    def validate(self):
        if self.selling_price <= self.unit_cost:
            frappe.throw("Selling Price must be greater than Unit Cost")

    def autoname(self):
        if not self.part_code:
            frappe.throw("Part Code is required")

        self.part_code = self.part_code.upper()

        self.name = make_autoname("PART-.YYYY.-.####")



    def on_update(self):
        threshold = frappe.db.get_value(
            "Quickfix Settings",
            None,
            "low_stock_threshold"
        ) or self.reorder_level or 0

        if self.stock_qty < threshold:
            frappe.msgprint("Low stock alert!")
