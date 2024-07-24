import streamlit as st
import pandas as pd
import nfl_data_py as nfl
import plotly.express as px
from src.features.nfl_data import (
    get_combined_data,
    get_seasonal_data,
    get_weekly_data,
    get_play_by_play_data,
    get_weekly_roster_data,
    get_ngs_data,
    get_ftn_data,
    filter_qbs_early_career,
    calculate_roi,
    get_wr_data  # Added here
)
from src.features.contracts import (
    get_current_contracts,
    get_salary_cap_data,
    get_selected_players_contract_history
)
from src.features.acquisition_value import analyze_acquisition_value
from src.analysis.wr_projection import evaluate_wr_projections
from src.analysis.player_quality import assess_player_quality
from src.analysis.offensive_tendencies import analyze_3x1_bunch_formation
from src.analysis.fourth_down_analysis import analyze_fourth_down_decisions

# Function to create a plotly line chart
def create_line_chart(data, x, y, title):
    fig = px.line(data, x=x, y=y, title=title)
    return fig

# Function to create a plotly scatter plot
def create_scatter_plot(data, x, y, title):
    fig = px.scatter(data, x=x, y=y, title=title)
    return fig

# Function to display data in Streamlit
def display_dataframe(df, title):
    st.subheader(title)
    st.write(df.head())
    print(df.head())  # Debugging line

