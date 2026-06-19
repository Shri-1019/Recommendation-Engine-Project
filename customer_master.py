import pandas as pd

# ----------------------------
# Customer Segmentation Logic
# ----------------------------
def get_segment(total_spend):

    if total_spend >= 500000:
        return "Premium"

    elif total_spend >= 250000:
        return "Gold"

    elif total_spend >= 100000:
        return "Silver"

    else:
        return "Bronze"


# ----------------------------
# Load Data
# ----------------------------
df = pd.read_excel(
    "data/fake_recommendation_engine_dataset.xlsx"
)

# ----------------------------
# Create Customer Summary
# ----------------------------
customer_data = df.groupby("Customer_ID").agg({
    "Amount": ["sum", "mean", "count"]
})

# Rename Columns
customer_data.columns = [
    "Total_Spend",
    "Average_Spend",
    "Transaction_Count"
]

# Convert Customer_ID back to column
customer_data.reset_index(inplace=True)

# ----------------------------
# Assign Customer Segment
# ----------------------------
customer_data["Segment"] = customer_data[
    "Total_Spend"
].apply(get_segment)

# ----------------------------
# Display Results
# ----------------------------
print("\nCustomer Summary:\n")

print(
    customer_data[
        [
            "Customer_ID",
            "Total_Spend",
            "Average_Spend",
            "Transaction_Count",
            "Segment"
        ]
    ].head(20)
)

print("\nTotal Customers:")

print(customer_data.shape[0])

# ----------------------------
# Export to Excel
# ----------------------------
customer_data.to_excel(
    "outputs/customer_master.xlsx",
    index=False
)

print("\nCustomer Master Created Successfully!")

print(
    "File Saved: outputs/customer_master.xlsx"
)