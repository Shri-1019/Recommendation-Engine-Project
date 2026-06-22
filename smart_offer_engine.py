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
    "Premium": 5,
    "Gold": 8,
    "Silver": 10,
    "Bronze": 15
}

# ==================================
# Main Loop
# ==================================

while True:

    customer_id = input(
        "\nEnter Customer ID (or END): "
    ).strip()

    if customer_id.upper() == "END":

        print("\nSystem Closed")
        break

    if customer_id not in customer_products:

        print("\nCustomer not found")
        continue

    # Customer Info

    customer = customer_master[
        customer_master["Customer_ID"] == customer_id
    ]

    segment = customer.iloc[0]["Segment"]

    total_spend = customer.iloc[0]["Total_Spend"]

    purchased = customer_products[
        customer_id
    ]

    # ==================================
    # Recommendation Logic
    # ==================================

    recommendations = {}

    for product in purchased:

        similar_customers = (
            product_customers.get(
                product,
                set()
            )
        )

        similar_products = df[
            df["Customer_ID"].isin(
                similar_customers
            )
        ]["Product"]

        for rec_product in similar_products:

            if rec_product not in purchased:

                recommendations[
                    rec_product
                ] = (
                    recommendations.get(
                        rec_product,
                        0
                    ) + 1
                )

    recommendations = (
        pd.DataFrame(
            recommendations.items(),
            columns=[
                "Product",
                "Score"
            ]
        )
        .sort_values(
            by="Score",
            ascending=False
        )
        .head(3)
    )

    # ==================================
    # Output
    # ==================================

    print("\n" + "=" * 60)

    print(
        f"\nCustomer ID : {customer_id}"
    )

    print(
        f"Segment : {segment}"
    )

    print(
        f"Total Spend : Rs. {total_spend:,.0f}"
    )

    print("\nTop 3 Recommendations\n")

    for i, row in enumerate(
        recommendations.itertuples(),
        start=1
    ):

        score = row.Score

        if score >= 70:

            priority = "High"
            strength = "Strong Match"

        elif score >= 40:

            priority = "Medium"
            strength = "Moderate Match"

        else:

            priority = "Low"
            strength = "Weak Match"

        print(
            f"{i}. {row.Product}"
        )

        print(
            f"   Score : {score}"
        )

        print(
            f"   Strength : {strength}"
        )

        print(
            f"   Priority : {priority}"
        )

        print(
            f"   Discount : {discounts[segment]}%"
        )

        print()

    # ==================================
    # Campaign Message
    # ==================================

    products = list(
        recommendations["Product"]
    )

    print(
        "Campaign Message\n"
    )

    print(
        f"Dear Customer,\n"
    )

    print(
        "Based on your purchase history, "
        "we have selected products that "
        "may interest you.\n"
    )

    print(
        f"Recommended Products: "
        f"{', '.join(products)}\n"
    )

    print(
        f"As a valued {segment} customer, "
        f"you are eligible for an "
        f"exclusive {discounts[segment]}% "
        f"discount.\n"
    )

    print(
        "Thank you for shopping with us."
    )

    print("\n" + "=" * 60)