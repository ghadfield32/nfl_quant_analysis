import pandas as pd

def analyze_fourth_down_decisions(pbp_data):
    fourth_down_plays = pbp_data[pbp_data['down'] == 4]
    decisions = fourth_down_plays.groupby(['season', 'play_type']).size().unstack(fill_value=0).reset_index()
    decisions['total'] = decisions.sum(axis=1)
    success_rates = fourth_down_plays.groupby(['season', 'play_type'])['success'].mean().unstack(fill_value=0).reset_index()
    decisions.columns = ['Season'] + [f"{col.capitalize()} (%)" for col in decisions.columns[1:]]
    success_rates.columns = ['Season'] + [f"{col.capitalize()} (%)" for col in success_rates.columns[1:]]
    return decisions, success_rates
