import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download NYC 311 data from Open Data API.")
    parser.add_argument(
        "--start-date",
        default="2019-12-31",
        help="Inclusive lower bound date used in created_date filter.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)

    url = (
        "https://data.cityofnewyork.us/resource/erm2-nwe9.csv"
        f"?$where=created_date>='{args.start_date}T00:00:00'"
        "&$order=created_date%20ASC"
        "&$limit=1000"
    )

    print(f"Downloading data from NYC Open Data API (start date: {args.start_date})...")
    df = pd.read_csv(url)

    output_path = raw_dir / "present.csv"
    df.to_csv(output_path, index=False)

    print(f"Download complete! File saved to {output_path}")


if __name__ == "__main__":
    main()
