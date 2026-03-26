# Copyright (c) 2026, navanithi and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ServiceInvoice(Document):
	pass

import frappe

def has_permission(doc, user=None):
    if not user:
        user = frappe.session.user

    
    if "QF Manager" in frappe.get_roles(user):
        return True

    
    if not doc.job_card:
        return False

    
    payment_status = frappe.db.get_value(
        "Job Card",
        doc.job_card,
        "payment_status"
    )

    if payment_status == "Paid":
        return True

    return False