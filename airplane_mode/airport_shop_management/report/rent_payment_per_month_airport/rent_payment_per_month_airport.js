// Copyright (c) 2026, Test and contributors
// For license information, please see license.txt

frappe.query_reports["Rent Payment Per Month Airport"] = {
	filters: [
		{
			fieldname: "airport",
			label: "Airport",
			fieldtype: "Link",
			options: "Airport",
			reqd: 0,
		},
		{
			fieldname: "shop",
			label: "Shop",
			fieldtype: "Link",
			options: "Airport Shop",
			reqd: 0,
		},
		{
			fieldname: "shop_type",
			label: "Shop Type",
			fieldtype: "Link",
			options: "Shop Type",
			reqd: 0,
		},
		{
			fieldname: "from_date",
			label: "From Date",
			fieldtype: "Date",
		},
		{
			fieldname: "to_date",
			label: "To Date",
			fieldtype: "Date",
		},
		{
			fieldname: "status",
			label: "Status",
			fieldtype: "Select",
			options: "\nPaid\nPending\nOverdue",
			default: "Paid",
			reqd: 1,
		},
		{
			fieldname: "contract",
			label: "Contract",
			fieldtype: "Link",
			options: "Shop Contract",
		},
		{
			fieldname: "tenant",
			label: "Tenant",
			fieldtype: "Link",
			options: "Tenant",
		},
	],
};
