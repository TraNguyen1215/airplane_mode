// Copyright (c) 2026, Test and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport Shop", {
	setup: function (frm) {
		frm.set_query("shop_type", function () {
			return {
				filters: {
					enabled: 1,
				},
			};
		});
	},
});
