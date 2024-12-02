# -*- coding: utf-8 -*-
"""
Problem 5: Extract Unique Keys

Task: 
    You are given a hierarchical dataset of user activity. 
    Extract all unique keys present in the dataset.


Input JSON:
[
  {"user_id": 1, "activity": {"type": "login", "time": "2024-11-01T08:00:00"}},
  {"user_id": 2, "activity": {"type": "click", "time": "2024-11-01T08:05:00", "details": {"button": "submit"}}},
  {"user_id": 3, "activity": {"type": "logout", "time": "2024-11-01T08:10:00"}}
]

Expected Output:
["activity", "button", "details", "time", "type", "user_id"]



Created on Mon Dec  2 11:04:30 2024

@author: enokj
"""
import os
import logging
import pandas as pd
import json

logging.basicConfig(level=logging.INFO)


def unique_keys(file: str) -> list:
    """
    Extracts unique keys from a JSON file.
    
    
    Args:
        - file (str): Path to JSON file.
    
    Returns:
        - list: List of unique keys extracted from JSON file
    """

    if not os.path.exists(file):
        raise FileNotFoundError(f"File '{file}' not found.")
    

    try:
        with open(file) as f:
            data = json.load(f)
            df = pd.json_normalize(data)
        
        logging.debug(f"Flattened DataFrame columns: {df.columns.tolist()}")

        result = set()
        for col in df.columns:
            keys = col.split('.')
            result.update(keys)
        
        result = sorted(result)
        logging.debug(f"Extracted unique keys: {result}")
        return result

    except FileNotFoundError as e:
        logging.error(f"File not found error -> {e}")
        raise e
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON format -> {e}")
        raise ValueError("Invalid JSON format.")
    except Exception as e:
        logging.error(f"Unexpected error -> {e}")
        raise e



# Example usage
if __name__ == "__main__":
    input_file = 'file.json'

    logging.info("\n\nExample of usage")
    logging.info("-----------------------------------------------------")
    output = unique_keys(input_file)
    if output is not None:
        print(output)
