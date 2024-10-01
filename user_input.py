import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from get_data_from_api import get_finals_df, get_regular_data, get_all_data

def collect_data():
    nba_players = players.get_players()
    all_players = pd.DataFrame(nba_players)
    all_players = all_players["full_name"].tolist()

    player_wanted = input("Enter the full name of an NBA player: ")

    while(True):
        if player_wanted in all_players:
            desired_player = [player for player in nba_players
                            if player['full_name'] == player_wanted][0]
            desired_player_id = desired_player["id"]
            break
        else:
            player_wanted = input("Please enter a valid player name: ")
        
    career = playercareerstats.PlayerCareerStats(player_id = desired_player_id)
    career = career.get_data_frames()[0]
    career_years = career["SEASON_ID"].tolist()
    career_years.append("Career")

    desired_year = input("Enter the years you want stats from (ex: 2015-16) or Career for entire career: ")

    while(True):
        if desired_year in career_years:
            desired_year = desired_year
            break
        else:
            desired_year = input("Please enter a valid season: ")

    title = player_wanted + " " + desired_year + " Shot Map"

    if desired_year == "Career":
        desired_year = None

    desired_games = input("Enter game type: (Regular Season, Playoffs, Finals, Pre Season, or All Star): ")

    while(True):
        if desired_games in ["Pre Season", "Regular Season", "All Star", "Playoffs", "Finals", "All"]:
            desired_games = desired_games
            break
        else:
            desired_games = input("Please enter a valid game type ")

    if desired_games == "Finals":
        shots_df = get_finals_df(desired_year, career, desired_player_id)
    elif desired_games == "All":
        shots_df = get_all_data(desired_player_id, desired_year, career)
    else:
        shots_df = get_regular_data(desired_year, desired_player_id, career, desired_games)
        
    return shots_df, title