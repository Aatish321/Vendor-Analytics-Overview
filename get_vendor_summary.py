import sqlite3
import pandas as pd
import logging
import os
from ingestion import ingest_db  # Make sure ingest_db exists in ingestion.py

# Set up logging
logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s = %(levelname)s - %(message)s",
    filemode="a"
)

# Load CSVs into tables if they don't already exist
def load_csv_to_sqlite(conn):
    csv_files = {
        "purchases": "purchases.csv",
        "purchase_prices": "purchase_prices.csv",
        "sales": "sales.csv",
        "vendor_invoice": "vendor_invoice.csv"
    }

    for table_name, file_name in csv_files.items():
        if not table_exists(conn, table_name):
            df = pd.read_csv(file_name)
            df.to_sql(table_name, conn, index=False, if_exists='replace')
            logging.info(f"{table_name} table loaded from {file_name}")
        else:
            logging.info(f"{table_name} table already exists in database")

def table_exists(conn, table_name):
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
    result = conn.execute(query, (table_name,)).fetchone()
    return result is not None

# Create vendor summary
def create_vendor_summary(conn):
    vendor_sales_summary = pd.read_sql_query("""
    WITH FreightSummary AS (
        SELECT 
            VendorNumber,
            SUM(Freight) AS FreightCost
        FROM vendor_invoice
        GROUP BY VendorNumber
    ),
    PurchaseSummary AS (
        SELECT 
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price AS ActualPrice,
            pp.Volume,
            SUM(p.Quantity) AS TotalPurchaseQuantity,
            SUM(p.Dollars) AS TotalPurchaseDollars
        FROM purchases p 
        JOIN purchase_prices pp
            ON p.Brand = pp.Brand
        WHERE p.PurchasePrice > 0
        GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
    ),
    SalesSummary AS (
        SELECT 
            VendorNo,
            Brand,
            SUM(SalesQuantity) AS TotalSalesQuantity,
            SUM(SalesDollars) AS TotalSalesDollars,
            SUM(SalesPrice) AS TotalSalesPrice,
            SUM(ExciseTax) AS TotalExciseTax
        FROM sales
        GROUP BY VendorNo, Brand
    )

    SELECT 
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume,
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        ss.TotalSalesQuantity,
        ss.TotalSalesDollars,
        ss.TotalSalesPrice,
        ss.TotalExciseTax,
        fs.FreightCost
    FROM PurchaseSummary ps
    LEFT JOIN SalesSummary ss
        ON ps.VendorNumber = ss.VendorNo AND ps.Brand = ss.Brand
    LEFT JOIN FreightSummary fs
        ON ps.VendorNumber = fs.VendorNumber
    ORDER BY ps.TotalPurchaseDollars DESC
    """, conn)

    return vendor_sales_summary

# Clean the vendor summary data
def clean_data(df):
    df['Volume'] = df['Volume'].astype('float')
    df.fillna(0, inplace=True)
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = (df['GrossProfit'] / df['TotalSalesDollars']) * 100
    df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity']
    df['SalestoPurchaseRatio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars']

    return df

# Main script
if __name__ == '__main__':
    conn = sqlite3.connect('inventory.db')

    logging.info("Loading CSV data into database...")
    load_csv_to_sqlite(conn)

    logging.info("Creating Vendor Summary...")
    summary_df = create_vendor_summary(conn)
    logging.info(summary_df.head())

    logging.info("Cleaning Data...")
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())

    logging.info("Ingesting Data into vendor_sales_summary table...")
    ingest_db(clean_df, 'vendor_sales_summary', conn)
    logging.info("Ingestion complete.")
