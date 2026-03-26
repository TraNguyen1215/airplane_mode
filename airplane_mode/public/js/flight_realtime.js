frappe.realtime.on("flight_scheduled", (data) => {
	frappe.msgprint(`Flight ${data.flight} has been scheduled! Route: ${data.route}`);
});
