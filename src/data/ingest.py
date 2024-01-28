import logging

import pandas as pd
from google.api_core.exceptions import GoogleAPIError
from google.cloud import bigquery

# https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries


def get_bicycle_data(from_dt: str, to_dt: str) -> None:
    # Create a BigQuery client using the service account path and client options
    client: bigquery.Client = bigquery.Client()

    query_hire: str = f"""
        SELECT *
        FROM `bigquery-public-data.london_bicycles.cycle_hire`
        WHERE start_date BETWEEN '{from_dt}' AND '{to_dt}'
    """

    query_stations: str = """
        SELECT * 
        FROM `bigquery-public-data.london_bicycles.cycle_stations`

    """

    try:
        df_hire: pd.DataFrame = client.query(query_hire).to_dataframe()
        df_stations: pd.DataFrame = client.query(query_stations).to_dataframe()

    except GoogleAPIError as e:
        logging.error(f"An error occurred during querying BigQuery: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

    df_hire.to_parquet(f"data/hire_{from_dt}_{to_dt}.parquet")

    # Convert 'dbdate' columns in df_stations to datetime
    dbdate_columns = df_stations.select_dtypes(include=["dbdate"]).columns
    for column in dbdate_columns:
        df_stations[column] = pd.to_datetime(df_stations[column])

    df_stations.to_parquet("data/stations.parquet")

    print("Data fetched and saved successfully!")


def get_hourly_hire_counts(from_dt: str, to_dt: str) -> None:
    client: bigquery.Client = bigquery.Client()

    query_hourly_hire_counts: str = f"""
        SELECT start_station_name, 
               TIMESTAMP_TRUNC(start_date, HOUR) as start_hour, 
               COUNT(*) as hire_count
        FROM `bigquery-public-data.london_bicycles.cycle_hire`
        WHERE start_date BETWEEN '{from_dt}' AND '{to_dt}'
        GROUP BY start_station_name, start_hour
        ORDER BY start_station_name, start_hour
    """

    try:
        df_hourly_hire_counts: pd.DataFrame = client.query(
            query_hourly_hire_counts
        ).to_dataframe()
    except GoogleAPIError as e:
        logging.error(
            f"An error occurred during querying BigQuery for hourly hire counts: {e}"
        )
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

    df_hourly_hire_counts.to_parquet(
        f"data/hourly_hire_counts_{from_dt}_{to_dt}.parquet"
    )

    print("Hourly hire counts with date fetched and saved successfully!")


if __name__ == "__main__":
    get_bicycle_data("2022-01-01", "2022-12-31")
    get_hourly_hire_counts("2021-01-01", "2099-01-01")
