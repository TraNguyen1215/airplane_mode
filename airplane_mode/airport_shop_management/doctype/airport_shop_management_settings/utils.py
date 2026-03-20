import frappe

def send_rent_reminders():
    settings = frappe.db.get_single_value("Airport Shop Management Settings")

    if not settings.allow_remind_to_payment_rental_shop:
        frappe.logger().info("Rent reminders are disabled")
        return

    contracts = frappe.get_all(
        "Shop Contract",
        filters={"status": "Active"},
        fields=["name", "tenant", "shop", "rent_amount"]
    )

    for c in contracts:
        tenant = frappe.get_doc("Tenant", c.tenant)

        if not tenant.email:
            continue

        frappe.sendmail(
            recipients=[tenant.email],
            subject="Rent Due Reminder",
            message=f"""
Dear {tenant.tenant_name},

Your rent for shop {c.shop} is due this month.
Amount: {c.rent_amount}

Please make the payment on time.

Thanks.
"""
        )
