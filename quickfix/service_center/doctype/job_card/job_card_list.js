// Copyright (c) 2026, navanithi and contributors
// For license information, please see license.txt

frappe.listview_settings['Job Card'] = {
	add_fields: ["final_amount", "priority"],
	get_indicator: function(doc) {
		if (doc.status == "Pending") {
			return [__("Pending"), "orange", "status,=,Pending"];
		} else if (doc.status == "In Repair") {
			return [__("In Repair"), "blue", "status,=,In Repair"];
		} else if (doc.status == "Ready for Delivery") {
			return [__("Ready for Delivery"), "green", "status,=,Ready for Delivery"];
		} else if (doc.status == "Completed") {
			return [__("Completed"), "gray", "status,=,Completed"];
		}
	},
	formatters: {
		final_amount: function(value) {
			return value ? "₹" + value : "";
		}
	},
	onload: function(listview) {
		listview.page.add_inner_button(__("Quick Action for In Repair"), function() {
			let selected = listview.get_checked_items();
			selected.forEach(function(doc) {
				if (doc.status == "In Repair") {
					frappe.msgprint("Quick action applied to " + doc.name);
					// Example: Could call an API to update status
				}
			});
		});
	}
};