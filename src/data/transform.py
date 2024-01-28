import pandas as pd
from tqdm import tqdm


def expand_hourly_counts(hourly_counts: pd.DataFrame) -> pd.DataFrame:
    shape_in = hourly_counts.shape
    expanded_hourly_counts = pd.DataFrame()

    for station in tqdm(
        hourly_counts["start_station_name"].unique(), desc="Expanding hourly counts"
    ):
        station_data = hourly_counts[hourly_counts["start_station_name"] == station]
        min_hour = station_data["start_hour"].min()
        max_hour = station_data["start_hour"].max()
        full_range = pd.date_range(start=min_hour, end=max_hour, freq="h")
        station_data = (
            station_data.set_index("start_hour")
            .reindex(full_range)
            .fillna(0)
            .reset_index()
        )
        station_data["start_station_name"] = station
        expanded_hourly_counts = pd.concat(
            [
                expanded_hourly_counts,
                station_data.rename(columns={"index": "start_hour"}),
            ],
            ignore_index=True,
        )

    expanded_hourly_counts["hire_count"] = expanded_hourly_counts["hire_count"].astype(
        int
    )

    n_additional_rows = expanded_hourly_counts.shape[0] - shape_in[0]
    print(
        f"Added {n_additional_rows} ({100*(expanded_hourly_counts.shape[0]/shape_in[0]):.1f}%)"
    )

    return expanded_hourly_counts


if __name__ == "__main__":
    hourly_counts = pd.read_parquet(
        "data/hourly_hire_counts_2021-01-01_2099-01-01.parquet"
    )
    expanded_hourly_counts = expand_hourly_counts(hourly_counts)
    expanded_hourly_counts.to_parquet("data/expanded_hourly_counts.parquet")

    print("Expanded hourly counts have been saved successfully.")
