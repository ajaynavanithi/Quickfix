
import frappe
import qrcode
import base64
from io import BytesIO

def get_qr_code(docname):
    url = f"https://your-site.com/app/job-card/{docname}"

    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    return base64.b64encode(buffer.getvalue()).decode()

def send_urgent_alert(job_card, manager):
    subject = "Urgent Job Card Unassigned"

    message = f"""
    Job Card <b>{job_card}</b> is marked as <b>Urgent</b> but has no technician assigned.
    Please take action immediately.
    """

    frappe.sendmail(
        recipients=[manager],
        subject=subject,
        message=message
    )   

def get_shop_name():
    return frappe.db.get_single_value("Quickfix Settings", "shop_name") or "Default Shop"
def format_job_id(value):
    return f"JOB#{value}"