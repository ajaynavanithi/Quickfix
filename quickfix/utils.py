import frappe


def send_urgent_alert(job_card, manager):
    doc = frappe.get_doc("Job Card", job_card)

    if not manager:
        frappe.throw("Manager email is not configured in Quickfix Settings.")

    frappe.sendmail(
        recipients=[manager],
        subject=f"Urgent Job Card Requires Assignment: {doc.name}",
        message=f"""
Hello,

An urgent job card has been created without an assigned technician.

Job Card: {doc.name}
Customer: {doc.customer_name}
Device: {doc.device_type} {doc.device_model or ""}
Priority: {doc.priority}

Please assign a technician as soon as possible.
"""
    )
