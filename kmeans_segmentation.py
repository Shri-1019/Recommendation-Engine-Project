import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load Data
df = pd.read_excel(
    "data/fake_recommendation_engine_dataset.xlsx"
)

# Customer Summary
customer_data = df.groupby("Customer_ID").agg({
    "Amount": ["sum", "mean", "count"]
})

customer_data.columns = [
    "Total_Spend",
    "Average_Spend",
    "Transaction_Count"
]

customer_data.reset_index(inplace=True)

# Features for ML
X = customer_data[
    [
        "Total_Spend",
        "Average_Spend",
        "Transaction_Count"
    ]
]

# Scale Data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# KMeans
kmeans = KMeans(
    n_clusters=4,
    random_state=42
)

customer_data["Cluster"] = kmeans.fit_predict(
    X_scaled
)

print(
    customer_data[
        [
            "Customer_ID",
            "Total_Spend",
            "Transaction_Count",
            "Cluster"
        ]
    ].head(20)
)
print("\nCluster Summary")

print(
    customer_data
    .groupby("Cluster")
    [
        [
            "Total_Spend",
            "Average_Spend",
            "Transaction_Count"
        ]
    ]
    .mean()
)