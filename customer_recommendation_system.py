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
# Recommendation Map
# ==================================

recommendation_map = {

    "Gaming Laptop": [
        "Wireless Mouse",
        "Laptop Bag",
        "USB Hub"
    ],

    "Wireless Mouse": [
        "Mouse Pad"
    ],

    "Samsung TV": [
        "Soundbar",
        "Wall Mount"
    ],

    "Soundbar": [
        "Extended Warranty"
    ],

    "Refrigerator": [
        "Microwave",
        "Extended Warranty"
    ],

    "Microwave": [
        "Dining Table"
    ]
}

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
        "\nEnter Customer ID (or type END to exit): "
    ).strip()

    # Exit System
    if customer_id.upper() == "END":

        print("\nSystem Closed Successfully")
        break

    # Find Customer
    customer = customer_master[
        customer_master["Customer_ID"] == customer_id
    ]

    # Customer Not Found
    if customer.empty:

        print("\nCustomer Not Found")
        continue

    # Customer Segment
    segment = customer.iloc[0]["Segment"]

    total_spend = customer.iloc[0]["Total_Spend"]

    average_spend = customer.iloc[0]["Average_Spend"]

    transaction_count = customer.iloc[0]["Transaction_Count"]

    # Purchase History
    purchased_products = list(
        df[
            df["Customer_ID"] == customer_id
        ]["Product"].unique()
    )

    # Recommendation Logic
    recommendations = []

    for product in purchased_products:

        if product in recommendation_map:

            for item in recommendation_map[product]:

                if item not in purchased_products:

                    recommendations.append(item)

    recommendations = list(
        set(recommendations)
    )

    # Discount
    discount = discounts.get(
        segment,
        10
    )

    # ==================================
    # Output
    # ==================================

    print("\n" + "=" * 50)

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

    if recommendations:

        for product in recommendations:

            print(
                f"  - {product}"
            )

    else:

        print(
            "  No recommendations available"
        )

    print(
        f"\nSuggested Discount : {discount}%"
    )

    print("\nSample Marketing Message:\n")

    if recommendations:

        print(
            f"Dear Customer,\n"
            f"\nBased on your previous purchases, "
            f"we believe you may be interested in "
            f"{recommendations[0]}.\n"
            f"\nAs a valued {segment} customer, "
            f"we are pleased to offer you "
            f"{discount}% OFF on this product.\n"
            f"\nThank you for shopping with us."
        )

    print("\n" + "=" * 50)