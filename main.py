import json
import plotly
from data import load_data, get_player_data, calculate_weekly_stats, get_latest_skills
from graphs import create_plots, add_stats_annotations

def print_game_types(ranked_team_matches):
    game_types = ranked_team_matches['game_type'].value_counts()
    total_matches = len(ranked_team_matches)
    
    print("\nGame Types Played:")
    print("-----------------")
    for game_type, count in game_types.items():
        percentage = (count / total_matches) * 100
        print(f"{game_type}: {count} matches ({percentage:.2f}%)")
    print(f"\nTotal Ranked Team Matches: {total_matches}")

def generate_report():
    # Load data
    matches_df, players_df = load_data()
    
    # Get player data for 134300
    player_id = 134300
    player_matches, ranked_team_matches, latest_match_ratings = get_player_data(players_df, matches_df, player_id)
    
    # Print game types
    print_game_types(ranked_team_matches)
    
    # Calculate weekly stats
    weekly_stats = calculate_weekly_stats(ranked_team_matches)
    
    # Create plots
    fig = create_plots(weekly_stats, latest_match_ratings, player_id)
    
    # Calculate percentile based on match rating
    player_match_rating = latest_match_ratings[player_id]
    percentile = (latest_match_ratings < player_match_rating).mean() * 100
    
    # Add stats annotations
    fig = add_stats_annotations(fig, ranked_team_matches, percentile)
    
    # Convert plot to JSON
    plotly_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Read HTML template
    with open('template.html', 'r') as file:
        html_template = file.read()
    
    # Replace placeholder with plot data
    html_output = html_template.replace('{{ plotly_json | safe }}', plotly_json)
    
    # Write to file
    with open(f'player_{player_id}_analysis.html', 'w') as file:
        file.write(html_output)
    
    print(f"Analysis complete. Check player_{player_id}_analysis.html for the report.")

if __name__ == "__main__":
    generate_report()