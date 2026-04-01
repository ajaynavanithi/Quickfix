import frappe

def after_install():
    """Runs once when the app is installed"""


    device_types = ["Smartphone", "Laptop", "Tablet"]

    for device in device_types:
        if not frappe.db.exists("Device Type", {"device_type": device}):
            frappe.get_doc({
                "doctype": "Device Type",
                "device_type": device
            }).insert(ignore_permissions=True)

    
    if not frappe.db.exists("Quickfix Settings", "Quickfix Settings"):
        frappe.get_doc({
            "doctype": "Quickfix Settings",
            "shop_name": "QuickFix Shop",
            "manager_email": frappe.session.user,
            "default_labour_charge": 500,
            "low_stock_alert_enabled": 1
        }).insert(ignore_permissions=True)

    
    frappe.msgprint("QuickFix setup completed successfuly!")
def extend_bootinfo(bootinfo):
    """Add QuickFix shop info to bootinfo sent to client"""

    settings = frappe.get_single("Quickfix Settings")

    bootinfo.quickfix_shop_name = settings.shop_name
    bootinfo.quickfix_manager_email = settings.manager_email