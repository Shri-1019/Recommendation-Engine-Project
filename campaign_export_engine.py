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
# Store Results
# ==================================

campaign_data = []

# ==================================
# Process All Customers
# ==================================

for customer_id in customer_products:

    customer = customer_master[
        customer_master["Customer_ID"] == customer_id
    ]

    if customer.empty:
        continue

    segment = customer.iloc[0]["Segment"]

    purchased = customer_products[
        customer_id
    ]

    recommendations = {}

    # Recommendation Logic

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

    # Skip if no recommendations

    if len(recommendations) == 0:
        continue

    # Top 3 Recommendations

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

    # Store Results

    for row in recommendations.itertuples():

        score = row.Score

        if score >= 70:

            strength = "Strong Match"
            priority = "High"

        elif score >= 40:

            strength = "Moderate Match"
            priority = "Medium"

        else:

            strength = "Weak Match"
            priority = "Low"

        campaign_data.append({

            "Customer_ID":
            customer_id,

            "Segment":
            segment,

            "Recommended_Product":
            row.Product,

            "Score":
            score,

            "Strength":
            strength,

            "Priority":
            priority,

            "Discount":
            discounts[segment]

        })

# ==================================
# Export Results
# ==================================

campaign_df = pd.DataFrame(
    campaign_data
)

campaign_df.to_excel(
    "outputs/recommendation_campaigns.xlsx",
    index=False
)

# ==================================
# Summary
# ==================================

print("\nCampaign Export Summary")
print("-" * 40)

print(
    f"Customers Processed : "
    f"{len(customer_products)}"
)

print(
    f"Recommendations Generated : "
    f"{len(campaign_df)}"
)

print(
    "\nFile Exported Successfully!"
)

print(
    "outputs/recommendation_campaigns.xlsx"
)