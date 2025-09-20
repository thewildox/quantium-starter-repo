import pandas as pd
import glob
import os

data_path = "data"

all_files = glob.glob(os.path.join(data_path, "daily_sales_data_*.csv"))

df_list = []
for file in all_files:
    df = pd.read_csv(file)

    # Filter only Pink Morsels
    df = df[df["product"] == "pink morsel"]

    # Create sales column
    df["sales"] = df["quantity"] * df["price"].str.replace("$", "").astype(float)

    # Keep only required fields
    df = df[["sales", "date", "region"]]

    df_list.append(df)

# Combine all into one DataFrame
final_df = pd.concat(df_list, ignore_index=True)

# Save output to CSV
final_df.to_csv("output.csv", index=False)

print("Processing complete! Output saved as output.csv")
