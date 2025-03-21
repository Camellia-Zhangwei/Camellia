# Author: [Camellia]
# Description: Financial report generator with filters and visualizations
# Date: [2025/3/21]

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --------------------------
# Configuration Parameters
# --------------------------
SAVINGS_RATIO = 0.388  # Savings rate (38.8%)
BASE_SAVINGS = 2000    # Initial savings amount
MONTHLY_GROWTH = 0.05  # Monthly growth rate (5%)
MONTHS = 12            # Number of months to generate

# --------------------------
# Data Generation
# --------------------------

# Generate monthly timestamps
dates = pd.date_range(start='2023-01-01', periods=MONTHS, freq='MS')
months = [date.strftime('%Y-%m') for date in dates]

# Calculate compounded savings
savings = [round(BASE_SAVINGS * (1 + MONTHLY_GROWTH)**i, 2) for i in range(MONTHS)]

# Derive income and expenses
income = [round(s / SAVINGS_RATIO, 2) for s in savings]
expenses = [round(i * (1 - SAVINGS_RATIO), 2) for i in income]

# Create DataFrame
df = pd.DataFrame({
    'Month': dates,
    'Income': income,
    'Expenses': expenses,
    'Savings': savings
})

# --------------------------
# Data Filtering
# --------------------------
filter_condition = (df['Income'] > 7000) & (df['Savings'] > 400)
filtered_df = df[filter_condition].sort_values('Month')

# --------------------------
# Visualization Settings
# --------------------------
plt.figure(figsize=(18, 6))

# Pie Chart (Full Dataset)
plt.subplot(1, 3, 1)
plt.pie([df.Expenses.sum(), df.Savings.sum()],
        labels=['Expenses', 'Savings'],
        autopct='%1.1f%%',
        colors=['#FF6B6B', '#4ECDC4'])
# 在图表中添加机器信息的代码片段示例（插入到绘图代码中）
plt.title('Expense vs Savings Distribution\nMachine: Camellia | IP: 10.50.43.228/16')

# Line Chart (Savings Trend)
plt.subplot(1, 3, 2)
plt.plot(df['Month'], df['Savings'],
        marker='o',
        color='#2E86C1',
        linestyle='--')
plt.title('Monthly Savings Trend')
plt.xlabel('Month')
plt.ylabel('Amount ($)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# Filtered Results Table
plt.subplot(1, 3, 3)
plt.axis('off')
table_data = filtered_df[['Month', 'Income', 'Savings']]
table_data['Month'] = table_data['Month'].dt.strftime('%b %Y')
plt.table(cellText=table_data.values,
         colLabels=table_data.columns,
         loc='center',
         cellLoc='center',
         colColours=['#F7DC6F']*3)
plt.title('Filtered Results:\nIncome > $7000 & Savings > $400')

plt.tight_layout()
plt.savefig('camellia_financial_report_v3.png', dpi=300)
plt.show()

# --------------------------
# Command-line Output
# --------------------------
print(f"\n{' Machine Info ':=^40}")
print(f"Name: camellia\nIP: 10.50.43.228/16\n{' Filter Criteria ':=^40}")
print("SELECT Month, Income, Expenses, Savings")
print("FROM financial_data")
print("WHERE Income > 7000 AND Savings > 400")
print("ORDER BY Month ASC\n")
print(filtered_df.to_string(index=False, formatters={
    'Month': lambda x: x.strftime('%Y-%m'),
    'Income': lambda x: f"${x:,.2f}",
    'Savings': lambda x: f"${x:,.2f}"
}))