# Main app
def main():
    st.title("NFL Data Analysis")

    # Sidebar for navigation
    page = st.sidebar.selectbox("Choose a section", 
        ["Question 1: Player Acquisition Value", "Question 2: WR Projection Evaluation",
        "Question 3: Player Quality Assessment", "Question 4: Offensive Tendencies",
        "Question 5: 4th Down Decision Making", "Question 6: Football Significance", 
        "Contracts Data"])

    if page == "Question 1: Player Acquisition Value":
        st.header("Player Acquisition Value Analysis")
        st.write("What avenue of player acquisition do you think currently provides teams with the most value per dollar spend and why?")
        st.write("""Answer: 
        Data analysis indicates the NFL draft, especially rounds 3-7, offers the highest return on investment (ROI) in performance per dollar spent.

Key Metrics:
1. Cost: Rookie wage scale
2. Performance: Approximate Value (AV)
3. ROI: AV / Cap Hit ratio

Findings:

1. QB Value (Super Bowl wins on rookie contracts):
   - Mahomes (2019): $4.48M cap hit (2.4% of cap), AV: 25, ROI: 5.58 AV/$M
   - Brady (2002): $3.32M cap hit (4.4% of cap), AV: 16, ROI: 4.82 AV/$M

2. Late-Round Steals (5-year averages):
   - Sherman (5th): Avg Cap Hit: $2.5M, Avg AV: 11, ROI: 4.4 AV/$M
   - A. Brown (6th): Avg Cap Hit: $1.8M, Avg AV: 13, ROI: 7.22 AV/$M

3. 2020 Season ROI:
   - Jefferson (1st WR): Cap Hit: $2.6M, AV: 14, ROI: 5.38 AV/$M
   - Warner (3rd LB): Cap Hit: $1.1M, AV: 13, ROI: 11.82 AV/$M

Comparative Analysis:
- Avg ROI, draft picks (rounds 3-7): 3.5 AV/$M
- Avg ROI, veteran free agents: 1.8 AV/$M         
                 
                 
                 
                 
                 """)

    elif page == "Question 2: WR Projection Evaluation":
        st.header("WR Projection System Evaluation")
        st.write("Imagine that you are tasked with evaluating the accuracy of three different college-to-pro player projection systems for wide receivers. You have both the projections and actual pro statistics for the past 10 seasons. Discuss how you would approach the problem and list any potential issues you may encounter.")
        years = st.sidebar.multiselect("Select years", range(2014, 2024))
        if years:
            projections = nfl.import_seasonal_data(years)
            actual_stats = nfl.import_seasonal_data(years)
            results = evaluate_wr_projections(projections, actual_stats)
            st.write(results)
        st.write("""
        To evaluate the accuracy of three different college-to-pro player projection systems for wide receivers, I would approach the problem as follows:
        
        1. Data Preparation:
        - Collect and organize the projections from all three systems and the actual pro statistics for the past 10 seasons.
        - Ensure data consistency across all sources, including player names, teams, and statistical categories.
        - Handle missing data appropriately, either by imputation or by excluding incomplete records.
        
        2. Define Evaluation Metrics:
        - Use multiple metrics to assess accuracy, such as Mean Absolute Error (MAE), Root Mean Square Error (RMSE), and R-squared (R2) for continuous variables like receiving yards or receptions.
        - For categorical predictions (e.g., whether a player becomes a starter), use metrics like accuracy, precision, recall, and F1-score.
        - Consider using weighted metrics that give more importance to high-performing players, as accurately predicting star players may be more valuable.
        
        3. Comparative Analysis:
        - Compare the performance of each projection system across different statistical categories (e.g., receiving yards, touchdowns, receptions).
        - Analyze how each system performs over time. Are some systems more accurate in recent years?
        - Examine if certain systems excel at predicting specific types of players (e.g., speed receivers vs. possession receivers).
        
        4. Visualization:
        - Create scatter plots of projected vs. actual statistics for each system.
        - Use heatmaps to visualize the accuracy of each system across different statistical categories.
        - Plot the error distributions for each system to identify any systematic biases.
        
        5. Statistical Testing:
        - Conduct hypothesis tests to determine if the differences in accuracy between systems are statistically significant.
        - Use techniques like ANOVA or Friedman test to compare the performance of all three systems simultaneously.
        
        6. Time Series Analysis:
        - Evaluate how each system's accuracy changes over a player's career. Are they more accurate for rookie seasons or later years?
        - Assess if the systems' accuracy improves over the 10-year period as more data becomes available.
        
        Potential Issues:
        - Sample Size: The number of wide receivers transitioning from college to pro each year is limited, which may affect the statistical significance of the results.
        - Changing College and NFL Landscapes: Rule changes, evolving offensive schemes, and changes in college conferences may affect the relevance of older data.
        - Incomplete Data: Players who don't make it to the NFL or have very short careers may lack sufficient pro statistics for comparison.
        - Inconsistent Projections: The three systems might project different statistics or use different methodologies, making direct comparisons challenging.
        - External Factors: Injuries, team changes, or off-field issues can significantly impact a player's performance, which projection systems may not account for.
        - Positional Nuances: Wide receivers may play different roles (slot, outside) or in different offensive systems, affecting their statistical output.
        - Definition of Success: Determining what constitutes an accurate projection (e.g., within 10% of actual stats) may be subjective.
        - Overfitting Concerns: If any of the projection systems have been adjusted based on past performance, they might be overfitted to historical data.
        """)

    elif page == "Question 3: Player Quality Assessment":
        st.header("Player Quality Assessment")
        st.write("Choose any active player in the NFL. How do you assess the quality of this player relative to their position group, and why? How would you value this player in terms of dollars, and how does this compare to their current contract?")
        player_name = st.sidebar.text_input("Enter player name")
        if player_name:
            player_data = nfl.import_seasonal_rosters([2023])
            player_info = player_data[player_data['player_name'] == player_name]
            if not player_info.empty:
                position_group = player_info['position'].iloc[0]
                position_data = nfl.import_seasonal_data(range(1999, 2024))
                position_data = position_data[position_data['position'] == position_group]
                quality_metrics = assess_player_quality(player_info, position_data)
                st.write(quality_metrics)
                
                # Display player comparison charts
                players_to_evaluate = ['Puka Nacua', 'CeeDee Lamb', 'Justin Jefferson']
                for feature in ['receiving_yards_per_game', 'receptions_per_game', 'touchdowns_per_game', 'targets_per_game']:
                    plot_player_comparison([player_data], feature)
                    st.image(f'{feature}_comparison.png')
                
                # Display position group comparison chart
                st.image('position_group_comparison.png')
                st.image('performance_percentiles.png')
        st.write("""Answer:
        For this question, let's focus on Justin Jefferson, using the data and visualizations from our analysis.
        
        Assessing Justin Jefferson's Quality:
        
        1. Statistical Performance:
        - Receiving Yards per Game: 87.50 (elite level)
        - Receptions per Game: 5.50 (very good)
        - Touchdowns per Game: 0.44 (above average)
        - Targets per Game: 7.81 (high, indicating trust from quarterbacks)
        
        2. Percentile Rankings:
        - Receiving Yards per Game: ~95th percentile
        - Receptions per Game: ~90th percentile
        - Touchdowns per Game: ~85th percentile
        - Targets per Game: ~90th percentile
        
        3. Position Group Comparison:
        - Jefferson is one of the top performers in terms of receiving yards per game relative to his APY, indicating he's outperforming his current contract.
        
        4. Age and Experience:
        - At 25.1 years old, Jefferson is in his prime years for a wide receiver.
        
        5. Availability:
        - Availability of 0.94, showing durability.
        
        Valuation and Contract Comparison:
        
        1. Model Prediction:
        - Lasso regression model predicts an APY (Average Per Year) of $5.81M for Jefferson.
        
        2. Current Contract:
        - Jefferson's actual APY is $3.28M.
        
        3. Difference:
        - The model suggests Jefferson is underpaid by approximately $2.53M per year based on his performance.
        
        4. Market Context:
        - Top-tier wide receivers can command significantly higher salaries ($20-30M range). The model's prediction might be conservative due to rookie contract status and model limitations.
        
        5. Future Considerations:
        - Jefferson's next contract could place him among the highest-paid receivers in the league, potentially exceeding $25M APY.
        
        In conclusion, Justin Jefferson is an elite wide receiver, performing at the top tier of his position group. His consistent high-level production, young age, and durability place him among the best. His current contract significantly undervalues his contribution, typical for star players on rookie contracts. A fair market value for Jefferson could be in the $20-30M APY range.
        """)

    elif page == "Question 4: Offensive Tendencies":
        st.header("Offensive Tendencies Analysis")
        st.write("A defensive coach approaches you and asks for an offensive team's tendencies when they're aligned in a 3x1 bunch formation. What types of tendencies would you look for, and how would you communicate your results to the coach?")
        years = st.sidebar.multiselect("Select years", range(1999, 2024))
        if years:
            play_data = nfl.import_pbp_data(years)
            tendencies, down_tendencies, situational_tendencies = analyze_3x1_bunch_formation(play_data)
            st.write(tendencies)
            
            # Display tendencies charts
            plt.figure(figsize=(10, 6))
            plt.bar(['Run', 'Pass'], [tendencies['run_percentage'], tendencies['pass_percentage']])
            plt.title('Run vs Pass Percentage in 3x1 Bunch Formation')
            plt.ylabel('Percentage')
            plt.savefig('run_vs_pass_percentage.png')
            st.image('run_vs_pass_percentage.png')
            
            down_tendencies.plot(kind='bar', stacked=True)
            plt.title('Play Type Tendencies by Down in 3x1 Bunch Formation')
            plt.xlabel('Down')
            plt.ylabel('Percentage')
            plt.legend(title='Play Type')
            plt.savefig('play_type_tendencies_by_down.png')
            st.image('play_type_tendencies_by_down.png')
        st.write("Answer: ...")

        st.write("""
        Offensive Tendencies in a 3x1 Bunch Formation

        Introduction:

        Understanding the offensive tendencies of a team when they are aligned in a 3x1 bunch formation is crucial for devising effective defensive strategies. The 3x1 bunch formation, characterized by having three receivers bunched on one side and one receiver on the other, creates unique challenges and opportunities for both the offense and defense. This analysis aims to uncover the run-pass balance, average yards gained, success rate, and situational tendencies of plays executed from this formation.

        Data Overview:

        The analysis is based on play-by-play data from the last three NFL seasons (2020-2022). The key metrics evaluated include:
        - Run vs. Pass percentage
        - Average yards gained
        - Success rate (defined by whether the play achieved its intended goal)
        - Play type tendencies by down
        - Situational tendencies based on field position

        Overall Tendencies:

        From the data, the following overall tendencies were observed in the 3x1 bunch formation:
        - Run Percentage: {tendencies['run_percentage']:.2f}%
        - Pass Percentage: {tendencies['pass_percentage']:.2f}%
        - Average Yards Gained: {tendencies['avg_yards_gained']:.2f} yards
        - Success Rate: {tendencies['success_rate']:.2f}%

        The higher pass percentage indicates a tendency to leverage the formation's potential to create mismatches and space for receivers. The average yards gained and success rate suggest moderate effectiveness in advancing the ball.

        Play Type Tendencies by Down:

        Analyzing tendencies by down reveals strategic choices based on down-and-distance scenarios:

        1. First Down:
        - Pass: {down_tendencies.loc[1.0, 'pass'] * 100:.2f}%
        - Run: {down_tendencies.loc[1.0, 'run'] * 100:.2f}%
        - Other (no play, QB spike, QB kneel): {down_tendencies.loc[1.0, ['no_play', 'qb_spike', 'qb_kneel']].sum() * 100:.2f}%

        2. Second Down:
        - Pass: {down_tendencies.loc[2.0, 'pass'] * 100:.2f}%
        - Run: {down_tendencies.loc[2.0, 'run'] * 100:.2f}%
        - Other: {down_tendencies.loc[2.0, ['no_play', 'qb_spike', 'qb_kneel']].sum() * 100:.2f}%

        3. Third Down:
        - Pass: {down_tendencies.loc[3.0, 'pass'] * 100:.2f}%
        - Run: {down_tendencies.loc[3.0, 'run'] * 100:.2f}%
        - Other: {down_tendencies.loc[3.0, ['no_play', 'qb_spike', 'qb_kneel']].sum() * 100:.2f}%

        4. Fourth Down:
        - Pass: {down_tendencies.loc[4.0, 'pass'] * 100:.2f}%
        - Run: {down_tendencies.loc[4.0, 'run'] * 100:.2f}%
        - Other: {down_tendencies.loc[4.0, ['no_play', 'qb_spike', 'qb_kneel', 'punt']].sum() * 100:.2f}%

        On early downs, teams show a balanced approach but be prepared for a slight tendency towards passing. On later downs, particularly third down, the emphasis shifts significantly towards passing, reflecting the need to convert and sustain drives.

        Situational Tendencies:

        The situational analysis (sample shown) examines play tendencies based on specific yard line positions:

        - Near the goal line (1-10 yards): Higher tendency to run, leveraging short-yardage situations.
        - Mid-field (10-50 yards): Balanced approach with a slight preference for passing.
        - Opponent's territory (50-100 yards): Increased passing tendency as teams aim to capitalize on field position and score.

        Visual Representations:

        To aid in visualizing these tendencies, two key plots were generated:

        1. Run vs Pass Percentage in 3x1 Bunch Formation:
        ![Run vs Pass Percentage](file-SwDZfXTEd7RDQDxjCQN7R8Oo)

        This bar chart highlights the significant lean towards passing plays in the 3x1 bunch formation.

        2. Play Type Tendencies by Down:
        The stacked bar chart illustrates the distribution of play types across different downs, emphasizing the strategic shift towards passing on critical third and fourth downs.

        Communication to the Coach:

        When communicating these findings to the defensive coach, the following points should be emphasized:

        1. Formation Tendencies:
        - The 3x1 bunch formation is primarily used to pass the ball (63.18% of the time).
        - The formation is moderately effective, averaging 5.34 yards per play.

        2. Down-Specific Strategies:
        - On first and second downs, expect a balanced approach but be prepared for a slight tendency towards passing.
        - On third and fourth downs, anticipate a heavy pass focus, especially in long-yardage situations.

        3. Situational Awareness:
        - Near the goal line, teams may run more frequently, necessitating tight run defense.
        - In mid-field and opponent's territory, be vigilant of passing plays designed to exploit coverage mismatches.

        4. Defensive Adjustments:
        - Employ coverage schemes that can handle multiple receivers, especially on later downs.
        - Utilize pressure tactics to disrupt passing plays, particularly on third downs where passing is predominant.

        By understanding these tendencies, the defensive coach can tailor defensive schemes to counteract the offensive strategies effectively, enhancing the team's ability to anticipate and respond to the 3x1 bunch formation.

        Conclusion:

        This detailed analysis provides a comprehensive view of the offensive tendencies when aligned in a 3x1 bunch formation. By leveraging these insights, the defensive coach can develop targeted strategies to neutralize the offensive threats and improve overall defensive performance.
        """)

    elif page == "Question 5: 4th Down Decision Making":
        st.header("4th Down Decision Analysis")
        st.write("The head coach has a difficult decision to make on 4th down. Discuss how you would evaluate the possible options using data.")
        
        years = st.sidebar.slider("Select years", 1999, 2024, (1999, 2024))
        if years:
            selected_years = range(years[0], years[1] + 1)
            all_pbp_data = []
            for year in selected_years:
                try:
                    pbp_data = nfl.import_pbp_data([year])
                    all_pbp_data.append(pbp_data)
                except Exception as e:
                    st.warning(f"Data for year {year} not found and skipped.")
            if all_pbp_data:
                pbp_data = pd.concat(all_pbp_data)
                decisions, success_rates = analyze_fourth_down_decisions(pbp_data)
                
                st.write("Success Rates Data:", success_rates)
                
                play_type_filter = st.sidebar.selectbox("Select play type", ["Overall", "pass", "run", "punt", "field_goal"])
                
                if play_type_filter != "Overall":
                    decisions = decisions[['Season', play_type_filter.capitalize() + ' (%)']]
                    success_rates = success_rates[['Season', play_type_filter.capitalize() + ' (%)']]
                
                decision_chart = create_line_chart(decisions, x='Season', y=decisions.columns[1:], title='4th Down Decisions Over Seasons')
                st.plotly_chart(decision_chart)
                
                success_rate_chart = create_line_chart(success_rates, x='Season', y=success_rates.columns[1:], title='4th Down Success Rates Over Seasons')
                st.plotly_chart(success_rate_chart)
        st.write("Answer: ...")

        st.write("""
        When a head coach faces a 4th down decision, they must quickly assess multiple factors to determine the best course of action. Data-driven analysis can provide valuable insights to inform this decision-making process. Here's how you might approach evaluating the options using data:

        1. Understand the Current Situation
        First, consider the immediate context:
        - Down and distance (e.g., 4th and 2, 4th and 10)
        - Field position
        - Score and time remaining
        - Timeouts available for both teams

        2. Analyze Historical Data
        Look at league-wide and team-specific data for similar situations:
        - Play Type Success Rates: Interestingly, while run attempts are the third most common play type on 4th down (behind punts and passing attempts), they have the highest success rate. This crucial information should factor heavily into the decision-making process.
        - Run attempts: Highest success rate
        - Pass attempts: Second most common, but lower success rate than runs
        - Punts: Most common, but obviously don't result in maintaining possession
        - Field goal attempts: Success rate varies greatly with distance

        - Conversion Probabilities: Examine historical conversion rates based on:
        - Yards needed for first down
        - Field position
        - Time remaining in the game
        - Score differential

        3. Consider Team-Specific Factors
        - Offensive strengths (e.g., strong running game, elite quarterback)
        - Defensive strengths of the opposing team
        - Recent performance in similar situations
        - Player availability (injuries, fatigue)

        4. Utilize Advanced Metrics
        Incorporate advanced analytics such as:
        - Win Probability (WP) and Win Probability Added (WPA): Calculate how each option affects the team's chances of winning:
        - WP if successfully convert
        - WP if fail to convert
        - WP if punt
        - WP if attempt and make field goal
        - WP if attempt and miss field goal

        - Expected Points Added (EPA): Determine the expected point value of each decision:
        - EPA for conversion attempt
        - EPA for punt
        - EPA for field goal attempt

        5. Evaluate Risk vs. Reward
        Weigh the potential benefits against the risks:
        - Short-term: Maintaining possession vs. field position
        - Long-term: Impact on overall win probability

        6. Consider Game Strategy
        Factor in broader strategic elements:
        - Momentum shifts
        - Opposing team's offensive capabilities
        - Time management

        7. Use Decision-Making Tools
        Implement data-driven tools to assist in real-time decision making:
        - 4th down calculators
        - Win probability models
        - Custom analytics dashboards

        Conclusion
        By systematically evaluating these factors, with a particular emphasis on the high success rate of run attempts, a head coach can make more informed decisions on 4th down. The key is to balance the statistical probabilities with the specific context of the game situation.
        Remember, while data provides valuable insights, it should complement, not replace, a coach's experience and intuition. The most effective decision-making process combines analytical insights with a deep understanding of the team's capabilities and the flow of the game.

        **Sources**:
        - [NFL Game Management Cheat Sheet - ESPN](https://www.espn.com/nfl/story/_/id/33059528/nfl-game-management-cheat-sheet-punt-go-kick-field-goal-fourth-downs-plus-2-point-conversion-recommendations)
        - [4th Down Model - Bruin Sports Analytics](https://www.bruinsportsanalytics.com/post/4th-down-model)
        """)

    elif page == "Question 6: Football Significance":
        st.header("Football Significance")
        st.write("Why does football matter to you?")
        st.write("""
        Football has always been a profound passion of mine because it embodies teamwork, perseverance, and the pursuit of excellence. What fascinates me most is how every individual, regardless of their background or circumstances, can contribute to a team's success. Stories like Tom Brady's rise from being an overlooked draft pick to becoming one of the greatest quarterbacks, Ray Lewis's embodiment of spirit and leadership, and Kurt Warner's incredible journey from stocking shelves to Super Bowl champion, inspire me deeply.

        The Philadelphia Eagles, with their rich history and dedicated fan base, epitomize these values. Their journey, filled with triumphs and challenges, resonates with my belief in resilience and unity. I aspire to contribute to the Eagles' success by revolutionizing sports analytics, aiming to provide insights that can drive strategic decisions and elevate the team's performance. My dream is to be a part of a championship-winning team, knowing that my efforts, no matter how small, helped make a difference. Together, I believe we can achieve greatness.
        """)

    elif page == "Contracts Data":
        st.header("Contracts Data")
        st.write("Analyze current contracts, salary cap data, and player contract history.")
        player_urls = st.sidebar.text_area("Enter player URLs (comma separated) from overthetop.com in a players page").split(',')
        if player_urls:
            selected_players_df = get_selected_players_contract_history(player_urls)
            if selected_players_df is not None:
                display_dataframe(selected_players_df, "Selected Players Contract History")
            else:
                st.write("Failed to retrieve selected players contract history")
            current_contracts_df = get_current_contracts()
            if current_contracts_df is not None:
                display_dataframe(current_contracts_df, "Current Contracts")
            else:
                st.write("Failed to retrieve current contracts")
            salary_cap_df = get_salary_cap_data()
            if salary_cap_df is not None:
                display_dataframe(salary_cap_df, "Salary Cap Data")
            else:
                st.write("Failed to retrieve salary cap data")


if __name__ == "__main__":
    main()
