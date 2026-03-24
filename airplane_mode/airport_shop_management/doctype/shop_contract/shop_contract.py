# Copyright (c) 2026, Test and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
from frappe.sessions import datetime


class ShopContract(Document):
	def before_save(self):
		from_date = datetime.strptime(self.start_date, "%Y-%m-%d")
		to_date = datetime.strptime(self.end_date, "%Y-%m-%d")

		months = (to_date.year - from_date.year) * 12 + (to_date.month - from_date.month)
		self.month_rent = months
		self.total_amount = self.month_rent * self.rent_amount
