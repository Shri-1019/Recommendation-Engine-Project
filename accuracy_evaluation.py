import pandas as pd

# ==================================
# Load Data
# ==================================

df = pd.read_excel(
    "data/fake_recommendation_engine_dataset.xlsx"
)

# ==================================
# Customer Purchase History
# ==================================

customer_products = (
    df.groupby("Customer_ID")["Product"]
    .apply(list)
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
# Accuracy Counters
# ==================================

total_customers = 0

correct_predictions = 0

results = []

# ==================================
# Evaluate Each Customer
# ==================================

for customer_id, products in customer_products.items():

    # Need at least 2 products
    if len(products) < 2:
        continue

    total_customers += 1

    # Hide latest purchased product

    hidden_product = products[-1]

    visible_products = products[:-1]

    recommendations = {}

    for product in visible_products:

        similar_customers = product_customers.get(
            product,
            set()
        )

        similar_products = df[
            df["Customer_ID"].isin(
                similar_customers
            )
        ]["Product"]

        for rec_product in similar_products:

            if rec_product not in visible_products:

                recommendations[rec_product] = (
                    recommendations.get(
                        rec_product,
                        0
                    ) + 1
                )

    if len(recommendations) == 0:
        continue

    recommended_products = sorted(
        recommendations,
        key=recommendations.get,
        reverse=True
    )[:10]

    hit = hidden_product in recommended_products

    if hit:
        correct_predictions += 1

    results.append([
        customer_id,
        hidden_product,
        hit
    ])

# ==================================
# Accuracy
# ==================================

accuracy = (
    correct_predictions /
    total_customers
) * 100

print("\nRecommendation Accuracy")

print("-" * 40)

print(
    f"Customers Evaluated : "
    f"{total_customers}"
)

print(
    f"Correct Predictions : "
    f"{correct_predictions}"
)

print(
    f"Accuracy : "
    f"{accuracy:.2f}%"
)

# ==================================
# Export
# ==================================

results_df = pd.DataFrame(
    results,
    columns=[
        "Customer_ID",
        "Hidden_Product",
        "Predicted_Correctly"
    ]
)

results_df.to_excel(
    "outputs/recommendation_accuracy.xlsx",
    index=False
)

print(
    "\nAccuracy report exported successfully!"
)