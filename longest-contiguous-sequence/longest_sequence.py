# -*- coding: utf-8 -*-
"""
Problem 4: Longest Contiguous Sequence

Task: 
    You are given a dataset of login dates for a user. 
    Find the longest contiguous sequence of login days.

Input JSON:
[
  {"user_id": 1, "login_date": "2024-11-01T08:00:00"},
  {"user_id": 1, "login_date": "2024-11-02T09:00:00"},
  {"user_id": 1, "login_date": "2024-11-04T10:30:00"},
  {"user_id": 1, "login_date": "2024-11-05T11:00:00"},
  {"user_id": 2, "login_date": "2024-11-01T12:00:00"},
  {"user_id": 2, "login_date": "2024-11-02T13:00:00"},
  {"user_id": 2, "login_date": "2024-11-03T14:00:00"},
  {"user_id": 2, "login_date": "2024-11-05T15:00:00"},
  {"user_id": 4, "login_date": "2024-11-05T11:00:00"},
  {"user_id": 3, "login_date": "2024-11-01T08:00:00"},
  {"user_id": 3, "login_date": "2024-11-03T09:00:00"},
  {"user_id": 3, "login_date": "2024-11-04T10:00:00"},
  {"user_id": 3, "login_date": "2024-11-05T11:00:00"},
  {"user_id": 6},
  {"user_id": 5},
  {"user_id": 5, "login_date": "2024-11-05T11:00:00"}
]


Expected Output:
[
  {"user_id": 1, "longest_sequence": 2, "start_date": "2024-11-01", "end_date": "2024-11-02"},
  {"user_id": 2, "longest_sequence": 3, "start_date": "2024-11-01", "end_date": "2024-11-03"},
  {"user_id": 3, "longest_sequence": 3, "start_date": "2024-11-03", "end_date": "2024-11-05"}
  {"user_id": 4, "longest_sequence": 1, "start_date": "2024-11-05", "end_date": "2024-11-05"},
  {"user_id": 5, "longest_sequence": 1, "start_date": "2024-11-05", "end_date": "2024-11-05"},
  {"user_id": 6, "longest_sequence": 0, "start_date": None, "end_date": None}
]


Created on Sat Nov 30 18:15:08 2024

@author: enokj
"""
import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)



def longest_contiguous_sequence(file: str) -> pd.DataFrame:
    """
    Returns the longest login date interval for every user.
    

    Args:
        - file (str): Path to JSON file.
    
    Returns:
        - pd.DataFrame: DataFrame with longest date interval of each user.
    """
    try:
        if not os.path.exists(file):
            raise FileNotFoundError(f"File '{file}' not found.")
        
        # Load and preprocess data
        df = pd.read_json(file)
        
        if df.empty:
            return pd.DataFrame(columns=["user_id", "longest_sequence", "start_date", "end_date"])
        
        if 'user_id' not in df.columns:
            raise ValueError("Input file is missing the 'user_id' column.")

        # Tranforming string to date
        df['login_date'] = pd.to_datetime(df['login_date'], errors='coerce').dt.date

        # Sorting data
        df = df.sort_values(by=['user_id', 'login_date'])
        
        # Grouping by user
        grouped = df.groupby(by='user_id')
        
        # Finds the longest users login date sequence per user
        results = []
        for user, group in grouped:
            group = group.reset_index(drop=True)
            results.append(extract_longest_sequence(user, group))

        logging.info(f"Process done for file '{file}'")
        return pd.DataFrame(results)

    except FileNotFoundError as e:
        logging.error(f"File not found error -> {e}")
    except ValueError as e:
        logging.error(f"Processing data error -> {e}")
    except Exception as e:
        logging.error(f"Not mapped error -> {e}")



def extract_longest_sequence(user: int, group: pd.DataFrame) -> dict:
    """
    Finds the longest contiguous sequence of dates for a user.
    

    Args:
        - user (int): User ID.
        - group (pd.DataFrame): DataFrame containing login dates for the user.
    
    Returns:
        - dict: User's longest login date sequence with start and end dates.
    """
    try:
        if group.empty or pd.isna(group.iloc[0]['login_date']):
            return {
                "user_id": user,
                "longest_sequence": 0,
                "start_date": None,
                "end_date": None,
            }

        max_sequence = current_sequence = 1
        max_sequence_start_date = current_start_date = max_sequence_end_date = group.iloc[0]['login_date']
        
        for i in range(1, len(group)):
            current_login_date = group.iloc[i]['login_date']
            previous_login_date = group.iloc[i - 1]['login_date']

            if pd.isna(current_login_date) or pd.isna(previous_login_date) or (current_login_date - previous_login_date).days > 1:
                current_sequence = 1
                current_start_date = current_login_date
            else:
                current_sequence += 1
                if current_sequence > max_sequence:
                    max_sequence = current_sequence
                    max_sequence_start_date = current_start_date
                    max_sequence_end_date = current_login_date

        logging.info(f"Longest sequence for user '{user}' calculated")
        return {
            "user_id": user,
            "longest_sequence": max_sequence,
            "start_date": str(max_sequence_start_date) if max_sequence_start_date else None,
            "end_date": str(max_sequence_end_date) if max_sequence_end_date else None,
        }

    except Exception as e:
        logging.error(f"Not mapped error -> {e}")



def save_to_json(df: pd.DataFrame, file: str) -> None:
    """
    Saves a DataFrame as JSON file.
    

    Args:
        - df (pd.DataFrame): DataFrame to be save as JSON file.
        - file (str): Path to JSON file.
    """
    try:
        if os.path.exists(file):
            logging.warning(f"File '{file}' alread exists. Overwriting...")
        
        df.to_json(file, orient='records', indent=4)
        
        logging.info(f"File '{file}' saved")

    except Exception as e:
        logging.error(f"Not mapped error -> {e}")


# Example usage
if __name__ == "__main__":
    input_file = 'file.json'
    output_file = 'output.json'

    logging.info("\n\nExample of usage")
    logging.info("-----------------------------------------------------")
    output = longest_contiguous_sequence(input_file)
    if output is not None:
        print(output)

    logging.info("\n\nSaving DataFrame to JSON file")
    logging.info("-----------------------------------------------------")
    save_to_json(output, output_file)

    logging.info("\n\nLoading saved JSON file")
    logging.info("-----------------------------------------------------")
    if os.path.exists(output_file):
        print(pd.read_json(output_file))