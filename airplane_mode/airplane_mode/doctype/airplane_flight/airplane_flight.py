# Copyright (c) 2026, Test and contributors
# For license information, please see license.txt

# import frappe
from multiprocessing import context

import frappe
from frappe.model.document import Document
from frappe.website.website_generator import WebsiteGenerator

class AirplaneFlight(Document):
    def before_save(self):
        if not self.route:
            self.route = f"/flights/{self.name}"

        for row in self.flight_crew:
            frappe.db.set_value(
                "Flight Crew Member",
                row.crew_name,
                "is_assigned",
                1
            )
    def on_submit(self):
        self.db_set("status", "Completed")

        for row in self.flight_crew:
            frappe.db.set_value(
                "Flight Crew Member",
                row.crew_name,
                "is_assigned",
                0
            )

    def on_update(self):
        if self.has_value_changed("gate_number"):
            frappe.enqueue(
				"airplane_mode.api.update_gate_in_tickets",
				flight=self.name,
				gate=self.gate_number
			)
            frappe.enqueue(
                "airplane_mode.api.send_email_notification_for_change_gate",
                flight=self.name,
                gate=self.gate_number
            )

    # Bam nut cancel thi status flght = cancelled va cac flight crew se chuyen is assigned = 0
    def on_cancel(self):
        self.db_set("status", "Cancelled")

        for row in self.flight_crew:
            frappe.db.set_value(
                "Flight Crew Member",
                row.crew_name,
                "is_assigned",
                0
            )

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
