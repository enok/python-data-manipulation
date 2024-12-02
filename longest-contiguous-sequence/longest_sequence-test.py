# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 00:03:51 2024

@author: enokj
"""
import unittest
import pandas as pd
import json
from longest_sequence import longest_contiguous_sequence, extract_longest_sequence


class TestLongestContiguousSequence(unittest.TestCase):
    def setUp(self):
        # Setup test data as JSON strings
        self.valid_data = json.loads("""
        [
            {"user_id": 1, "login_date": "2024-11-01T08:00:00"},
            {"user_id": 1, "login_date": "2024-11-02T09:00:00"},
            {"user_id": 1, "login_date": "2024-11-04T10:30:00"},
            {"user_id": 1, "login_date": "2024-11-05T11:00:00"},
            {"user_id": 2, "login_date": "2024-11-01T12:00:00"},
            {"user_id": 2, "login_date": "2024-11-02T13:00:00"},
            {"user_id": 2, "login_date": "2024-11-03T14:00:00"},
            {"user_id": 2, "login_date": "2024-11-05T15:00:00"},
            {"user_id": 3, "login_date": "2024-11-01T08:00:00"},
            {"user_id": 3, "login_date": "2024-11-03T09:00:00"},
            {"user_id": 3, "login_date": "2024-11-04T10:00:00"},
            {"user_id": 3, "login_date": "2024-11-05T11:00:00"}
        ]
        """)
        self.empty_data = json.loads("""[]""")
        self.missing_login_dates = json.loads("""
        [
            {"user_id": 4},
            {"user_id": 5, "login_date": "2024-11-05T11:00:00"}
        ]
        """)

    def test_longest_contiguous_sequence_valid_data(self):
        # Save valid data to a temporary JSON file
        file_name = "test_valid.json"
        with open(file_name, "w") as f:
            json.dump(self.valid_data, f)

        # Run the function
        result = longest_contiguous_sequence(file_name)

        # Expected result
        expected = pd.DataFrame([
            {"user_id": 1, "longest_sequence": 2, "start_date": "2024-11-01", "end_date": "2024-11-02"},
            {"user_id": 2, "longest_sequence": 3, "start_date": "2024-11-01", "end_date": "2024-11-03"},
            {"user_id": 3, "longest_sequence": 3, "start_date": "2024-11-03", "end_date": "2024-11-05"}
        ])

        # Compare DataFrame results
        pd.testing.assert_frame_equal(result, expected)

    def test_longest_contiguous_sequence_empty_data(self):
        # Save empty data to a temporary JSON file
        file_name = "test_empty.json"
        with open(file_name, "w") as f:
            json.dump(self.empty_data, f)

        # Run the function
        result = longest_contiguous_sequence(file_name)

        # Expected result: an empty DataFrame
        expected = pd.DataFrame(columns=["user_id", "longest_sequence", "start_date", "end_date"])
        pd.testing.assert_frame_equal(result, expected)

    def test_extract_longest_sequence_with_missing_dates(self):
        # Convert missing login dates into a DataFrame
        group = pd.DataFrame(self.missing_login_dates)
        result = extract_longest_sequence(4, group)

        # Expected result
        expected = {
            "user_id": 4,
            "longest_sequence": 0,
            "start_date": None,
            "end_date": None,
        }
        self.assertEqual(result, expected)

    def test_extract_longest_sequence_with_valid_dates(self):
        # Prepare a valid group
        group = pd.DataFrame([
            {"login_date": pd.to_datetime("2024-11-01").date()},
            {"login_date": pd.to_datetime("2024-11-02").date()},
            {"login_date": pd.to_datetime("2024-11-04").date()}
        ])
        result = extract_longest_sequence(1, group)

        # Expected result
        expected = {
            "user_id": 1,
            "longest_sequence": 2,
            "start_date": "2024-11-01",
            "end_date": "2024-11-02",
        }
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()


