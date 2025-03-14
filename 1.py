import pandas as pd
import sqlite3
import os

# Print the current working directory
print("Current working directory:", os.getcwd())

try:
    # Load CSV files
    customers_df = pd.read_csv('customer.csv')
    orders_df = pd.read_csv('orders.csv')

    # Print loaded data
    print("Loaded customers data:")
    print(customers_df.head())

    print("Loaded orders data:")
    print(orders_df.head())

    # Merge data on CustomerID
    merged_df = pd.merge(orders_df, customers_df, on='CustomerID', how='inner')
    print("Merged data:")
    print(merged_df.head())

    # Calculate Total Sales (Quantity * Price)
    merged_df['TotalSales'] = merged_df['Quantity'] * merged_df['Price']
    print("Data with TotalSales:")
    print(merged_df.head())

    # Add Status column (New or Old based on OrderDate)
    merged_df['Status'] = merged_df['OrderDate'].apply(lambda x: 'New' if pd.to_datetime(x) > pd.to_datetime('2024-10-01') else 'Old')
    print("Data with Status:")
    print(merged_df.head())

    # Filter records with TotalSales > $4500
    high_value_orders = merged_df[merged_df['TotalSales'] > 4500]
    print("High value orders:")
    print(high_value_orders)

    # Connect to SQLite database
    conn = sqlite3.connect('ecommerce.db')

    # Create HighValueOrders table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS HighValueOrders (
        OrderID INTEGER,
        CustomerID INTEGER,
        Name TEXT,
        Email TEXT,
        Product TEXT,
        Quantity INTEGER,
        Price REAL,
        OrderDate TEXT,
        TotalSales REAL,
        Status TEXT
    )
    '''
    conn.execute(create_table_query)

    # Load data into the SQLite table
    high_value_orders.to_sql('HighValueOrders', conn, if_exists='replace', index=False)

    # Query and print results
    result = conn.execute('SELECT * FROM HighValueOrders')
    print("HighValueOrders table content:")
    for row in result.fetchall():
        print(row)

    # Close the database connection
    conn.close()

    print("ETL process completed successfully!")

except FileNotFoundError as e:
    print("File not found. Please check the file path and name.")
    print("Error details:", e)
except Exception as e:
    print("An error occurred:", e)