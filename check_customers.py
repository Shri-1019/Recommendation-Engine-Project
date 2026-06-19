import pandas as pd

df = pd.read_excel(
    "data/fake_recommendation_engine_dataset.xlsx"
)

print(df["Customer_ID"].head(20))