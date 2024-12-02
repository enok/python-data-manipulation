# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 16:40:32 2024

@author: enokj
"""

import pandas as pd
from collections import Counter

def extract_insights(data):
    """
    Extract insights such as the most frequent and unique entries from hierarchical data.

    Args:
        data (list): A list of dictionaries representing user interactions.

    Returns:
        dict: Insights including most clicked items and unique categories.
    """
    # Flatten the hierarchical data into a DataFrame
    df = pd.json_normalize(data)

    # Most clicked items
    most_clicked_item = df['interaction.item'].value_counts().idxmax()
    most_clicked_count = df['interaction.item'].value_counts().max()

    # Unique categories
    unique_categories = df['interaction.category'].unique()

    # Aggregate insights
    insights = {
        "most_clicked_item": most_clicked_item,
        "most_clicked_count": most_clicked_count,
        "unique_categories": list(unique_categories)
    }

    return insights


# Example hierarchical data
user_interactions = [
    {"user_id": 1, "interaction": {"item": "item1", "category": "electronics", "type": "click"}},
    {"user_id": 2, "interaction": {"item": "item2", "category": "books", "type": "click"}},
    {"user_id": 3, "interaction": {"item": "item1", "category": "electronics", "type": "click"}},
    {"user_id": 4, "interaction": {"item": "item3", "category": "fashion", "type": "click"}},
    {"user_id": 5, "interaction": {"item": "item2", "category": "books", "type": "click"}},
    {"user_id": 6, "interaction": {"item": "item1", "category": "electronics", "type": "click"}},
    {"user_id": 7, "interaction": {"item": "item4", "category": "fashion", "type": "view"}},
]

# Extract insights
insights = extract_insights(user_interactions)

# Display insights
print("Insights from User Interactions:")
print(f"Most Clicked Item: {insights['most_clicked_item']} (Clicked {insights['most_clicked_count']} times)")
print(f"Unique Categories: {', '.join(insights['unique_categories'])}")
