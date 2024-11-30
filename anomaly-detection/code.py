# -*- coding: utf-8 -*-
"""
Problem 3: Anomaly Detection

Detect duplicate user registrations. 
A registration is considered a duplicate if the same user_id appears with the same email.

Input:

[
  {"user_id": 1, "email": "user1@example.com", "timestamp": "2024-11-01T08:00:00"},
  {"user_id": 2, "email": "user2@example.com", "timestamp": "2024-11-01T08:05:00"},
  {"user_id": 1, "email": "user1@example.com", "timestamp": "2024-11-01T08:10:00"},
  {"user_id": 3, "email": "user3@example.com", "timestamp": "2024-11-01T08:15:00"},
  {"user_id": 2, "email": "user2@example.com", "timestamp": "2024-11-01T08:20:00"}
]


Output:

[
  {"user_id": 1, "email": "user1@example.com"},
  {"user_id": 2, "email": "user2@example.com"}
]


Created on Sat Nov 30 17:10:36 2024

@author: enok
"""
import pandas as pd
import os

def detect_anomaly(file: str) -> pd.DataFrame:
    """
    Detects duplicate user registrations where the same user_id appears with the same email.
    
    Args:
        file (str): Path to the input JSON file.
    
    Returns:
        pd.DataFrame: DataFrame with duplicated records (user_id, email).
    """

    try:
        if not os.path.exists(file):
            raise FileNotFoundError(f"File not found: '{file}'")
        
        # Load data
        df = pd.read_json(file)

        # Identify duplicates
        duplicates = df[df.duplicated(subset=['user_id', 'email'], keep=False)]        
        
        # Returning users duplicated
        result = duplicates[['user_id', 'email']].drop_duplicates()

        print(f"File '{file}' processed successfully.")
        return result
 
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
    except ValueError as e:
        print(f"Data processing error: {e}")
    except Exception as e:
        print(f"Data processing error: {e}")


def df_to_file(df: pd.DataFrame, file: str) -> None:
    """
    Saves a DataFrame to a JSON file.
    
    Args:
        df (pd.dataFrame): DataFrame to be saved.
        file (str): Path to the output JSON file.
    
    Returns:
        None
    """
    try:
        if os.path.exists(file):
            print(f"Warning: File '{file}' already exists. Overwriting...")
        df.to_json(file, orient='records', indent=4)
        print(f"File '{file}' saved successfully.")
    except Exception as e:
        print(f"Error to save file: {e}")

# Example usage
print("\nCalling detect_anomaly......")
output = detect_anomaly('file.json')
if output is not None:
    print(output)

output_file = 'output.json'

print(f"\nSaving to file '{output_file}'......")
df_to_file(output, output_file)

if os.path.exists(output_file):
    print("\n\nDuplicates found")
    print(pd.read_json(output_file))