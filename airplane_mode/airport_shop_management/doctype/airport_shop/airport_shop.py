# Copyright (c) 2026, Test and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirportShop(WebsiteGenerator):
    def before_save(self):
        if not self.route:
            self.route = f"/airport_shop/{self.name}"
    def get_page_info(self):
        return {
			"title": self.name,
		}
