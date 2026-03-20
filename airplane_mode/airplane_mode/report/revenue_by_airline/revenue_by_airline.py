# Copyright (c) 2026, Test@example.com and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data

import frappe

def execute(filters=None):

    data = frappe.db.sql("""
        SELECT
            al.name as airline,
            SUM(t.flight_price) as revenue
        FROM `tabAirline` al
        LEFT JOIN `tabAirplane` ap ON ap.airline = al.name
        LEFT JOIN `tabAirplane Flight` af ON af.airplane = ap.name
        LEFT JOIN `tabAirplane Ticket` t ON t.flight = af.name
        GROUP BY al.name
    """, as_dict=1)

    for d in data:
        d["revenue"] = float(d["revenue"] or 0)

    total_revenue = sum(d.revenue or 0 for d in data)

    columns = [
        {
            "label": "Airline",
            "fieldname": "airline",
            "fieldtype": "Link",
            "options": "Airline",
            "width": 200
        },
        {
            "label": "Revenue",
            "fieldname": "revenue",
            "fieldtype": "Currency",
            "width": 150,
            "default": 0
        }
    ]

    chart = {
        "data": {
            "labels": [d["airline"] for d in data],
            "datasets": [
                {"values": [d["revenue"] or 0 for d in data]}
            ]
        },
        "type": "donut"
    }

    summary = [
        {
            "label": "Total Revenue",
            "value": total_revenue,
            "indicator": "Green"
        }
    ]

    return columns, data, None, chart, summary
