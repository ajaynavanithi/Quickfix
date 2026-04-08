import frappe


def get_shop_name():
    return frappe.db.get_single_value("Quickfix Settings", "shop_name") or "Default Shop"


def format_job_id(value):
    return f"JOB#{value}"
