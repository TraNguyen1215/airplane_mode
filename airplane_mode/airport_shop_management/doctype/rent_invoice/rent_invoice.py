# Copyright (c) 2026, Test and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RentInvoice(Document):
    # def validate(self):
    #     current_date = frappe.utils.nowdate()
    #     if self.status != "Paid" and self.payment_date:
    #         if self.payment_date < current_date:
    #             self.db_set("status", "Overdue")
    #         else:
    #             self.db_set("status", "Pending")
    pass
