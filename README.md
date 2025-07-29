# Vendor-Analytics-Overview

# Vendor Performance Analysis Project

An end-to-end real-world data analytics project that leverages **Python**, **SQL (SQLite)**, and **Power BI** to evaluate vendor performance based on sales, purchase, and inventory data. This project mimics a complete analytics pipeline used in the industry and serves as a powerful addition to a data analyst’s portfolio.

---

## 📅 Table of Contents

* [Problem Statement](#problem-statement)
* [Tech Stack](#tech-stack)
* [Project Workflow](#project-workflow)
* [Database & Aggregation](#database--aggregation)
* [Power BI Dashboard](#power-bi-dashboard)
* [Key Insights](#key-insights)
* [Setup Instructions](#setup-instructions)
* [Project Structure](#project-structure)
* [Credits](#credits)

---

## ❓ Problem Statement

Vendors are key stakeholders in any retail or wholesale operation. However, identifying which vendors drive profitability and which do not requires careful analysis. This project aims to:

* Evaluate vendor performance across sales and purchase metrics
* Detect inefficiencies in inventory turnover and pricing
* Identify top- and low-performing brands
* Guide business decisions around stocking, marketing, and vendor management

---

## ⚙️ Tech Stack

| Tool       | Purpose                                  |
| ---------- | ---------------------------------------- |
| Python     | Data ingestion, cleaning, aggregation    |
| SQLite     | Lightweight relational database          |
| SQLAlchemy | Database connection and ORM              |
| Power BI   | Dashboard creation & visualizations      |
| Pandas     | Data manipulation and transformation     |
| Logging    | Real-time process tracking and debugging |

---

## 🔄 Project Workflow

### 1. 📂 Data Exploration & Cleaning

* Raw data from 6 CSVs including: `purchases.csv`, `purchase_prices.csv`, `sales.csv`, `vendor_invoice.csv`, etc.
* Loaded and explored using SQLite and Pandas
* Standardized data (nulls, whitespaces, datatypes) and joined relevant tables

### 2. ⚙️ Logging Setup

* Real-time logging implemented to track:

  * Table creation
  * Data ingestion
  * Error handling

### 3. 📅 Ingestion & Transformation

* Built `ingestion.py` script to automate data ingestion
* Used `get_vendor_summary.py` to:

  * Aggregate data using complex SQL joins and CTEs
  * Generate `vendor_sales_summary` table with key business metrics

### 4. 📊 Power BI Dashboard

* Connected directly to the `warehouse.db` SQLite database
* Visualizations include:

  * Vendor-wise performance metrics
  * Brand-wise profitability
  * Sales vs Purchase trends
  * Inventory turnover analysis

---

## 📊 Database & Aggregation

Key calculated metrics:

* **Gross Profit** = Sales - Purchase
* **Profit Margin** = (Gross Profit / Sales) \* 100
* **Stock Turnover** = Sales Quantity / Purchase Quantity
* **Sales-to-Purchase Ratio** = Total Sales / Total Purchase

Summary table constructed using optimized SQL queries with:

* Sales Summary
* Purchase Summary
* Freight Charges

---

## 📊 Power BI Dashboard

Highlights of the dashboard:

* Top Vendors by Sales
* Vendor Stock Turnover Ratio
* Brand-level Profitability
* Sales vs Purchase Comparison
* Outliers in Purchase Pricing
* Contribution to Total Sales
  

> To display only **Top 10 Vendors**: apply a **Top N filter** on your chart in Power BI by selecting the visual, dragging `VendorName` to the Filters pane, choosing "Top N", and setting N = 10 based on the relevant metric (e.g. Sum of Sales).
<img width="1317" height="699" alt="Screenshot 2025-07-29 225549" src="https://github.com/user-attachments/assets/c3fda11a-9760-4d18-bdd2-c61b1a151428" />

---

## 📊 Key Insights

* **Top Vendors**: Martignetti Companies and E & J Gallo Winery showed superior sales performance
* **Best-Selling Product**: Johnnie Walker Red Label
* **Inventory Warnings**: Low-performing vendors with high purchase costs
* **Operational Issues**: Poor pricing strategy and stock delays indicated by pricing outliers and turnover ratios

---

## ⚙️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/yourusername/vendor-performance-analytics.git
cd vendor-performance-analytics

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate (Windows)

# Install dependencies
pip install -r requirements.txt

# Run ingestion and processing scripts
python ingestion.py
python get_vendor_summary.py

# Open Power BI Desktop and connect to warehouse.db for dashboard building
```

---

## 🗂️ Project Structure

```
vendor-performance-analytics/
├── ingestion.py                  # Ingest CSVs into SQLite DB
├── get_vendor_summary.py         # Compute aggregates and metrics
├── warehouse.db                  # Final SQLite database
├── Exploratory Data Analysis.ipynb
├── Vendor Analytics overview.ipynb
├── *.csv                         # Raw input data files
├── logs/                         # Logging output directory
├── dashboard_screenshot.png      # Power BI visuals
├── workflow_diagram.png          # Project flow image
└── README.md                     # This file
```


