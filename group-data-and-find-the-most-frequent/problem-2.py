# %% Group Data and Find the Most Frequent
import pandas as pd
import os

def group_data_and_find_most_frequent(file: str) -> pd.DataFrame:
    """
    Reads a JSON file, groups data by user_id and item,
    and finds the most purchased item for each user.
    
    Args:
        file (str): Path to the input JSON file.
    
    Returns:
        pd.DataFrame: DataFrame with user_id and most_purchased_item.
    """
    try:
        if not os.path.exists(file):
            raise FileNotFoundError(f"File not found: {file}")
        
        # Load data
        df = pd.read_json(file)

        # Summing quantities
        grouped_df = df.groupby(by=['user_id', 'item'], as_index=False)['quantity'].sum()
        
        # Find the most purchased item for each user
        # Group again by user_id and determine max for each group
        most_purchased = grouped_df.loc[
            grouped_df.groupby('user_id')['quantity'].idxmax()
        ]
        
        result = most_purchased[['user_id', 'item']].rename(columns={'item': 'most_purchased_item'})
        
        return result

    except FileNotFoundError as e:
        print(f"Could not open '{file}': {e}")
    except ValueError as e:
        print(f"Error manipulating data: {e}")
    except Exception as e:
        print(f"Unknown error: {e}")


def save_to_file(result: pd.DataFrame, output: str) -> None:
    """
    Saves a DataFrame to a JSON file.
    
    Args:
        result (pd.DataFrame): DataFrame to save.
        output (str): Path to the output JSON file.
    """
    try:
        result.to_json(output, orient='records', indent=4)
        print(f"Result saved to {output}")
    except Exception as e:
        print(f"Error saving to file: {e}")

# Example usage
output = group_data_and_find_most_frequent('file.json')
if output is not None:
    save_to_file(output, 'problem-2_result.json')
