import pandas as pd

def assess_player_quality(player_data, position_data):
    player_stats = player_data.iloc[0]

    percentiles = {}
    for stat in ['passing_yards', 'rushing_yards', 'receptions', 'receiving_yards', 'touchdowns']:
        if stat in player_stats and stat in position_data:
            percentile = (position_data[stat] < player_stats[stat]).mean() * 100
            percentiles[stat] = percentile

    return percentiles
