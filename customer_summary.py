import pandas as pd

# Load Data
df = pd.read_excel(
    "data/fake_recommendation_engine_dataset.xlsx"
)

# Create Customer Summary
customer_data = df.groupby("Customer_ID").agg({
    "Amount": ["sum", "mean", "count"]
})

customer_data.columns = [
    "Total_Spend",
    "Average_Spend",
    "Transaction_Count"
]

customer_data.reset_index(inplace=True)

print(customer_data.head())

print("\nNumber of Customers:")
print(customer_data.shape)