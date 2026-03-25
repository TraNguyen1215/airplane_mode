// Copyright (c) 2026, Test and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Flight", {
	setup(frm) {
		frm.set_query("crew_name", "flight_crew", function (doc, cdt, cdn) {
			return {
				filters: {
					is_assigned: 0,
				},
			};
		});
	},
});
