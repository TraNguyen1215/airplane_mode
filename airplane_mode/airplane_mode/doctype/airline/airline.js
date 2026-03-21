// Copyright (c) 2026, Test and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Airline", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Airline", {
	refresh: function (frm) {
		if (!frm.doc.website) {
			return;
		}
		frm.add_web_link(frm.doc.website, "Website");
	},
});
