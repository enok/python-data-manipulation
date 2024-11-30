"""
    Merging two files, removing duplications and filtering action = login
"""
import pandas as pd
import os

def merge_json_files(file1: str, file2: str, output: str) -> None:
    try:
        if not os.path.exists(file1) or not os.path.exists(file2):
            raise FileNotFoundError(f"One or both files not found: '{file1}' or '{file2}'")
        
        # Loading files
        df1 = pd.read_json(file1)
        df2 = pd.read_json(file2)
        
        # Merging dfs and removing duplicates
        df = pd.concat([df1, df2], ignore_index=True).drop_duplicates()
        
        # Filtering: keeping just login actions
        df = df[df['action'] == 'login']
        
        # Formatting datetime to export as json string
        df['timestamp'] = df['timestamp'].astype('str')
        
        # Saving result
        df.to_json(output, orient='records', indent=4)
        
        print(f"Merged files into file: {output}")
        
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
    except ValueError as e:
        print(f"Error processing data: {e}")
    except Exception as e:
        print(f"Unknow error: {e}")    
    

merge_json_files('file1.json', 'file2.json', 'problem-1_result.json')



