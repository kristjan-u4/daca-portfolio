import pandas as pd
import matplotlib.pyplot as plt
import json

# JSON data
data = [
    {"marketing_channel": "facebook ads", "month": "2024-12", "customer_count": 169},
    {"marketing_channel": "facebook ads", "month": "2023-12", "customer_count": 147},
    {"marketing_channel": "facebook ads", "month": "2023-03", "customer_count": 123},
    {"marketing_channel": "facebook ads", "month": "2024-06", "customer_count": 172},
    {"marketing_channel": "facebook ads", "month": "2024-03", "customer_count": 126},
    {"marketing_channel": "facebook ads", "month": "2023-06", "customer_count": 129},
    {"marketing_channel": "facebook ads", "month": "2023-07", "customer_count": 143},
    {"marketing_channel": "facebook ads", "month": "2024-10", "customer_count": 138},
    {"marketing_channel": "facebook ads", "month": "2024-08", "customer_count": 170},
    {"marketing_channel": "facebook ads", "month": "2024-04", "customer_count": 136},
    {"marketing_channel": "facebook ads", "month": "2023-11", "customer_count": 104},
    {"marketing_channel": "facebook ads", "month": "2023-08", "customer_count": 151},
    {"marketing_channel": "facebook ads", "month": "2025-02", "customer_count": 104},
    {"marketing_channel": "facebook ads", "month": "2024-05", "customer_count": 138},
    {"marketing_channel": "facebook ads", "month": "2023-05", "customer_count": 115},
    {"marketing_channel": "facebook ads", "month": "2023-10", "customer_count": 94},
    {"marketing_channel": "facebook ads", "month": "2023-04", "customer_count": 116},
    {"marketing_channel": "facebook ads", "month": "2023-02", "customer_count": 86},
    {"marketing_channel": "facebook ads", "month": "2024-07", "customer_count": 158},
    {"marketing_channel": "facebook ads", "month": "2024-02", "customer_count": 95},
    {"marketing_channel": "facebook ads", "month": "2024-11", "customer_count": 113},
    {"marketing_channel": "facebook ads", "month": "2024-01", "customer_count": 115},
    {"marketing_channel": "facebook ads", "month": "2024-09", "customer_count": 126},
    {"marketing_channel": "facebook ads", "month": "2023-09", "customer_count": 100},
    {"marketing_channel": "facebook ads", "month": "2025-01", "customer_count": 101},
    {"marketing_channel": "facebook ads", "month": "2023-01", "customer_count": 97}
]

# Convert data to DataFrame
df = pd.DataFrame(data)

# Convert 'month' column to datetime and sort
df["month"] = pd.to_datetime(df["month"])
df = df.sort_values("month")

# Plot the chart
plt.figure(figsize=(12, 6)) # Define figure size
plt.plot(df["month"], df["customer_count"], marker="o", linestyle="-", color="#1877F2", linewidth=2)

# Styling
plt.title("Facebook Ads: Customer Count by Month", fontsize=14, pad=20)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Customer Count", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.xticks(df["month"], df["month"].dt.strftime("%Y-%m"), rotation=45)

# Prevent labels from overlapping
plt.tight_layout() 
# Show the chart
plt.show()
