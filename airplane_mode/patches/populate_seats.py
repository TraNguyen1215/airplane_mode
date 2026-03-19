import frappe
import random

def execute():
    tickets = frappe.get_all("Airplane Ticket", filters={"seat": ["in", ["", None]]})

    for t in tickets:
        doc = frappe.get_doc("Airplane Ticket", t.name)
        random_num = random.randint(1, 99)
        random_letter = random.choice(['A', 'B', 'C', 'D', 'E'])

        doc.db_set("seat", f"{random_num}{random_letter}")
