from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file, flash
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import csv
import os

app = Flask(__name__)
app.secret_key = "sales-analysis-demo-secret"

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "sales_data.csv"
BILLS_DIR = BASE_DIR / "bills"
BILLS_DIR.mkdir(exist_ok=True)

PRODUCTS = [
    {"name": "Laptop", "price": 45000},
    {"name": "Mobile", "price": 18000},
    {"name": "Keyboard", "price": 1200},
    {"name": "Mouse", "price": 600},
    {"name": "Monitor", "price": 10000},
    {"name": "Printer", "price": 8000},
    {"name": "Headphone", "price": 1500},
    {"name": "USB Cable", "price": 300},
]

HEADERS = ["Date", "Bill No", "Customer", "Product", "Quantity", "Price", "Total"]


def ensure_csv():
    if not CSV_FILE.exists():
        with CSV_FILE.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(HEADERS)


def read_sales():
    ensure_csv()
    with CSV_FILE.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_product(name):
    return next((p for p in PRODUCTS if p["name"] == name), None)


def next_bill_number():
    numbers = []
    for row in read_sales():
        try:
            numbers.append(int(row["Bill No"].replace("B", "")))
        except (ValueError, AttributeError):
            pass
    return f"B{max(numbers, default=0) + 1:03d}"


def dashboard_data():
    sales = read_sales()
    product_qty = defaultdict(int)
    product_revenue = defaultdict(float)
    monthly_revenue = defaultdict(float)

    total_revenue = 0.0
    total_items = 0
    bills = set()

    for row in sales:
        qty = int(row["Quantity"])
        total = float(row["Total"])
        product = row["Product"]
        product_qty[product] += qty
        product_revenue[product] += total
        total_revenue += total
        total_items += qty
        bills.add(row["Bill No"])

        try:
            dt = datetime.strptime(row["Date"], "%d-%m-%Y")
            month = dt.strftime("%Y-%m")
        except ValueError:
            month = row["Date"][:7]
        monthly_revenue[month] += total

    products = sorted(product_qty.items(), key=lambda x: x[1], reverse=True)
    revenue_products = sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)

    month_keys = sorted(monthly_revenue)
    monthly_labels = []
    monthly_values = []
    for key in month_keys:
        monthly_labels.append(datetime.strptime(key, "%Y-%m").strftime("%b %Y"))
        monthly_values.append(round(monthly_revenue[key], 2))

    return {
        "total_sales": round(total_revenue, 2),
        "total_bills": len(bills),
        "total_items": total_items,
        "best_product": products[0][0] if products else "No sales",
        "product_names": [p[0] for p in products],
        "product_quantities": [p[1] for p in products],
        "revenue_product_names": [p[0] for p in revenue_products],
        "revenue_product_values": [round(p[1], 2) for p in revenue_products],
        "months": monthly_labels,
        "month_values": monthly_values,
    }


@app.route("/")
def index():
    data = dashboard_data()
    return render_template("index.html", products=PRODUCTS, data=data)


@app.route("/billing")
def billing():
    return render_template("billing.html", products=PRODUCTS)


@app.post("/create_bill")
def create_bill():
    customer = request.form.get("customer", "").strip()
    product_names = request.form.getlist("product[]")
    quantities = request.form.getlist("quantity[]")

    if not customer:
        flash("Customer name is required.", "error")
        return redirect(url_for("billing"))

    items = []
    for product_name, qty_text in zip(product_names, quantities):
        product = get_product(product_name)
        try:
            quantity = int(qty_text)
        except (ValueError, TypeError):
            quantity = 0

        if not product or quantity <= 0:
            continue

        total = product["price"] * quantity
        items.append({
            "product": product["name"],
            "quantity": quantity,
            "price": product["price"],
            "total": total,
        })

    if not items:
        flash("Add at least one valid product.", "error")
        return redirect(url_for("billing"))

    bill_no = next_bill_number()
    date = datetime.now().strftime("%d-%m-%Y")

    with CSV_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for item in items:
            writer.writerow([
                date, bill_no, customer, item["product"],
                item["quantity"], item["price"], item["total"]
            ])

    grand_total = sum(item["total"] for item in items)

    txt_path = BILLS_DIR / f"{bill_no}.txt"
    with txt_path.open("w", encoding="utf-8") as f:
        f.write("SALES INVOICE\n")
        f.write("=" * 50 + "\n")
        f.write(f"Bill No : {bill_no}\n")
        f.write(f"Date    : {date}\n")
        f.write(f"Customer: {customer}\n")
        f.write("-" * 50 + "\n")
        for item in items:
            f.write(
                f"{item['product']} | Qty: {item['quantity']} | "
                f"Price: Rs.{item['price']:.2f} | Total: Rs.{item['total']:.2f}\n"
            )
        f.write("-" * 50 + "\n")
        f.write(f"Grand Total: Rs.{grand_total:.2f}\n")

    return render_template(
        "bill.html",
        bill_no=bill_no,
        date=date,
        customer=customer,
        items=items,
        grand_total=grand_total,
    )


@app.route("/sales")
def sales():
    return render_template("sales.html", sales=list(reversed(read_sales())))


@app.route("/dashboard")
def dashboard():
    data = dashboard_data()
    return render_template("dashboard.html", data=data)


# ---------------- API ----------------

@app.get("/api/products")
def api_products():
    return jsonify(PRODUCTS)


@app.get("/api/sales")
def api_sales():
    return jsonify(read_sales())


@app.get("/api/dashboard")
def api_dashboard():
    return jsonify(dashboard_data())


@app.get("/download-csv")
def download_csv():
    ensure_csv()
    return send_file(CSV_FILE, as_attachment=True, download_name="sales_data.csv")


@app.get("/download-bill/<bill_no>")
def download_bill(bill_no):
    path = BILLS_DIR / f"{bill_no}.txt"
    if not path.exists():
        return "Bill not found", 404
    return send_file(path, as_attachment=True, download_name=path.name)


if __name__ == "__main__":
    ensure_csv()
    app.run(debug=True)
