import frappe
from frappe.model.document import Document

class JobCard(Document):
    def validate(self):
        if self.labour_charge in (None, ""):
            self.labour_charge = frappe.db.get_single_value(
                "Quickfix Settings", "default_labour_charge"
            ) or 0
