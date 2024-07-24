import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

def evaluate_wr_projections(projections, actual_stats):
    # Debug: Print columns of projections and actual_stats DataFrames
    print("Projections columns:", projections.columns)
    print("Actual stats columns:", actual_stats.columns)
    
    # Perform merge
    merged_data = pd.merge(projections, actual_stats, on=['player_id', 'season'], suffixes=('_proj', '_actual'))
    
    # Debug: Print columns of the merged DataFrame
    print("Merged data columns:", merged_data.columns)
    
    metrics = ['receptions', 'receiving_yards', 'receiving_tds']  # Updated here
    results = {}

    for metric in metrics:
        actual_col = f'{metric}_actual'
        proj_col = f'{metric}_proj'
        if actual_col not in merged_data.columns or proj_col not in merged_data.columns:
            print(f"Column {actual_col} or {proj_col} not found in merged_data")
            continue

        mae = mean_absolute_error(merged_data[actual_col], merged_data[proj_col])
        rmse = np.sqrt(mean_squared_error(merged_data[actual_col], merged_data[proj_col]))
        results[metric] = {'MAE': mae, 'RMSE': rmse}

    return results
