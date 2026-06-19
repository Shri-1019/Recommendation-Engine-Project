import pandas as pd

df = pd.read_excel(
    "data/fake_recommendation_engine_dataset.xlsx"
)

recommendations = {
    "Airline Ticket": [
        "Hotel Booking",
        "Travel Insurance"
    ],

    "Laptop": [
        "Wireless Mouse",
        "Laptop Bag"
    ],

    "Smart TV": [
        "Soundbar",
        "Home Theatre"
    ]
}

product = input(
    "Enter purchased product: "
)

print(
    recommendations.get(
        product,
        ["No recommendation found"]
    )
)
