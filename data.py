import pandas as pd

def load_data():
    matches_df = pd.read_parquet('data_source/prod/matches.parquet')
    players_df = pd.read_parquet('data_source/prod/match_players.parquet')
    
    # Rename columns to reflect correct understanding
    players_df.rename(columns={
        'new_skill': 'mu',  # 'new_skill' is actually mu
        'new_uncertainty': 'sigma'  # 'new_uncertainty' is sigma
    }, inplace=True)
    
    # Calculate match_rating
    players_df['match_rating'] = players_df['mu'] - players_df['sigma']
    
    # Convert start_time to datetime if it's not already
    matches_df['start_time'] = pd.to_datetime(matches_df['start_time'])
    
    # Calculate game duration if not present
    if 'game_duration' not in matches_df.columns:
        matches_df['game_duration'] = (matches_df['end_time'] - matches_df['start_time']).dt.total_seconds()
    
    return matches_df, players_df

def get_player_data(players_df, matches_df, player_id):
    player_matches = players_df[players_df['user_id'] == player_id]
    player_matches = player_matches.merge(matches_df, on='match_id')
    
    ranked_team_matches = player_matches[
        (player_matches['is_ranked'] == True) & 
        (
            (player_matches['game_type'].str.contains('Large Team')) |
            (player_matches['game_type'].str.contains('Small Team')) |
            (player_matches['game_type'] == 'Team')
        ) &
        (~player_matches['game_type'].str.contains('Team FFA'))
    ]
    
    ranked_team_matches = ranked_team_matches.sort_values('start_time')
    
    # Get match ratings of all players in these matches, applying the same filter
    all_players_in_matches = players_df[players_df['match_id'].isin(ranked_team_matches['match_id'])]
    all_players_in_matches = all_players_in_matches.merge(matches_df[['match_id', 'game_type', 'is_ranked']], on='match_id')
    filtered_players = all_players_in_matches[
        (all_players_in_matches['is_ranked'] == True) & 
        (
            (all_players_in_matches['game_type'].str.contains('Large Team')) |
            (all_players_in_matches['game_type'].str.contains('Small Team')) |
            (all_players_in_matches['game_type'] == 'Team')
        ) &
        (~all_players_in_matches['game_type'].str.contains('Team FFA'))
    ]
    latest_match_ratings = filtered_players.sort_values('match_id').groupby('user_id').last()['match_rating']
    
    return player_matches, ranked_team_matches, latest_match_ratings

def calculate_weekly_stats(ranked_team_matches):
    ranked_team_matches['week'] = ranked_team_matches['start_time'].dt.to_period('W')
    weekly_stats = ranked_team_matches.groupby('week').agg({
        'match_id': 'count',
        'mu': 'last',
        'match_rating': 'last',
        'sigma': 'last',
        'winning_team': lambda x: (x == ranked_team_matches.loc[x.index, 'team_id']).sum(),
        'team_id': 'count'
    }).reset_index()
    
    weekly_stats['skill_change'] = weekly_stats['mu'].diff()
    weekly_stats['cumulative_matches'] = weekly_stats['match_id'].cumsum()
    weekly_stats['losses'] = weekly_stats['team_id'] - weekly_stats['winning_team']
    
    return weekly_stats
def calculate_monthly_stats(ranked_team_matches):
    ranked_team_matches['month'] = ranked_team_matches['start_time'].dt.to_period('M')
    monthly_stats = ranked_team_matches.groupby('month').agg({
        'match_id': 'count',
        'mu': 'last',
        'match_rating': 'last',
        'sigma': 'last',
        'winning_team': lambda x: (x == ranked_team_matches.loc[x.index, 'team_id']).sum(),
        'team_id': 'count'
    }).reset_index()
    
    monthly_stats['skill_change'] = monthly_stats['mu'].diff()
    monthly_stats['cumulative_matches'] = monthly_stats['match_id'].cumsum()
    monthly_stats['losses'] = monthly_stats['team_id'] - monthly_stats['winning_team']
    
    return monthly_stats

def get_latest_skills(players_df):
    return players_df.sort_values('match_id').groupby('user_id').last()['mu']