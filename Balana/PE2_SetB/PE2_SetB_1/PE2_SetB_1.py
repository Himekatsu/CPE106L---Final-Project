# BALANA, FRANCIS DOMINIC G.
# CPE106L-4-E02
# SET B
# PE2_SetB_1.py
# Problem 1: Customer Spending by Country (Flet & SQLite)
# Task: Build a Flet app that shows total spending per customer grouped by country.
# Requirements:

#   > Use SQLite to fetch customer, invoice, and invoice item data.
#   > Calculate total spending per customer.
#   > Group by country and compute average spending per customer.
#   > Display in a Flet DataTable, sorted by average spending (descending).

# SubTask 1: Fetch customer, invoice, and invoice item data.

import flet as ft
import sqlite3
import json
from collections import defaultdict

def fetch_data_from_json():
    with open("customers.json") as f:
        customers = json.load(f)
    with open("invoices.json") as f:
        invoices = json.load(f)
    with open("invoice_items.json") as f:
        invoice_items = json.load(f)
    return customers, invoices, invoice_items

# SubTask 2: Calculate total spending per customer.

def process_data(customers, invoices, invoice_items):
    
    customer_lookup = {c["CustomerId"]: c for c in customers}
    invoice_lookup = {i["InvoiceId"]: i for i in invoices}

    
    customer_spending = defaultdict(float)
    customer_country = {}
    for item in invoice_items:
        invoice = invoice_lookup[item["InvoiceId"]]
        cust_id = invoice["CustomerId"]
        customer = customer_lookup[cust_id]
        spending = item["UnitPrice"] * item["Quantity"]
        customer_spending[cust_id] += spending
        customer_country[cust_id] = (
            customer["FirstName"],
            customer["LastName"],
            customer["Country"],
        )

# SubTask 3: Group by country and compute average spending per customer.

    country_totals = defaultdict(list)
    for cust_id, total in customer_spending.items():
        fname, lname, country = customer_country[cust_id]
        country_totals[country].append((f"{fname} {lname}", total))

    country_averages = []
    for country, customers in country_totals.items():
        avg = sum(total for _, total in customers) / len(customers)
        country_averages.append((country, avg, customers))

    
    country_averages.sort(key=lambda x: x[1], reverse=True)
    return country_averages

def main(page: ft.Page):
    page.title = "Customer Spending by Country (JSON)"
    customers, invoices, invoice_items = fetch_data_from_json()
    country_averages = process_data(customers, invoices, invoice_items)

    table_rows = []
    for country, avg, customers in country_averages:
        for name, total in customers:
            table_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(country)),
                        ft.DataCell(ft.Text(name)),
                        ft.DataCell(ft.Text(f"${total:.2f}")),
                        ft.DataCell(ft.Text(f"${avg:.2f}")),
                    ]
                )
            )

# SubTask 4: Displaying via Flet datatable.

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Country")),
            ft.DataColumn(ft.Text("Customer")),
            ft.DataColumn(ft.Text("Total Spending")),
            ft.DataColumn(ft.Text("Avg Spending (Country)")),
        ],
        rows=table_rows,
    )

    page.add(
        ft.Column(
            [table],
            scroll="auto",
            height=500,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)