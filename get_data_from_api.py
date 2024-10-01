import pandas as pd
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

#region in case of finals
def get_finals_df(desired_year, career, desired_player_id):
    finals_df = pd.DataFrame()
    
    if desired_year == None:
        all_years = career["SEASON_ID"].to_numpy().tolist()
    else:
        all_years = [desired_year]
        
    for year in all_years:
        data_response = shotchartdetail.ShotChartDetail(
        team_id = 0,
        player_id = desired_player_id,
        context_measure_simple = "FGA",
        season_nullable = year,
        season_type_all_star = "Playoffs"
        )

        new_df = data_response.get_data_frames()[0]
        
        if len(new_df) > 0:
            if len(pd.unique(new_df["VTM"])) >= 5:
                player_team = career.TEAM_ABBREVIATION[1]
                finals_team1 = new_df.HTM[len(new_df)-1]
                finals_team2 = new_df.VTM[len(new_df)-1]
                if player_team == finals_team1:
                    opp_team = finals_team2
                else:
                    opp_team = finals_team1
                new_df1 = new_df[new_df.HTM == opp_team]
                new_df2 = new_df[new_df.VTM == opp_team]
                new_df3 = pd.concat([new_df1, new_df2], axis=0)
                finals_df = pd.concat([finals_df,new_df3], axis=0)
                
    return finals_df
#endregion

#region regular data
def get_regular_data(desired_year, desired_player_id, career, desired_games):
    finals_df = pd.DataFrame()
    
    if desired_year == None:
        all_years = career["SEASON_ID"].to_numpy().tolist()
    else:
        all_years = [desired_year]
    
    for year in all_years:
        response = shotchartdetail.ShotChartDetail(
                team_id = 0,
                player_id = desired_player_id,
                context_measure_simple = "FGA",
                season_nullable = year,
                season_type_all_star = desired_games
        )
        shots_df = response.get_data_frames()[0]
        final_df = pd.concat([finals_df,shots_df], axis = 0)
    
    return final_df
#endregion

#region all data
def get_all_data(desired_player_id,desired_year,career):
    final_df = pd.DataFrame()
    
    if desired_year == None:
        all_years = career["SEASON_ID"].to_numpy().tolist()
    else:
        all_years = [desired_year]
    
    for year in all_years:
        response = shotchartdetail.ShotChartDetail(
                team_id = 0,
                player_id = desired_player_id,
                context_measure_simple = "FGA",
                season_nullable = year,
                season_type_all_star = "Regular Season"
        )
        shots_df1 = response.get_data_frames()[0]
        
        response = shotchartdetail.ShotChartDetail(
                team_id = 0,
                player_id = desired_player_id,
                context_measure_simple = "FGA",
                season_nullable = year,
                season_type_all_star = "Playoffs"
        )
        shots_df2 = response.get_data_frames()[0]
        
        shots_df = pd.concat([shots_df1,shots_df2], axis = 0)
        final_df = pd.concat([final_df,shots_df], axis = 0)
    
    return final_df
#endregion