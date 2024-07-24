import pandas as pd


def analyze_3x1_bunch_formation(play_data):
    # Filter plays for '3x1 bunch' inferred formation: 1 RB, 1 TE, 3 WR
    bunch_formation_plays = play_data[play_data['offense_personnel'] == '1 RB, 1 TE, 3 WR']
    
    # Debug: Check the number of plays in the 3x1 bunch formation
    print("Number of plays in 3x1 bunch formation:", bunch_formation_plays.shape[0])
    
    tendencies = {
        'run_percentage': (bunch_formation_plays['play_type'] == 'run').mean() * 100,
        'pass_percentage': (bunch_formation_plays['play_type'] == 'pass').mean() * 100,
        'avg_yards_gained': bunch_formation_plays['yards_gained'].mean(),
        'success_rate': (bunch_formation_plays['success'] == 1).mean() * 100
    }
    
    # Additional analyses
    down_tendencies = bunch_formation_plays.groupby('down')['play_type'].value_counts(normalize=True).unstack()
    
    situational_tendencies = bunch_formation_plays.groupby(['down', 'yardline_100'])['play_type'].value_counts(normalize=True).unstack()
    
    return tendencies, down_tendencies, situational_tendencies

# Example usage
# years = [2020, 2021, 2022]
# play_data = pd.concat([nfl.import_pbp_data([year]) for year in years])
# tendencies, down_tendencies, situational_tendencies = analyze_3x1_bunch_formation(play_data)

# print("Overall Tendencies:", tendencies)
# print("Tendencies by Down:", down_tendencies)
# print("Situational Tendencies:", situational_tendencies.head(10))
