import frappe
from frappe import ValidationError

def before_uninstall():
    """Prevent uninstall if submitted Job Cards exist"""

    # Check for submitted Job Cards (docstatus = 1)
    if frappe.db.exists("Job Card", {"docstatus": 1}):
        raise ValidationError(
            "Cannot uninstall QuickFix: Submitted Job Cards exist. "
            "Please cancel or delete them before uninstalling."
        )