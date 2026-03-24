# Copyright (c) 2026, Test and contributors
# For license information, please see license.txt

# import frappe
from random import random

import frappe
from frappe.model.document import Document
from frappe.utils import flt
import random


class AirplaneTicket(Document):
    def validate(self):
        unique_addons = []
        cleaned_addons = []
        for d in self.add_ons:
            if d.item not in unique_addons:
                unique_addons.append(d.item)
                cleaned_addons.append(d)
        self.set("add_ons", cleaned_addons)

        total_addons = sum([d.amount for d in self.add_ons])

        # seat
        list_seats =[]
        for ls in self.seat:
            if ls.item not in list_seats:
                list_seats.append({
					"item": ls.item,
					"row": ls.row,
					"number": ls.number,
					"level": ls.level,
					"amount": ls.amount
				})
        self.set("seat", list_seats)

        total_seat_amount = sum([d.amount for d in self.seat])

        self.total_amount = flt(total_addons) + flt(total_seat_amount)

        flight = frappe.get_doc("Airplane Flight", self.flight)

        airplane = frappe.get_doc("Airplane", flight.airplane)

        capacity = airplane.capacity

        ticket_count = frappe.db.count(
            "Airplane Ticket",
            {
                "flight": self.flight,
                "docstatus": ["!=", 2]
            }
        )

        if ticket_count >= capacity:
            frappe.throw("Flight is already full")

    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw("Chỉ có thể Submit vé khi trạng thái là 'Boarded'!")

    # def before_insert(self):
    #     number = random.randint(1, 150)
    #     letter = random.choice(["A","B","C","D","E"])
    #     self.seat = f"{number}{letter}"

    # def on_update(self):
    #     if self.has_value_changed("flight"):
    #         # Cap nhat lai name trong Airplane Ticket khi flight thay doi
