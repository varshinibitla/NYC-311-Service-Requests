import pandas as pd
from pathlib import Path

RAW = Path("data/raw/present.csv")
CLEAN = Path("data/clean/present.csv")

print("Loading dataset...")
df = pd.read_csv(RAW, low_memory=False)

# Select only the columns your PPT requires
cols = ["complaint_type", "borough", "created_date", "latitude", "longitude", "descriptor"]
df = df[cols]

# Drop rows missing essential fields
df = df.dropna(subset=["complaint_type", "borough", "created_date"])

# Convert created_date to datetime
df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
df = df.dropna(subset=["created_date"])

# Remove invalid coordinates
df = df[(df["latitude"] != 0) & (df["longitude"] != 0)]

# Save cleaned file
df.to_csv(CLEAN, index=False)
print("Cleaned dataset saved:", CLEAN)
