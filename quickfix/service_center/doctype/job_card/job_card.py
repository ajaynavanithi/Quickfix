import frappe
from frappe.model.document import Document

class JobCard(Document):
    def validate(self):
        if self.labour_charge in (None, ""):
            self.labour_charge = frappe.db.get_single_value(
                "Quickfix Settings", "default_labour_charge"
            ) or 0

        if self.customer_phone:
            if not self.customer_phone.isdigit() or len(self.customer_phone) != 10:
                frappe.throw("Customer Phone must be exactly 10 digits")

        if self.status in ["In Repair", "Ready for Delivery", "Delivered"]:
            if not self.assigned_technician:
                frappe.throw("Assigned Technician is required when status is In Repair or beyond.")

        parts_total = 0
        for row in self.part_usage_entry:
            row.total_price = (row.quantity or 0) * (row.unit_price or 0)
            parts_total += row.total_price

        self.parts_total = parts_total

        if not self.labour_charge:
            self.labour_charge = frappe.db.get_single_value(
                "QuickFix Settings",
                "default_labour_charge"
            ) or 0

        self.final_amount = (self.parts_total or 0) + (self.labour_charge or 0)

    def before_submit(self):

        if self.status != "Ready for Delivery":
            frappe.throw("Job Card can only be submitted when status is 'Ready for Delivery'.")

        for row in self.part_usage_entry:
            stock_qty = frappe.db.get_value("Spare Part", row.part, "stock_qty") or 0

            if stock_qty < (row.quantity or 0):
                frappe.throw(
                    f"Insufficient stock for Part: {row.part}. "
                    f"Available: {stock_qty}, Required: {row.quantity}"
                )


    def on_submit(self):
        for row in self.part_usage_entry:
            stock_qty = frappe.db.get_value("Spare Part", row.part, "stock_qty") or 0

            new_qty = stock_qty - (row.quantity or 0)

            frappe.db.set_value(
                "Spare Part",
                row.part,
                "stock_qty",
                new_qty
            )

        invoice = frappe.get_doc({
            "doctype": "Service Invoice",
            "job_card": self.name,
            "customer_name": self.customer_name,
            "invoice_date": frappe.utils.today(),
            "labour_charge": self.labour_charge,
            "parts_total": self.parts_total,
            "total_amount": self.final_amount,
            "payment_status": "Unpaid"
        })
        invoice.flags.ignore_permissions = True
        invoice.insert()
        invoice.submit()

        frappe.publish_realtime(
            "job_ready",
            {
                "job_card": self.name,
                "message": "Job is ready for delivery"
            },
            user=self.owner
        )

        frappe.enqueue(
            "quickfix.api.send_job_ready_email",
            job_card=self.name
        )

    def on_cancel(self):

        
        self.db_set("status", "Cancelled")

        
            for row in self.part_usage_entry:
                stock_qty = frappe.db.get_value(
                    "Spare Part",
                    row.part,
                    "stock_qty"
                ) or 0

                frappe.db.set_value(
                    "Spare Part",
                    row.part,
                    "stock_qty",
                    stock_qty + (row.quantity or 0)
                )

        
        invoice_name = frappe.db.get_value(
            "Service Invoice",
            {"job_card": self.name},
            "name"
        )

        if invoice_name:
            invoice_doc = frappe.get_doc("Service Invoice", invoice_name)

            if invoice_doc.docstatus == 1:
                invoice_doc.cancel()

    def on_trash(self):

        if self.status not in ["Cancelled", "Draft"]:
            frappe.throw(
                "You can only delete Job Cards that are in Draft or Cancelled status."
            )

    

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
