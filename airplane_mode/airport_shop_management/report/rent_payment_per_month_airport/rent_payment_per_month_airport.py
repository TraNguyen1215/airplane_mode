# Copyright (c) 2026, Test and contributors
# For license information, please see license.txt

import frappe

#
def execute(filters=None):
    data = frappe.db.sql("""
        SELECT rent.shop, rent, rent.payment_date, rent.total_amount, rent.status, contract.name as contract, shop.airport
		FROM `tabRent Invoice` rent
		LEFT JOIN `tabShop Contract` contract ON rent.contract = contract.name
		LEFT JOIN `tabAirport Shop` shop ON rent.shop = shop.name
    """, as_dict=1)

    for d in data:
        if d.status == "Paid":
            d['revenue'] = d.total_amount
        elif d.status == "Overdue":
            d['revenue'] = 0
        else:
            d['revenue'] = 0
    total_revenue = sum(d['revenue'] for d in data)
    columns = [
		{
			"label": "Month",
			"fieldname": "payment_date",
			"fieldtype": "Date",
			"width": 150
		},
        {
			"label": "Shop",
			"fieldname": "shop",
			"fieldtype": "Link",
			"options": "Airport Shop",
			"width": 200
		},
		{
			"label": "Aiport",
			"fieldname": "airport",
			"fieldtype": "Link",
			"options": "Airport",
			"width": 200
		},
        {
			"label": " Contract",
			"fieldname": "contract",
			"fieldtype": "Link",
			"options": "Shop Contract",
			"width": 200
		},
        {
			"label": "Status",
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 200

		},
        {
			"label": "Pending Amount",
			"fieldname": "total_amount",
			"fieldtype": "Currency",
			"width": 200
		}
	]

    chart = {
		"data": {
			"labels": [d["payment_date"].strftime("%B %Y") for d in data],
			"datasets": [
				{"values": [d["revenue"] or 0 for d in data]}
			]
		},
		"type": "line"
    }

    summary = [
		{
			"label": "Total Revenue",
			"value": total_revenue,
			"indicator": "Green"
		}
	]

    return columns, data, None, chart, summary
