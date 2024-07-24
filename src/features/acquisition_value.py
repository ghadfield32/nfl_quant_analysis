import pandas as pd
import nfl_data_py as nfl

def analyze_acquisition_value(years):
    if not isinstance(years, (list, range)):
        raise ValueError("years variable must be list or range.")
    
    draft_data = nfl.import_draft_picks(years)
    seasonal_data = nfl.import_seasonal_data(years, s_type='REG')

    try:
        salary_df = nfl.import_contracts()
        if 'year_signed' not in salary_df.columns:
            print("Warning: 'year_signed' column not found in salary data. Skipping salary analysis.")
            return draft_data, seasonal_data

        required_cols = ['player', 'year_signed', 'value']
        if not all(col in salary_df.columns for col in required_cols):
            print(f"Warning: Missing required columns in salary data. Expected {required_cols}. Found {salary_df.columns.tolist()}. Skipping salary analysis.")
            return draft_data, seasonal_data

        seasonal_data = pd.merge(seasonal_data, salary_df[required_cols], left_on=['player', 'season'], right_on=['player', 'year_signed'], how='left')
        seasonal_data['value_per_dollar'] = seasonal_data['approximate_value'] / seasonal_data['value']
    except Exception as e:
        print(f"Error processing salary data: {str(e)}. Skipping salary analysis.")
        return draft_data, seasonal_data

    drafted_players = seasonal_data[seasonal_data['draft_number'].notnull()]
    undrafted_players = seasonal_data[seasonal_data['draft_number'].isnull()]

    return drafted_players, undrafted_players
