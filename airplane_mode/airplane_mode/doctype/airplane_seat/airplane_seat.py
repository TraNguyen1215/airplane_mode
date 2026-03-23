# Copyright (c) 2026, Test and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document


class AirplaneSeat(Document):
	def validate(self):
		if not self.amount or self.amount == 0:
			self.amount = frappe.db.get_single_value("Airport Shop Management Settings", "standard_ticket_flight_amount")
			if self.level == "First":
				self.amount *= 2
			if self.level == "Business":
				self.amount *= 1.5
			if self.level == "Premium Economy":
				self.amount *= 1.2
			else:
				self.amount = self.amount
