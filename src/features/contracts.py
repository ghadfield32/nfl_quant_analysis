import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_player_contract_history(player_url):
    response = requests.get(player_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')

    if not tables:
        return None

    for table in tables:
        headers = [th.text.strip() for th in table.find_all('th')]
        if 'Year' in headers and 'Age' in headers and 'Base Salary' in headers:
            rows = []
            for tr in table.find_all('tr')[1:]:
                row = [td.text.strip() for td in tr.find_all('td')]
                if row:
                    row = row[:len(headers)]
                    rows.append(row)

            df = pd.DataFrame(rows, columns=headers)
            for col in df.columns[1:]:
                df[col] = df[col].replace('[\$,]', '', regex=True).astype(float, errors='ignore')

            return df

    return None

def get_current_contracts():
    url = 'https://overthecap.com/cash-flows'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')

    if not tables:
        return None

    for table in tables:
        headers = [th.text.strip() for th in table.find_all('th')]
        if 'Player' in headers and 'Team' in headers and 'Position' in headers:
            rows = []
            for tr in table.find_all('tr')[1:]:
                row = [td.text.strip() for td in tr.find_all('td')]
                if row:
                    rows.append(row)

            df = pd.DataFrame(rows, columns=headers)
            for col in df.columns[3:]:
                df[col] = df[col].replace('[\$,]', '', regex=True).astype(float, errors='ignore')

            return df

    return None

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

def get_selected_players_contract_history(player_urls):
    all_player_data = []

    for url in player_urls:
        try:
            player_df = get_player_contract_history(url)
            if player_df is not None:
                player_name = url.split('/')[-2].replace('-', ' ').title()
                player_df['Player'] = player_name
                all_player_data.append(player_df)
            time.sleep(1)
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")

    if all_player_data:
        try:
            return pd.concat(all_player_data, ignore_index=True)
        except Exception as e:
            print(f"Error concatenating player data: {str(e)}")
            return None
    else:
        return None
