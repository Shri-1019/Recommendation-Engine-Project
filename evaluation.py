import pandas as pd

# ==================================
# Load Data
# ==================================

df = pd.read_excel(
    "data/fake_recommendation_engine_dataset.xlsx"
)

customer_master = pd.read_excel(
    "outputs/customer_master.xlsx"
)

# ==================================
# Customer Purchase History
# ==================================

customer_products = (
    df.groupby("Customer_ID")["Product"]
    .apply(set)
    .to_dict()
)

# ==================================
# Product Customers
# ==================================

product_customers = (
    df.groupby("Product")["Customer_ID"]
    .apply(set)
    .to_dict()
)

# ==================================
# Recommendation Function
# ==================================

def next_best_product(customer_id):

    purchased = customer_products[customer_id]

    recommendations = {}

    for product in purchased:

        similar_customers = product_customers[product]

        similar_products = df[
            df["Customer_ID"].isin(similar_customers)
        ]["Product"]

        for rec_product in similar_products:

            if rec_product not in purchased:

                recommendations[rec_product] = (
                    recommendations.get(rec_product, 0) + 1
                )

    if len(recommendations) == 0:
        return None

    top_product = max(
        recommendations,
        key=recommendations.get
    )

    return top_product

# ==================================
# Evaluate All Customers
# ==================================

results = []

for customer_id in customer_products.keys():

    recommendation = next_best_product(
        customer_id
    )

    if recommendation:

        segment = customer_master[
            customer_master["Customer_ID"] == customer_id
        ]["Segment"].values[0]

        results.append(
            [
                customer_id,
                segment,
                recommendation
            ]
        )

# ==================================
# Results DataFrame
# ==================================

evaluation = pd.DataFrame(
    results,
    columns=[
        "Customer_ID",
        "Segment",
        "Recommended_Product"
    ]
)

print("\nTotal Recommendations Generated:")
print(len(evaluation))

# ==================================
# Top Recommended Products
# ==================================

print("\nTop 10 Recommended Products:\n")

print(
    evaluation[
        "Recommended_Product"
    ]
    .value_counts()
    .head(10)
)

# ==================================
# Segment Distribution
# ==================================

print("\nRecommendations by Segment:\n")

print(
    evaluation[
        "Segment"
    ]
    .value_counts()
)

# ==================================
# Export
# ==================================

evaluation.to_excel(
    "outputs/recommendation_evaluation.xlsx",
    index=False
)

print(
    "\nEvaluation exported successfully!"
)