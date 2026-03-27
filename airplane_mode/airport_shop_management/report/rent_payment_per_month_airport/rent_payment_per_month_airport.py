# Copyright (c) 2026, Test and contributors
# For license information, please see license.txt

import frappe
from collections import defaultdict
from datetime import datetime

def execute(filters=None):
    filters = filters or {}

    conditions = []
    values = {}

    conditions.append("rent.docstatus = 1")

    if filters.get("airport"):
        conditions.append("shop.airport = %(airport)s")
        values["airport"] = filters.get("airport")

    if filters.get("shop"):
        conditions.append("rent.shop = %(shop)s")
        values["shop"] = filters.get("shop")

    if filters.get("status"):
        conditions.append("rent.status = %(status)s")
        values["status"] = filters.get("status")

    if filters.get("from_date"):
        conditions.append("rent.payment_date >= %(from_date)s")
        values["from_date"] = filters.get("from_date")

    if filters.get("to_date"):
        conditions.append("rent.payment_date <= %(to_date)s")
        values["to_date"] = filters.get("to_date")

    if filters.get("contract"):
        conditions.append("rent.contract = %(contract)s")
        values["contract"] = filters.get("contract")

    if filters.get("tenant"):
        conditions.append("rent.tenant = %(tenant)s")
        values["tenant"] = filters.get("tenant")

    if filters.get("shop_type"):
        conditions.append("shop.shop_type = %(shop_type)s")
        values["shop_type"] = filters.get("shop_type")

    condition_sql = " AND ".join(conditions)
    if condition_sql:
        condition_sql = "WHERE " + condition_sql

    data = frappe.db.sql("""
        SELECT
            rent.shop,
            rent.payment_date,
            rent.total_amount,
            rent.status,
            contract.name as contract,
            shop.airport,
            shop.shop_type,
			rent.tenant
        FROM `tabRent Invoice` rent
        LEFT JOIN `tabShop Contract` contract ON rent.contract = contract.name
        LEFT JOIN `tabAirport Shop` shop ON rent.shop = shop.name
        {0}
    """.format(condition_sql), values, as_dict=1)

    monthly_data = defaultdict(float)
    result = []

    for d in data:
        revenue = d.total_amount if d.status == "Paid" else 0

        if d.payment_date:
            month_key = d.payment_date.strftime("%Y-%m")
            monthly_data[month_key] += revenue

        result.append({
            "month": d.payment_date.strftime("%Y-%m") if d.payment_date else "",
            "shop": d.shop,
            "airport": d.airport,
            "tenant": d.tenant,
            "shop_type": d.shop_type,
            "contract": d.contract,
            "status": d.status,
            "total_amount": d.total_amount,
            "revenue": revenue
        })

    total_revenue = sum(monthly_data.values())

    columns = [
        {
            "label": "Month",
            "fieldname": "month",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "Shop",
            "fieldname": "shop",
            "fieldtype": "Link",
            "options": "Airport Shop",
            "width": 180
        },
        {
            "label": "Airport",
            "fieldname": "airport",
            "fieldtype": "Link",
            "options": "Airport",
            "width": 150
        },
        {
            "label": "Contract",
            "fieldname": "contract",
            "fieldtype": "Link",
            "options": "Shop Contract",
            "width": 180
        },
        {
            "label": "Shop Type",
            "fieldname": "shop_type",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": "Tenant",
            "fieldname": "tenant",
            "fieldtype": "Link",
            "options": "Tenant",
            "width": 150
        },
        {
            "label": "Status",
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "Amount",
            "fieldname": "total_amount",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": "Revenue",
            "fieldname": "revenue",
            "fieldtype": "Currency",
            "width": 150
        }
    ]

    sorted_months = sorted(monthly_data.keys())

    chart = {
        "data": {
            "labels": sorted_months,
            "datasets": [
                {
                    "name": "Revenue",
                    "values": [monthly_data[m] for m in sorted_months]
                }
            ]
        },
        "type": "bar"
    }

    summary = [
        {
            "label": "Total Revenue",
            "value": total_revenue,
            "indicator": "Green"
        }
    ]

    return columns, result, None, chart, summary
