import pandas as pd
import matplotlib.pyplot as plt


csv_file = "air_quality.csv"


df = pd.read_csv(csv_file)

if "Date" not in df.columns:
    if "date_local" in df.columns:
        df["Date"] = df["date_local"]
    else:
        raise ValueError("CSV has no Date column.")

if "PM2.5" not in df.columns:
    if "arithmetic_mean_a" in df.columns:
        df["PM2.5"] = df["arithmetic_mean_a"]
    else:
        raise ValueError("CSV has no PM2.5 column.")

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["PM2.5"] = pd.to_numeric(df["PM2.5"], errors="coerce")

cleaned_df = df[["Date", "PM2.5"]].dropna()
cleaned_df = cleaned_df.sort_values("Date")

mean_pm25 = cleaned_df["PM2.5"].mean()
min_pm25 = cleaned_df["PM2.5"].min()
max_pm25 = cleaned_df["PM2.5"].max()

cleaned_df["Month"] = cleaned_df["Date"].dt.to_period("M").astype(str)
monthly_avg = cleaned_df.groupby("Month")["PM2.5"].mean().reset_index()

print("Air Quality Analysis")
print("--------------------")
print(f"Overall mean PM2.5: {mean_pm25:.2f}")
print(f"Minimum PM2.5: {min_pm25:.2f}")
print(f"Maximum PM2.5: {max_pm25:.2f}")
print()
print("Monthly Average PM2.5")
print("---------------------")
print(monthly_avg.to_string(index=False))

cleaned_df.to_csv("cleaned_air_quality.csv", index=False)

plt.figure(figsize=(10, 5))
plt.plot(cleaned_df["Date"], cleaned_df["PM2.5"], color="blue")
plt.title("PM2.5 Over Time")
plt.xlabel("Date")
plt.ylabel("PM2.5")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("pm25_over_time.png")

plt.figure(figsize=(12, 5))
positions = range(len(monthly_avg))
tick_step = 3

plt.bar(positions, monthly_avg["PM2.5"], color="green")
plt.title("Monthly Average PM2.5")
plt.xlabel("Month")
plt.ylabel("Average PM2.5")
plt.xticks(
    positions[::tick_step],
    monthly_avg["Month"][::tick_step],
    rotation=45,
    ha="right"
)
plt.tight_layout()
plt.savefig("monthly_avg_pm25.png")

plt.show()
