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
# Discount Rules
# ==================================

discounts = {

    "Premium": 15,
    "Gold": 10,
    "Silver": 5,
    "Bronze": 3

}

# ==================================
# Recommendation Function
# ==================================

def next_best_product(customer_id):

    if customer_id not in customer_products:
        return pd.DataFrame()

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

    if len(recommendations) == 0:
        return pd.DataFrame()

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


# ==================================
# Main Loop
# ==================================

while True:

    customer_id = input(
        "\nEnter Customer ID (or type END to exit): "
    ).strip()

    # Exit
    if customer_id.upper() == "END":

        print("\nSystem Closed Successfully")
        break

    # Customer Validation
    customer = customer_master[
        customer_master["Customer_ID"] == customer_id
    ]

    if customer.empty:

        print("\nCustomer Not Found")
        continue

    # Customer Details
    segment = customer.iloc[0]["Segment"]

    total_spend = customer.iloc[0]["Total_Spend"]

    average_spend = customer.iloc[0]["Average_Spend"]

    transaction_count = customer.iloc[0]["Transaction_Count"]

    purchased_products = list(
        customer_products.get(customer_id, [])
    )

    # ==================================
    # Recommendation
    # ==================================

    recommendations = next_best_product(
        customer_id
    )

    discount = discounts.get(
        segment,
        5
    )

    # ==================================
    # Output
    # ==================================

    print("\n" + "=" * 60)

    print(
        f"\nCustomer ID : {customer_id}"
    )

    print(
        f"Customer Segment : {segment}"
    )

    print(
        f"Total Spend : Rs. {total_spend:,.0f}"
    )

    print(
        f"Average Spend : Rs. {average_spend:,.0f}"
    )

    print(
        f"Transaction Count : {transaction_count}"
    )

    print("\nPurchased Products:")

    for product in purchased_products:

        print(
            f"  - {product}"
        )

    print("\nRecommended Products:")

    if recommendations.empty:

        print(
            "  No recommendations available"
        )

    else:

        for _, row in recommendations.iterrows():

            print(
                f"  - {row['Product']} "
                f"(Score: {row['Score']})"
            )

    print(
        f"\nSuggested Discount : {discount}%"
    )

    print("\nSample Marketing Message:\n")

    if not recommendations.empty:

        top_product = recommendations.iloc[0]["Product"]

        top_score = recommendations.iloc[0]["Score"]

        print(
            f"Dear Customer,\n"
            f"\nBased on your purchase history and "
            f"customers with similar buying patterns, "
            f"we recommend '{top_product}'.\n"
            f"\nRecommendation Confidence Score: "
            f"{top_score}\n"
            f"\nAs a valued {segment} customer, "
            f"you are eligible for an exclusive "
            f"{discount}% discount.\n"
            f"\nThank you for shopping with us."
        )

    print("\n" + "=" * 60)