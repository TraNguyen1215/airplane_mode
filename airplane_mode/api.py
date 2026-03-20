import frappe
def update_gate_in_tickets(flight, gate):
    tickets = frappe.get_all("Airplane Ticket",
        filters={"flight": flight},
        fields=["name"]
    )

    for t in tickets:
        frappe.db.set_value("Airplane Ticket", t.name, "gate_number", gate)
