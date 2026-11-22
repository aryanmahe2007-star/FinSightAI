
import pandas as pd
import numpy as np
from pathlib import Path

# Data storage location
DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_FILE = DATA_DIR / "transactions.csv"


def generate_transactions():

    np.random.seed(42)

    transactions = []

    today = pd.Timestamp.today().normalize()

    income_categories = [
        "Retail Sales",
        "UPI Sales",
        "Cash Sales",
        "Customer Payment"
    ]

    expense_categories = [
        "Inventory Purchase",
        "Rent",
        "Electricity",
        "Staff Salary",
        "Transport",
        "Maintenance",
        "Miscellaneous"
    ]

    payment_modes = ["UPI", "Cash", "Bank Transfer"]

    for day in range(180):

        date = today - pd.Timedelta(days=179-day)

        daily_transactions = np.random.randint(3, 8)

        for _ in range(daily_transactions):

            transaction_type = np.random.choice(
                ["Inflow", "Outflow"],
                p=[0.65, 0.35]
            )

            if transaction_type == "Inflow":

                category = np.random.choice(income_categories)

                amount = round(
                    np.random.uniform(300, 8000), 2
                )

                description = "Customer payment received"

            else:

                category = np.random.choice(expense_categories)

                amount = round(
                    np.random.uniform(200, 6000), 2
                )

                description = "Business expense paid"

            payment_mode = np.random.choice(payment_modes)

            transactions.append({
                "date": date,
                "type": transaction_type,
                "category": category,
                "amount": amount,
                "payment_mode": payment_mode,
                "description": description
            })

    df = pd.DataFrame(transactions)

    return df


def load_transactions():

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():

        df = generate_transactions()

        df.to_csv(DATA_FILE, index=False)

    return pd.read_csv(DATA_FILE, parse_dates=["date"])


if __name__ == "__main__":

    df = load_transactions()

    print("FinSightAI Transaction Database")
    print("--------------------------------")
    print("Total Transactions:", len(df))
    print("\nSample Transactions:")
    print(df.head())

    print("\nTransaction Summary:")
    print(df.groupby("type")["amount"].agg(["count", "sum"]))
