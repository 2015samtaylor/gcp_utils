import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from gcp_utils.yoy import load_and_append_previous_year

def make_blob_with_csv(data):
    mock_blob = MagicMock()
    mock_blob.download_as_bytes.return_value = data.encode()
    return mock_blob

def test_load_and_append_previous_year_combines_data():
    # Prepare fake CSVs
    current_csv = 'col1,col2\n1,2\n3,4'
    prev_csv = 'col1,col2\n5,6\n7,8'
    # Mock bucket and blobs
    mock_bucket = MagicMock()
    mock_bucket.blob.side_effect = [make_blob_with_csv(current_csv), make_blob_with_csv(prev_csv)]
    mock_client = MagicMock()
    mock_client.bucket.return_value = mock_bucket
    with patch('gcp_utils.yoy.storage.Client', return_value=mock_client):
        df = load_and_append_previous_year('bucket', 'etl/incoming/2024_file.csv')
        assert len(df) == 4
        assert 'school_year' in df.columns
        assert set(df['school_year']) == {2023, 2024}

def test_load_and_append_previous_year_handles_missing_prev(caplog):
    caplog.set_level("INFO")
    current_csv = 'col1,col2\n1,2\n3,4'
    mock_bucket = MagicMock()
    # First call returns current, second raises exception
    def blob_side_effect(path):
        if '2024' in path:
            return make_blob_with_csv(current_csv)
        else:
            raise Exception('not found')
    mock_bucket.blob.side_effect = blob_side_effect
    mock_client = MagicMock()
    mock_client.bucket.return_value = mock_bucket
    with patch('gcp_utils.yoy.storage.Client', return_value=mock_client):
        df = load_and_append_previous_year('bucket', 'etl/incoming/2024_file.csv')
        assert len(df) == 2
        assert 'school_year' in df.columns
        assert set(df['school_year']) == {2024}
        assert 'Previous year file not found' in caplog.text
