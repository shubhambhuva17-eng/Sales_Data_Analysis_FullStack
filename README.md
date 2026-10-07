# Sales Data Analysis - Full Stack Project

## Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- Data storage: CSV
- Charts: Chart.js
- API: Flask JSON endpoints

## Features
- Create a customer bill
- Add multiple products
- Automatic total calculation
- Save every sale to `sales_data.csv`
- Generate a printable invoice
- Sales history
- Dashboard
- Best-selling product chart
- Monthly revenue chart
- Revenue-by-product chart
- REST API endpoints

## Installation

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

Install:
```bash
pip install -r requirements.txt
```

Run:
```bash
python app.py
```

Open:
http://127.0.0.1:5000

## API
- GET `/api/products`
- GET `/api/sales`
- GET `/api/dashboard`
- GET `/download-csv`

## Project structure

```text
Sales_Data_Analysis/
├── app.py
├── requirements.txt
├── sales_data.csv
├── README.md
├── bills/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── billing.html
│   ├── bill.html
│   ├── sales.html
│   └── dashboard.html
└── static/
    ├── style.css
    ├── billing.js
    └── dashboard.js
```
