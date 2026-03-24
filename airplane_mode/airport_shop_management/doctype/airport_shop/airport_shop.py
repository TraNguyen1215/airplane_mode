# Copyright (c) 2026, Test and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirportShop(WebsiteGenerator):
    def validate(self):
        if not self.rent_amount or self.rent_amount == 0:
            self.rent_amount = frappe.db.get_single_value("Airport Shop Management Settings", "standard_rental_amount")

    def before_save(self):
        if not self.route:
            self.route = f"airport_shop/{self.name}"
    def get_page_info(self):
        return {
			"title": self.name,
		}
