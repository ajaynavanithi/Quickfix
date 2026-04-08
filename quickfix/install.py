import frappe


def after_install():
    device_types = ["Smartphone", "Laptop", "Tablet"]

    for device in device_types:
        if not frappe.db.exists("Device Type", device):
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

    if not frappe.db.exists(
        "Property Setter",
        {"doc_type": "Job Card", "field_name": "remarks", "property": "bold"},
    ):
        frappe.make_property_setter(
            {
                "doctype": "Job Card",
                "fieldname": "remarks",
                "property": "bold",
                "value": "1",
                "property_type": "Check",
            },
            validate_fields_for_doctype=False,
        )


def extend_bootinfo(bootinfo):
    settings = frappe.get_single("Quickfix Settings")
    bootinfo.quickfix_shop_name = settings.shop_name
    bootinfo.quickfix_manager_email = settings.manager_email
