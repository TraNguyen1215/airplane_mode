# Copyright (c) 2026, Test and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document


class ShopContract(Document):
	def validate(self):
		if not self.rent_amount or self.rent_amount == 0:
			self.rent_amount = frappe.db.get_single_value("Airport Shop Management Settings", "standard_rental_amount")
