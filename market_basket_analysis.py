import pandas as pd

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# ==================================
# Load Data
# ==================================

df = pd.read_excel(
    "data/fake_recommendation_engine_dataset.xlsx"
)

# ==================================
# Customer vs Product Matrix
# ==================================

basket = pd.crosstab(
    df["Customer_ID"],
    df["Product"]
)

basket = basket > 0

print("\nBasket Shape:")
print(basket.shape)

# ==================================
# Frequent Itemsets
# ==================================

frequent_itemsets = apriori(
    basket,
    min_support=0.001,
    use_colnames=True
)

print("\nFrequent Itemsets Found:")
print(len(frequent_itemsets))

# ==================================
# Multi Product Itemsets
# ==================================

multi_itemsets = frequent_itemsets[
    frequent_itemsets["itemsets"].apply(
        lambda x: len(x) >= 2
    )
]

print("\nItemsets with 2 or More Products:")
print(len(multi_itemsets))

print("\nTop Multi Product Itemsets:")
print(
    multi_itemsets
    .sort_values(
        by="support",
        ascending=False
    )
    .head(20)
)

# ==================================
# Top Frequent Itemsets
# ==================================

print("\nTop Frequent Itemsets:")

print(
    frequent_itemsets
    .sort_values(
        by="support",
        ascending=False
    )
    .head(20)
)

# ==================================
# Association Rules
# ==================================

rules = association_rules(
    frequent_itemsets,
    metric="confidence",
    min_threshold=0.1
)

print("\nRules Found:")
print(len(rules))

# ==================================
# Sort Rules
# ==================================

if len(rules) > 0:

    top_rules = rules.sort_values(
        by=[
            "confidence",
            "lift"
        ],
        ascending=False
    )

    print("\nTop 20 Rules:\n")

    print(
        top_rules[
            [
                "antecedents",
                "consequents",
                "support",
                "confidence",
                "lift"
            ]
        ]
        .head(20)
    )

    top_rules.to_excel(
        "outputs/association_rules.xlsx",
        index=False
    )

    print("\nRules exported successfully!")
    print(
        "File Saved: outputs/association_rules.xlsx"
    )

else:

    print(
        "\nNo Association Rules Found!"
    )

    frequent_itemsets.to_excel(
        "outputs/frequent_itemsets.xlsx",
        index=False
    )

    print(
        "Frequent Itemsets exported instead."
    )