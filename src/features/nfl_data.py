import nfl_data_py as nfl
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_seasonal_data(year):
    year_list = [int(year)]
    df = nfl.import_seasonal_data(year_list)
    id_df = nfl.import_ids()[['gsis_id', 'name']]
    df = pd.merge(df, id_df, left_on='player_id', right_on='gsis_id', how='left')

    salary_df = nfl.import_contracts()
    if 'year_signed' not in salary_df.columns:
        print("'year_signed' column not found in salary data")
    df = pd.merge(df, salary_df[['player', 'year_signed', 'value']], left_on=['name', 'season'], right_on=['player', 'year_signed'], how='left', suffixes=('_left', '_right'))

    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-2]
    return df[cols].sort_values('name')

def get_wr_data(years):
    seasonal_data = nfl.import_seasonal_data(years)
    
    wr_data = seasonal_data[
        (seasonal_data['receptions'].notna()) & 
        (seasonal_data['receiving_yards'].notna()) & 
        (seasonal_data['targets'].notna()) &
        (seasonal_data['receptions'] > 0)
    ]

    player_ids = nfl.import_ids()
    wr_data = pd.merge(wr_data, player_ids[['gsis_id', 'name', 'weight', 'height', 'age']], left_on='player_id', right_on='gsis_id', how='left')
    
    salary_data = nfl.import_contracts()
    wr_data = pd.merge(wr_data, salary_data[['player', 'year_signed', 'value', 'apy', 'team']], 
                       left_on=['name', 'season'], right_on=['player', 'year_signed'], how='left')

    wr_data['availability'] = wr_data['games'] / 17
    wr_data = wr_data.dropna(subset=['apy'])  # Remove players without salary data
    
    return wr_data

# Example usage
years = range(2013, 2024)
wr_data = get_wr_data(years)
print(wr_data.head())

def get_weekly_data(year):
    return nfl.import_weekly_data([int(year)])

def get_play_by_play_data(year):
    return nfl.import_pbp_data([int(year)])

def get_weekly_roster_data(year):
    return nfl.import_weekly_rosters([int(year)])

def get_ngs_data(stat_type, year):
    return nfl.import_ngs_data(stat_type, [int(year)])

def get_ftn_data(year):
    return nfl.import_ftn_data([int(year)])

def get_salary_cap_data():
    url = 'https://overthecap.com/salary-cap-space'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')

    if not tables:
        return None

    for table in tables:
        headers = [th.text.strip() for th in table.find_all('th')]
        if 'Team' in headers and 'Cap Space' in headers:
            rows = []
            for tr in table.find_all('tr')[1:]:
                row = [td.text.strip() for td in tr.find_all('td')]
                if row:
                    rows.append(row)

            df = pd.DataFrame(rows, columns=headers)
            for col in df.columns[1:]:
                df[col] = df[col].replace('[\$,]', '', regex=True).astype(float, errors='ignore')

            return df

    return None

def get_combined_data(year):
    seasonal_data = nfl.import_seasonal_data([year])
    ids = nfl.import_ids()[['gsis_id', 'name']]
    seasonal_data = pd.merge(seasonal_data, ids, left_on='player_id', right_on='gsis_id', how='left')

    salary_data = nfl.import_contracts()
    salary_cap_data = get_salary_cap_data()

    combined_data = pd.merge(seasonal_data, salary_data, left_on=['name', 'season'], right_on=['player', 'year_signed'], how='left', suffixes=('_season', '_salary'))
    combined_data = pd.merge(combined_data, salary_cap_data, left_on='team', right_on='Team', how='left')

    return combined_data

def filter_qbs_early_career(data, years=3):
    qbs = data[data['position'] == 'QB']
    early_career_qbs = qbs[qbs['season'] - qbs['draft_year'] <= years]
    return early_career_qbs

def calculate_roi(data):
    data['cap_pct'] = data['value'] / data['Cap Space']
    data['roi'] = data['passing_yards'] / data['value']
    return data

def main():
    year = 2023
    combined_data = get_combined_data(year)
    early_career_qbs = filter_qbs_early_career(combined_data)
    roi_data = calculate_roi(early_career_qbs)
    print(roi_data[['name', 'team', 'season', 'passing_yards', 'value', 'cap_pct', 'roi']])

if __name__ == "__main__":
    main()
