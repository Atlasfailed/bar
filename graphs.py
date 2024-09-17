import plotly.graph_objs as go
from plotly.subplots import make_subplots

def create_plots(weekly_stats, latest_match_ratings, player_id, width=800, height=1200):
    fig = make_subplots(rows=5, cols=1, 
                        shared_xaxes=True, 
                        vertical_spacing=0.07,
                        subplot_titles=('Weekly Matches Played', 'Skill and Match Rating', 'Weekly Skill Change', 
                                        'Weekly Wins and Losses', 'Match Rating Distribution'))
    
    # Weekly Matches Played
    fig.add_trace(go.Bar(x=weekly_stats['week'].astype(str), y=weekly_stats['match_id'], name='Matches Played'),
                  row=1, col=1)
    
    # Skill and Match Rating
    fig.add_trace(go.Scatter(x=weekly_stats['week'].astype(str), y=weekly_stats['mu'], mode='lines+markers', name='Mu (Skill)', marker=dict(size=4)),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=weekly_stats['week'].astype(str), y=weekly_stats['match_rating'], mode='lines+markers', name='Match Rating', marker=dict(size=4)),
                  row=2, col=1)
    
    # Weekly Skill Change
    fig.add_trace(go.Bar(x=weekly_stats['week'].astype(str), y=weekly_stats['skill_change'], name='Skill Change'),
                  row=3, col=1)
    
    # Weekly Wins and Losses
    fig.add_trace(go.Bar(x=weekly_stats['week'].astype(str), y=weekly_stats['winning_team'], 
                         name='Wins', marker_color='green'), row=4, col=1)
    fig.add_trace(go.Bar(x=weekly_stats['week'].astype(str), y=-weekly_stats['losses'], 
                         name='Losses', marker_color='red'), row=4, col=1)
    
    # Skill Distribution
    player_skill = latest_match_ratings[player_id]
    fig.add_trace(go.Histogram(x=latest_match_ratings, name='Filtered Players', nbinsx=30), row=5, col=1)
    fig.add_trace(go.Scatter(x=[player_skill], y=[0], mode='markers', 
                             marker=dict(size=8, color='red'), name=f'Player {player_id}'), row=5, col=1)
    
    # Update layout
    fig.update_layout(height=1800, width=1200, title_text=f"Player {player_id} - Comprehensive Analysis")
    fig.update_xaxes(title_text="Week", row=4, col=1)
    fig.update_xaxes(title_text="Match rating", row=5, col=1)
    fig.update_yaxes(title_text="Matches", row=1, col=1)
    fig.update_yaxes(title_text="Skill / Rating", row=2, col=1)
    fig.update_yaxes(title_text="Skill Change", row=3, col=1)
    fig.update_yaxes(title_text="Wins / Losses", row=4, col=1)
    fig.update_yaxes(title_text="Count", row=5, col=1)
    
    # Reduce the number of ticks on x-axis
    for i in range(1, 5):
        fig.update_xaxes(nticks=10, row=i, col=1)
    
    return fig

def add_stats_annotations(fig, player_matches, percentile):
    overall_stats = [
        f"Total matches: {len(player_matches)}",
        f"Date range: {player_matches['start_time'].min().date()} to {player_matches['start_time'].max().date()}",
        f"Initial mu: {player_matches['mu'].iloc[0]:.2f}",
        f"Final mu: {player_matches['mu'].iloc[-1]:.2f}",
        f"Initial match rating: {player_matches['match_rating'].iloc[0]:.2f}",
        f"Final match rating: {player_matches['match_rating'].iloc[-1]:.2f}",
        f"Overall mu change: {player_matches['mu'].iloc[-1] - player_matches['mu'].iloc[0]:.2f}",
        f"Overall win rate: {(player_matches['winning_team'] == player_matches['team_id']).mean():.2%}",
        f"Skill percentile: {percentile:.2f}%"
    ]
    
    for i, stat in enumerate(overall_stats):
        fig.add_annotation(
            x=1.0, y=1.0 - (i * 0.05),
            xref="paper", yref="paper",
            text=stat,
            showarrow=False,
            font=dict(size=12),
            align="right",
            xanchor="right",
            yanchor="top"
        )
    
    return fig