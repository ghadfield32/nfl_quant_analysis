### NFL Data Analysis

streamlit app: https://nfl-quant-analysis.streamlit.app/

This repository contains a comprehensive suite of tools and analyses for exploring NFL data, with a focus on player performance, offensive tendencies, and decision-making. The main feature is a Streamlit app that allows users to interactively explore these insights.
Table of Contents

    Overview
    Features
        Player Acquisition Value Analysis
        WR Projection Evaluation
        Player Quality Assessment
        Offensive Tendencies Analysis
        4th Down Decision Making
        Football Significance
        Contracts Data
    Data Sources
    Installation
    Usage
    Credits

Overview

This repository provides tools to analyze various aspects of NFL data using Python and Streamlit. Users can explore player performance metrics, offensive strategies, and make data-driven decisions using the provided analyses and visualizations.
Features
Player Acquisition Value Analysis

Analyze the value provided by different avenues of player acquisition (e.g., draft, free agency) per dollar spent.
WR Projection Evaluation

Evaluate the accuracy of college-to-pro projection systems for wide receivers using metrics like Mean Absolute Error (MAE) and Root Mean Square Error (RMSE).
Player Quality Assessment

Assess the quality of any active NFL player relative to their position group and evaluate their market value compared to their current contract.
Offensive Tendencies Analysis

Understand the offensive tendencies of a team when aligned in a 3x1 bunch formation, including run/pass balance, average yards gained, and success rates.
4th Down Decision Making

Evaluate the possible options on 4th down using historical data, success rates, and advanced metrics like Win Probability (WP) and Expected Points Added (EPA).
Football Significance

Explore personal insights and significance of football from a fan's perspective.
Contracts Data

Analyze current contracts, salary cap data, and player contract history from sources like OverTheCap.
Data Sources

The data used in this repository comes from several sources:

    nfl_data_py: A comprehensive library for accessing various NFL datasets.
    OverTheCap: Provides detailed contract and salary cap data.
    Public NFL APIs: Used for play-by-play, seasonal, and weekly data.

These sources provide a rich dataset for analyzing player performance, team strategies, and financial aspects of the NFL.
Installation

    Clone the repository:

    bash

git clone https://github.com/yourusername/nfl_data_analysis.git
cd nfl_data_analysis

Create and activate a conda environment:

bash

conda env create -f environment.yml
conda activate data_science_nfl_quant

Install additional Python packages if needed:

bash

    pip install -r requirements.txt

Usage

    Run the Streamlit app:

    bash

    streamlit run app.py

    Open your browser and navigate to the local URL provided by Streamlit (usually http://localhost:8501).

    Use the sidebar to navigate through different sections of the app:
        Player Acquisition Value Analysis
        WR Projection Evaluation
        Player Quality Assessment
        Offensive Tendencies Analysis
        4th Down Decision Making
        Football Significance
        Contracts Data

    Explore the data and visualizations interactively.

Credits

This repository was developed using several data sources and libraries. We gratefully acknowledge the following:

    nfl_data_py: For providing comprehensive NFL data access.
    OverTheCap: For detailed contract and salary cap data.
    Streamlit: For the interactive web application framework.

Contributing

We welcome contributions! Please fork the repository and submit pull requests with your changes. Ensure that your code adheres to the existing style and includes tests where appropriate.
License

This project is licensed under the MIT License. See the LICENSE file for details.