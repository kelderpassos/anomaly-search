import pandas as pd


df_checkout_1 = pd.read_csv("uploads/checkout_1.csv")

print(df_checkout_1)
print(df_checkout_1.describe())


anomaly_checkout_1 = df_checkout_1.loc[
    (df_checkout_1["time"] == "06h")
    | (df_checkout_1["time"] == "07h")
    | (df_checkout_1["time"] == "08h")
    | (df_checkout_1["time"] == "09h"),
    ["time", "today", "yesterday", "same_day_last_week"],
]

print(anomaly_checkout_1)


df_checkout_2 = pd.read_csv("data/checkout_2.csv")

anomaly_checkout_morning = df_checkout_2.loc[
    (df_checkout_2["time"] == "07h")
    | (df_checkout_2["time"] == "08h")
    | (df_checkout_2["time"] == "09h"),
    ["time", "today", "yesterday"],
]

anomaly_checkout_afternoon = df_checkout_2.loc[
    (df_checkout_2["time"] == "15h")
    | (df_checkout_2["time"] == "16h")
    | (df_checkout_2["time"] == "17h")
    | (df_checkout_2["time"] == "18h"),
    ["time", "today", "yesterday"],
]

print(anomaly_checkout_morning)
print(anomaly_checkout_afternoon)
