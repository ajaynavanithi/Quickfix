// Example shipped JS equivalent for Client Script DocType customization
// This could be placed in the app for version-controlled Reject Job button

frappe.ui.form.on('Job Card', {
	refresh: function(frm) {
		if (frm.doc.docstatus == 1) {
			frm.add_custom_button("Reject Job (Shipped)", function() {
				let d = new frappe.ui.Dialog({
					title: "Reject Job",
					fields: [
						{ label: "Rejection Reason", fieldname: "reason", fieldtype: "Small Text", reqd: 1 }
					],
					primary_action_label: "Submit",
					primary_action(values) {
						frappe.call({
							method: "quickfix.api.reject_job",
							args: { job_card: frm.doc.name, reason: values.reason },
							callback: function() {
								frappe.msgprint("Job Rejected");
								d.hide();
								frm.reload_doc();
							}
						});
					}
				});
				d.show();
			});
		}
	}
});