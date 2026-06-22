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
# Input Customer
# ==================================

customer_id = input(
    "Enter Customer ID: "
).strip()

if customer_id not in customer_products:

    print("\nCustomer not found!")
    exit()

# ==================================
# Purchases
# ==================================

products = customer_products[customer_id]

if len(products) < 2:

    print(
        "\nCustomer has less than 2 purchases."
    )
    exit()

# ==================================
# Hide Latest Purchase
# ==================================

hidden_product = products[-1]

visible_products = products[:-1]

# ==================================
# Recommendation Logic
# ==================================

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

# ==================================
# Sort Recommendations
# ==================================

top_recommendations = sorted(
    recommendations.items(),
    key=lambda x: x[1],
    reverse=True
)[:10]

# ==================================
# Display
# ==================================

print("\n" + "=" * 60)

print(
    f"\nCustomer ID : {customer_id}"
)

print("\nAll Purchases:")

for p in products:

    print(
        f" - {p}"
    )

print(
    f"\nHidden Product : {hidden_product}"
)

print("\nVisible Products:")

for p in visible_products:

    print(
        f" - {p}"
    )

print("\nTop Recommendations:")

for product, score in top_recommendations:

    print(
        f" - {product} (Score: {score})"
    )

recommended_products = [
    product
    for product, score
    in top_recommendations
]

print("\nResult:")

if hidden_product in recommended_products:

    print(
        f"SUCCESS - Model predicted '{hidden_product}'"
    )

else:

    print(
        f"FAIL - Model missed '{hidden_product}'"
    )

print("\n" + "=" * 60)