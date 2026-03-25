from annotated_types import doc

import frappe
from frappe.utils.data import today
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
			"status": ["!=", "Cancelled"] and ["!=", "Paid"],
		},
		fields=["name", "tenant", "rent_amount", "payment_date", "status", "contract", "shop"]
	)

    settings = frappe.get_single("Airport Shop Management Settings")

    if settings.allow_remind_to_payment_rental_shop == False or not settings.allow_remind_to_payment_rental_shop or settings.allow_remind_to_payment_rental_shop == 0:
        return

    for invoice in rent_invoice:
        tenant_email = frappe.db.get_value("Tenant", invoice.tenant, "email")
        if tenant_email:
            frappe.sendmail(
				recipients=tenant_email,
				subject="Rent Payment Reminder",
				message=f"""This is a reminder to pay your rent for this month.
                Please make the payment at your earliest convenience.
                \t\tRent Invoice: {invoice.name}
                \t\tAmount Due: {invoice.rent_amount} VND
                \t\tDue Date: {invoice.payment_date}
                \t\tShop: {invoice.shop}
                \t\tContract: {invoice.contract}
                \t\tStatus: {invoice.status}
				""",
		)

# def update_shop_status(doc, method):
#     if not doc.tenant or not doc.contract:
#         doc.status = "Available"
#         return
#     contract = frappe.get_doc("Contract", doc.contract)
#     if contract.status == "Active":
#         if contract.end_date and contract.end_date >= today():
#             doc.status = "Occupied"
#         else:
#             doc.status = "Expired"
#     else:
#         doc.status = "Available"

def create_rent_invoice_for_active_contracts():
	active_contracts = frappe.get_all(
		"Shop Contract",
		filters={"status": "Active"},
		fields=["name", "tenant", "total_amount", "end_date"]
	)

	for contract in active_contracts:
		if contract.end_date and contract.end_date >= today():
			invoice = frappe.new_doc("Rent Invoice")
			invoice.tenant = contract.tenant
			invoice.amount = contract.total_amount
			invoice.contract = contract.name
			invoice.save()

def send_email_notification_for_change_gate(flight, gate):
	tickets = frappe.get_all("Airplane Ticket",
		filters={"flight": flight},
		fields=["name"]
	)

	for t in tickets:
		if t.name:
			frappe.sendmail(
				recipients="tratthunguyen1215@gmail.com",
				subject="Gate Change Notification",
				message=f"""Dear Passenger,
				We would like to inform you that the gate for your flight {flight} has been changed to {gate}.
				Please make sure to check the updated gate information before your departure.
				Thank you for your understanding.
				""",
		)
