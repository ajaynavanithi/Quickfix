import frappe
from frappe.utils.background_jobs import enqueue
from frappe.client import get_count as original_get_count
from frappe.core.doctype.prepared_report.prepared_report import PreparedReport

@frappe.whitelist()
def share_job_card(job_card_name, user_email):
    if not frappe.db.exists("Job Card", job_card_name):
        frappe.throw("Job Card not found")

    if not frappe.db.exists("User", user_email):
        frappe.throw("User not found")

    frappe.share.add(
        doctype="Job Card",
        name=job_card_name,
        user=user_email,
        read=1,
        write=0,
        share=0,
        submit=0
    )

    return f"Job Card {job_card_name} shared with {user_email}"

@frappe.whitelist()
def manager_only_action():
    frappe.only_for("QF Manager")

    return "Welcome, QF Manager! You are allowed to perform this action."

@frappe.whitelist()
def mark_as_delivered(job_card):
    doc = frappe.get_doc("Job Card", job_card)

    if doc.docstatus != 1 or doc.status != "Ready for Delivery":
        frappe.throw("Job Card must be submitted and ready for delivery before it can be marked as delivered.")

    doc.status = "Delivered"
    doc.delivery_date = frappe.utils.nowdate()
    doc.save()

    return {"name": doc.name, "status": doc.status}

@frappe.whitelist()
def reject_job(job_card, reason=None):
    doc = frappe.get_doc("Job Card", job_card)

    if doc.docstatus != 1:
        frappe.throw("Only submitted Job Cards can be rejected.")

    doc.status = "Cancelled"
    if reason:
        doc.remarks = (doc.remarks or "") + "\nRejected: " + reason
    doc.save()

    return {"name": doc.name, "status": doc.status}

@frappe.whitelist()
def transfer_technician(job_card, technician=None):
    doc = frappe.get_doc("Job Card", job_card)

    if not technician:
        frappe.throw("Technician is required.")

    doc.assigned_technician = technician
    doc.save()

    return {"name": doc.name, "assigned_technician": doc.assigned_technician}

@frappe.whitelist()
def transfer_job(from_tech, to_tech):
    try:
        frappe.db.sql(
            """
            UPDATE `tabJob Card`
            SET assigned_technician = %s
            WHERE assigned_technician = %s
            AND status IN ('Pending Diagnosis', 'In Repair')
            """,
            (to_tech, from_tech)
        )

        return {"message": "Jobs transferred successfully"}

    except Exception:
        frappe.log_error(
            message=frappe.get_traceback(),
            title="Job Transfer Failed"
        )
        raise

@frappe.whitelist()
def get_job_cards_unsafe():
    return frappe.get_all(
        "Job Card",
        fields="*"
    )

@frappe.whitelist()
def get_job_cards_safe():
    user = frappe.session.user
    roles = frappe.get_roles(user)

    job_cards = frappe.get_list(
        "Job Card",
        fields=[
            "name",
            "customer_name",
            "device_model",
            "issue_description",
            "payment_status",
            "customer_phone",
            "customer_email"
        ]
    )

    if "Manager" not in roles and "System Manager" not in roles:
        for jc in job_cards:
            jc.pop("customer_phone", None)
            jc.pop("customer_email", None)

    return job_cards

@frappe.whitelist(allow_guest=True)
def track_job(job_id):
    job = frappe.db.get_value(
        "Job Card",
        job_id,
        [
            "name",
            "customer_name",
            "device_type",
            "device_brand",
            "device_model",
            "problem_description",
            "assigned_technician",
            "diagnosis_notes",
            "estimated_cost",
            "diagnosis_date",
            "priority",
            "status",
            "delivery_date",
            "payment_status",
            "final_amount"
        ],
        as_dict=True
    )

    return job

def send_job_ready_email(job_card):
    doc = frappe.get_doc("Job Card", job_card)

    frappe.sendmail(
        recipients=[doc.customer_email],
        subject="Your Device is Ready",
        message=f"""
Hello {doc.customer_name},

Your device is ready for delivery.

Job Card: {doc.name}

Thank you.
"""
    )

@frappe.whitelist()
def custom_get_count(doctype, filters=None, debug=False, cache=False):
    frappe.get_doc({
        "doctype": "Audit Log",
        "doctype_name": doctype,
        "action": "count_queried",
        "user": frappe.session.user
    }).insert(ignore_permissions=True)

    return original_get_count(doctype, filters, debug, cache)

import frappe
from frappe.utils.background_jobs import enqueue
from frappe.core.doctype.prepared_report.prepared_report import generate_report

@frappe.whitelist()
def trigger_prepared_report(filters=None):
    # TEMP direct call
    run_prepared_report(filters, frappe.session.user)


def run_prepared_report(filters=None, user=None):
    if not filters:
        filters = {}

    prepared_report = frappe.get_doc({
        "doctype": "Prepared Report",
        "report_name": "Technician Performance Report",
        "filters": frappe.as_json(filters),
        "owner": user
    })
    prepared_report.insert(ignore_permissions=True)

    # ✅ THIS IS THE FIX
    generate_report(prepared_report.name)