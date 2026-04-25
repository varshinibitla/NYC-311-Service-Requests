import uuid
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "clean" / "311_clean_2020_present.csv"
OUTPUTS_DIR = BASE_DIR / "outputs"


def write_output(df: pd.DataFrame, folder_name: str) -> None:
    out_dir = OUTPUTS_DIR / folder_name
    out_dir.mkdir(parents=True, exist_ok=True)

    for old in out_dir.glob("*"):
        if old.is_file():
            old.unlink()

    part_name = f"part-00000-{uuid.uuid4()}-c000.csv"
    df.to_csv(out_dir / part_name, index=False)
    (out_dir / "_SUCCESS").write_text("", encoding="utf-8")


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Clean dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH, low_memory=False)

    top_complaints = (
        df.groupby("complaint_type", dropna=False)
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(10)
    )
    write_output(top_complaints, "top_complaints")

    borough_counts = (
        df.groupby("borough", dropna=False)
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    write_output(borough_counts, "borough_counts")

    dt = pd.to_datetime(df["created_date"], errors="coerce")
    monthly_trend = (
        pd.DataFrame({"year": dt.dt.year, "month": dt.dt.month})
        .dropna()
        .astype({"year": int, "month": int})
        .groupby(["year", "month"], dropna=False)
        .size()
        .reset_index(name="count")
        .sort_values(["year", "month"], ascending=[True, True])
    )
    write_output(monthly_trend, "monthly_trend")

    high_volume_boroughs = borough_counts.head(10)
    write_output(high_volume_boroughs, "high_volume_boroughs")

    hourly_trend = (
        pd.DataFrame({"hour": dt.dt.hour})
        .dropna()
        .astype({"hour": int})
        .groupby("hour", dropna=False)
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    write_output(hourly_trend, "hourly_trend")

    print("Analysis completed successfully.")


if __name__ == "__main__":
    main()
