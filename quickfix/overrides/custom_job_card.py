import frappe
from quickfix.service_center.doctype.job_card.job_card import JobCard


class CustomJobCard(JobCard):

    def validate(self):
        super().validate()
        self._check_urgent_unassigned()

    def _check_urgent_unassigned(self):
        if self.priority == "Urgent" and not self.assigned_technician:
            settings = frappe.get_single("Quickfix Settings")

            frappe.enqueue(
                "quickfix.utils.send_urgent_alert",
                job_card=self.name,
                manager=settings.manager_email
            )
# MRO means the order Python follows to find methods when using inheritance.
# Since CustomJobCard extends JobCard, both can have validate().
# super().validate() runs the original JobCard validate() first.
# If we don’t call super(), important built-in checks may be skipped.
# So super() is required to keep Frappe working correctly.