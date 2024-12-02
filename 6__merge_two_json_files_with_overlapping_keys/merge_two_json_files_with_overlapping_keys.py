# -*- coding: utf-8 -*-
"""
Problem 6: Merge Two JSON Files with Overlapping Keys


Task: 
    Given two JSON files, merge them into one. 
    If keys overlap, values from the second file should overwrite the ones from the first file.


Input:

File 1:
[
  {"user_id": 1, "name": "Alice", "age": 25},
  {"user_id": 2, "name": "Bob"}
]

File 2:
[
  {"user_id": 1, "age": 26, "city": "New York"},
  {"user_id": 3, "name": "Charlie", "city": "San Francisco"}
]


Output:
[
  {"user_id": 1, "name": "Alice", "age": 26, "city": "New York"},
  {"user_id": 2, "name": "Bob"},
  {"user_id": 3, "name": "Charlie", "city": "San Francisco"}
]




Created on Mon Dec  2 15:06:17 2024

@author: enokj
"""
import pandas as pd
import os
import logging
import json

def merge_two_json_files_with_overlapping_keys(file1: str, file2: str, output_file: str) -> None:
    """
    Merges two JSON files with overlaping keys.
    
    
    Args:
        file1 (str): Path to first JSON file.
        file2 (str): Path to second JSON file.
        output_file (str): Path to output JSON file. 
        
    Returns:
        pd.DataFrame: DataFrame containing the result merge os JSON files
    """

    if not os.path.exists(file1) or not os.path.exists(file2):
        raise FileNotFoundError(f"File '{file1}' and/or '{file2} does not exist.'")
        
    try:
        with open(file1, 'r') as f1:
            data1 = json.load(f1)
        with open(file2, 'r') as f2:
            data2 = json.load(f2)

        dict1 = {item["user_id"]: item for item in data1}
        dict2 = {item["user_id"]: item for item in data2}
        
        print("\n\n")
        print(dict1)
        print(dict2)

        # Perform a deep merge for overlapping keys
        merged_dict = {}
        all_keys = set(dict1.keys()).union(dict2.keys())
        for key in all_keys:
            merged_dict[key] = merge_dicts(dict1.get(key, {}), dict2.get(key, {}))

        print("\n\n")
        print(merged_dict)

        merged_data = list(merged_dict.values())
        print("\n\n")
        print(merged_data)

        with open(output_file, 'w') as output:
            json.dump(merged_data, output, indent=4)

    except FileNotFoundError as e:
        logging.error(f"File not found error -> {e}", e)
        raise e
    except Exception as e:
        logging.error(f"Unknown error -> {e}", e)
        raise e    
    


def merge_dicts(dict1, dict2):
    """
    Deep merge two dictionaries. If a key exists in both dictionaries:
    - If the value is a dictionary, recursively merge it.
    - Otherwise, overwrite the value with the one from dict2.

    Args:
        dict1 (dict): The first dictionary.
        dict2 (dict): The second dictionary.

    Returns:
        dict: The merged dictionary.
    """
    merged = dict1.copy()
    for key, value in dict2.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_dicts(merged[key], value)  # Recursive merge
        else:
            merged[key] = value  # Overwrite or add new key
    return merged

    
merge_two_json_files_with_overlapping_keys('file1.json', 'file2.json', 'output.json')
    
output_df = pd.read_json('output.json')
print(output_df)
    