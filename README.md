# Player Analysis Project

## Overview

This project provides a comprehensive analysis tool for player performance in team-based ranked matches. It processes match data, calculates various statistics, and generates insightful visualizations to help understand a player's performance over time.

## Features

- Data processing from parquet files
- Calculation of weekly and monthly statistics
- Generation of multiple performance graphs:
  - Weekly Matches Played
  - Skill and Match Rating Over Time
  - Weekly Skill Change
  - Weekly Wins and Losses
  - Match Rating Distribution
- HTML report generation with interactive Plotly graphs

## Requirements

- Python 3.7+
- pandas
- plotly
- parquet

## Usage

Run the main script to generate the analysis:

```
python main.py
```

This will create an HTML file named `player_134300_analysis.html` (or similar, depending on the player ID) in the project directory. Open this file in a web browser to view the complete analysis.

## Project Structure

- `main.py`: The entry point of the application
- `data.py`: Contains functions for data loading and processing
- `graphs.py`: Handles the creation of Plotly graphs
- `template.html`: HTML template for the final report

## Customization

To analyze a different player, modify the `player_id` variable in the `generate_report()` function in `main.py`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

