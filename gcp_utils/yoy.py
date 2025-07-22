from google.cloud import storage
import pandas as pd
from io import BytesIO
import logging

def load_and_append_previous_year(bucket_name, current_blob_path, year_column='school_year'):
    """
    Loads current and previous year CSVs from GCS, appends them into one DataFrame.

    Args:
        bucket_name (str): GCS bucket name.
        current_blob_path (str): Path to current file in GCS (e.g., 'etl/incoming/2024_file.csv').
        year_column (str): Column name to identify year (default: 'school_year').

    Returns:
        pd.DataFrame: Combined DataFrame with both current and previous year data.
    """
    # Auth automatically picked up from GOOGLE_APPLICATION_CREDENTIALS
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    current_year = int(''.join(filter(str.isdigit, current_blob_path)))
    prev_year = current_year - 1
    prev_blob_path = current_blob_path.replace(str(current_year), str(prev_year))

    current_blob = bucket.blob(current_blob_path)
    current_data = pd.read_csv(BytesIO(current_blob.download_as_bytes()))
    current_data[year_column] = current_year

    try:
        prev_blob = bucket.blob(prev_blob_path)
        prev_data = pd.read_csv(BytesIO(prev_blob.download_as_bytes()))
        prev_data[year_column] = prev_year
        combined = pd.concat([prev_data, current_data], ignore_index=True)
    except Exception as e:
        logging.info(f"[INFO] Previous year file not found ({prev_blob_path}): {e}")
        combined = current_data

    return combined
