# Author: [Camellia]
# Description: Financial report generator with filters and visualizations
# Date: [2025/3/21]

import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from io import StringIO

# --------------------------
# Configuration Parameters
# --------------------------
SAVINGS_RATIO = 0.388  # Savings rate (38.8%)
BASE_SAVINGS = 2000    # Initial savings amount
MONTHLY_GROWTH = 0.05  # 5% monthly compound growth

# --------------------------
# Data Generation
# --------------------------
dates = pd.date_range(start='2023-01-01', periods=12, freq='MS')
savings = [round(BASE_SAVINGS * (1 + MONTHLY_GROWTH)**i, 2) for i in range(12)]
income = [round(s / SAVINGS_RATIO, 2) for s in savings]
expenses = [round(i * (1 - SAVINGS_RATIO), 2) for i in income]

df = pd.DataFrame({
    'Month': [date.strftime('%Y-%m') for date in dates],  # Convert to string for SQL
    'Income': income,
    'Expenses': expenses,
    'Savings': savings
})

# --------------------------
# SQL Query Execution
# --------------------------
# Create in-memory SQLite database
conn = sqlite3.connect(':memory:')
df.to_sql('financial_data', conn, index=False)

# Define SQL query
query = '''
SELECT Month, Income, Expenses, Savings
FROM financial_data
WHERE Income > 7000 AND Savings > 400
ORDER BY Month ASC
'''

# Execute query and load results
filtered_df = pd.read_sql_query(query, conn)
conn.close()

# --------------------------
# Visualization
# --------------------------
plt.figure(figsize=(15, 6))

# Pie Chart
plt.subplot(1, 3, 1)
plt.pie([df.Expenses.sum(), df.Savings.sum()],
        labels=['Expenses', 'Savings'],
        autopct='%1.1f%%',
        colors=['#FF6B6B', '#4ECDC4'])
plt.title('Expense vs Savings Distribution\nMachine: Camellia | IP: 10.50.43.228/16')

# Line Chart
plt.subplot(1, 3, 2)
plt.plot(pd.to_datetime(df['Month']), df['Savings'],  # Convert back to datetime
         marker='o',
         color='#2E86C1',
         linestyle='--')
plt.title('Monthly Savings Trend')
plt.xlabel('Month')
plt.ylabel('Savings ($)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# Filtered Results Table
plt.subplot(1, 3, 3)
plt.axis('off')
plt.table(cellText=filtered_df.values,
          colLabels=filtered_df.columns,
          loc='center',
          cellLoc='center',
          colColours=['#F7DC6F']*4)
plt.title('SQL-Filtered Results:\nIncome > $7000 & Savings > $400')

plt.tight_layout()
plt.savefig('Camellia_financial_report_v4.png', dpi=300)
plt.show()

# --------------------------
# Command-line Output
# --------------------------
print(f"\n{' SQL Query ':=^40}")
print(query)
print(f"\n{' Filtered Results ':=^40}")
print(filtered_df.to_string(index=False))