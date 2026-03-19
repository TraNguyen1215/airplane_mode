# Copyright (c) 2026, Test and contributors
# For license information, please see license.txt

# import frappe
from multiprocessing import context

import frappe
from frappe.model.document import Document
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(Document):
    def on_submit(self):
        self.db_set("status", "Completed")
    def get_page_info(self):
        return {
            "title": self.name,
        }
    def get_context(self, context):
        if not self.is_published:
            raise frappe.DoesNotExistError
        airline = frappe.db.get_value("Airplane", self.airplane, "airline")
        context.airline = airline
        context.airline_short = airline.split("-")[0] if airline else ""
