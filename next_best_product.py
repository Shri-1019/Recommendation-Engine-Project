import pandas as pd

# Load Data
df = pd.read_excel(
    "data/fake_recommendation_engine_dataset.xlsx"
)

# Customer Purchase History
customer_products = (
    df.groupby("Customer_ID")["Product"]
    .apply(set)
    .to_dict()
)

# Product Relationships
product_customers = (
    df.groupby("Product")["Customer_ID"]
    .apply(set)
    .to_dict()
)

def next_best_product(customer_id):

    if customer_id not in customer_products:
        return "Customer not found"

    purchased = customer_products[customer_id]

    recommendations = {}

    for product in purchased:

        similar_customers = product_customers[product]

        similar_customer_products = df[
            df["Customer_ID"].isin(similar_customers)
        ]["Product"]

        for rec_product in similar_customer_products:

            if rec_product not in purchased:

                recommendations[rec_product] = (
                    recommendations.get(rec_product, 0) + 1
                )

    recommendations = (
        pd.DataFrame(
            recommendations.items(),
            columns=["Product", "Score"]
        )
        .sort_values(
            by="Score",
            ascending=False
        )
        .head(10)
    )

    return recommendations

customer_id = input(
    "Enter Customer ID: "
)

print("\nPurchased Products:\n")

print(
    customer_products.get(customer_id)
)

print("\nNext Best Products:\n")

print(
    next_best_product(customer_id)
)