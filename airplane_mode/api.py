from annotated_types import doc

import frappe
def update_gate_in_tickets(flight, gate):
    tickets = frappe.get_all("Airplane Ticket",
        filters={"flight": flight},
        fields=["name"]
    )

    for t in tickets:
        frappe.db.set_value("Airplane Ticket", t.name, "gate_number", gate)

def send_email_reminder_for_tenant():
    rent_invoice = frappe.get_all(
		"Rent Invoice",
		filters={
			"payment_date": frappe.utils.today(),
			"status": ["!=", "Paid"]
		},
		fields=["name", "tenant", "amount"]
	)
    for invoice in rent_invoice:
        tenant = frappe.db.get_value("Tenant")
        tenant_email = tenant.email if tenant else None
        if tenant_email:
            frappe.sendmail(
				recipients=tenant_email,
				subject="Rent Payment Reminder",
				message=f"This is a reminder to pay your rent for this month. Please make the payment at your earliest convenience."
		)
