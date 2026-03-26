import frappe
from frappe.model.document import Document

class JobCard(Document):
    def validate(self):
        if self.labour_charge in (None, ""):
            self.labour_charge = frappe.db.get_single_value(
                "Quickfix Settings", "default_labour_charge"
            ) or 0

def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user


    if user == "Administrator":
        return None

    if "QF Technician" in frappe.get_roles(user):
        return f"""
    `tabJob Card`.assigned_technician IN (
        SELECT name FROM `tabTechnician`
        WHERE user = '{user}'
    )
"""

    return None