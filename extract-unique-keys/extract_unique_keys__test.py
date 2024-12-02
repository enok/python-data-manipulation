# -*- coding: utf-8 -*-
"""
Tests extract_unique_keys functions

Created on Mon Dec  2 11:04:30 2024

@author: enokj
"""
import unittest
import os
import json
import logging
from extract_unique_keys import unique_keys

class TestExtractUniqueKeys(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.file_name = "valid_input_data.json"
        self.invalid_file_name = "invalid_file.json"
        
        # Setup test data as JSON strings
        self.valid_input_data = json.loads("""
        [
          {"user_id": 1, "activity": {"type": "login", "time": "2024-11-01T08:00:00"}},
          {"user_id": 2, "activity": {"type": "click", "time": "2024-11-01T08:05:00", "details": {"button": "submit"}}},
          {"user_id": 3, "activity": {"type": "logout", "time": "2024-11-01T08:10:00"}}
        ]
        """)
        self.valid_output_data = json.loads("""
        ["activity", "button", "details", "time", "type", "user_id"]
        """)

        self.empty_input_data = json.loads("""[]""")
        self.empty_output_data = json.loads("""[]""")


    def test_extract_unique_keys_not_found_input_file(self):
        with self.assertRaises(FileNotFoundError) as ctx:
            unique_keys('')
        self.assertEqual("File '' not found.", str(ctx.exception))
        
    
    def test_extract_unique_keys_valid_data(self):
        # Save valid data to a temporary JSON file
        with open(self.file_name, "w") as f:
            json.dump(self.valid_input_data, f)
        
        # Run the function
        result = unique_keys(self.file_name)
        
        # Compare results
        self.assertEqual(result, self.valid_output_data)
        

    def test_extract_unique_keys_nested_data(self):
        nested_data = json.loads("""
        [
            {"user_id": 1, "activity": {"type": "login", "metadata": {"ip": "192.168.0.1", "device": "mobile"}}},
            {"user_id": 2, "activity": {"type": "logout", "metadata": {"ip": "192.168.0.2", "device": "desktop"}}}
        ]
        """)
        expected_output = ["activity", "device", "ip", "metadata", "type", "user_id"]

        with open(self.file_name, "w") as f:
            json.dump(nested_data, f)

        result = unique_keys(self.file_name)

        self.assertEqual(result, expected_output)

    def test_extract_unique_keys_empty_data(self):
        with open(self.file_name, "w") as f:
            json.dump(self.empty_input_data, f)
    
        result = unique_keys(self.file_name)
    
        self.assertEqual(result, self.empty_output_data)


    def test_extract_unique_keys_invalid_json_format(self):
        with self.assertRaises(ValueError) as ctx:
            unique_keys(self.invalid_file_name)
        self.assertEqual("Invalid JSON format.", str(ctx.exception))


    @classmethod
    def tearDownClass(self):
        try:
            os.remove(self.file_name)
        except FileNotFoundError as e:
            logging.warning(f"File not found: {e}")

if __name__ == "__main__":
    unittest.main()