import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import uuid
import os


def generate_synthetic_upi_data(
    num_users=1000,
    transactions_per_user=50,
    fraud_ratio=0.02,
    output_path="data/synthetic/upi_transactions.csv"
):
    """
    Generates a synthetic UPI transaction dataset with fraud labels.
    """

    random.seed(42)
    np.random.seed(42)

    records = []
    base_time = datetime.now()

    for user_id in range(1, num_users + 1):
        last_time = base_time

        for _ in range(transactions_per_user):
            transaction_id = str(uuid.uuid4())

            # Time progression
            time_gap = np.random.exponential(scale=300)
            last_time = last_time + timedelta(seconds=time_gap)

            amount = round(np.random.lognormal(mean=5, sigma=1.0), 2)
            location = random.choice(["Bangalore", "Mumbai", "Delhi", "Chennai", "Hyderabad"])
            device_id = f"DEV-{random.randint(1, 5)}"
            merchant_id = f"MER-{random.randint(1, 50)}"

            is_fraud = 0

            # Inject fraud behavior
            if random.random() < fraud_ratio:
                is_fraud = 1
                amount *= random.uniform(5, 15)
                location = random.choice(["Unknown", "Foreign"])
                device_id = f"DEV-{random.randint(10, 20)}"

            records.append([
                user_id,
                transaction_id,
                last_time,
                amount,
                location,
                device_id,
                merchant_id,
                is_fraud
            ])

    df = pd.DataFrame(records, columns=[
        "user_id",
        "transaction_id",
        "timestamp",
        "amount",
        "location",
        "device_id",
        "merchant_id",
        "is_fraud"
    ])

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Dataset generated successfully: {output_path}")
    print(df.head())


if __name__ == "__main__":
    generate_synthetic_upi_data()
