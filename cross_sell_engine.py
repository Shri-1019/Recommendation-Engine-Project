import pandas as pd

# Load data
df = pd.read_excel(
    "data/fake_recommendation_engine_dataset.xlsx"
)

# Build customer-product matrix
customer_products = df.groupby("Customer_ID")["Product"].apply(list)

# Recommendation function
def recommend_for_product(product):

    customers = customer_products[
        customer_products.apply(lambda x: product in x)
    ]

    recommendations = []

    for products in customers:
        recommendations.extend(products)

    recommendations = pd.Series(recommendations)

    recommendations = recommendations[
        recommendations != product
    ]

    return recommendations.value_counts().head(10).reset_index()

# Test
product_name = input("Enter Product: ")

print("\nRecommended Products:\n")

print(
    recommend_for_product(product_name)
)