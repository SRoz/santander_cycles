import pandas as pd
import holidays

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    # Extract date features
    df['hour_of_day'] = df.start_hour.dt.hour
    df['day_of_week'] = df.start_hour.dt.dayofweek
    df['week_of_year'] = df.start_hour.dt.isocalendar().week

    # Add bank holiday feature
    uk_holidays = holidays.UnitedKingdom(years=df.start_hour.dt.year.unique())
    df['bank_holiday'] = df.start_hour.dt.date.isin(uk_holidays.keys())

    return df

if __name__ == "__main__":
    df_hourly_hire = pd.read_parquet('data/expanded_hourly_counts.parquet')
    df_hourly_hire = feature_engineering(df_hourly_hire)
    df_hourly_hire.to_parquet('data/hourly_hire_counts_fe.parquet')
