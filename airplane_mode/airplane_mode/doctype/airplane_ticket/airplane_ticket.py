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
        self.total_amount = flt(self.flight_price) + flt(total_addons)
    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw("Chỉ có thể Submit vé khi trạng thái là 'Boarded'!")

    def before_insert(self):
        number = random.randint(1, 150)
        letter = random.choice(["A","B","C","D","E"])
        self.seat = f"{number}{letter}"
