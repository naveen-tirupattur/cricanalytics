import json
import os
from src.cricanalytics.download import Download
from espncricinfo.match import Match
import pandas as pd
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../..'))


def download_from_cricinfo(input_path, output_path):
    data_files = os.path.join(ROOT_DIR, input_path)
    i = 0
    for dirname, _, filenames in os.walk(data_files):
        for filename in filenames:
            # print(os.path.join(dirname, filename))
            with open(os.path.join(dirname, filename)) as file:
                if filename.endswith('.json'):
                    i = i + 1
                    data = json.loads(file.read())
                    match_id = filename.rsplit(".", 1)[0]
                    print(match_id)
                    print("Downloading file #{} for match {}".format(i, match_id))
                    Download(match_id, os.path.join(ROOT_DIR, output_path, match_id))
                    data['info']['filename'] = filename
    print('Total Files: ', i)


class MatchData(object):
    def __init__(self, match):
        self.id = match.match_id
        self.venue = match.ground_name
        self.country_name = match.country_name
        self.town_name = match.town_name
        self.start_datetime_gmt = match.start_datetime_gmt
        self.match_type = match.lighting
        self.description = match.description
        self.team_1_id = match.team_1_id
        self.team_1_name = match.team_1_name
        self.team_2_id = match.team_2_id
        self.team_2_name = match.team_2_name
        self.home_team = match.home_team
        self.toss_winner = match.toss_winner
        self.batting_first = match.batting_first
        self.match_winner = match.match_winner
        self.match_result = match.result_name
        self.tie_breaker = match.tie_breaker_name
        self.win_by_runs = match.win_by_runs
        self.win_by_wickets = match.win_by_wickets
        self.dl_applied = match.dl_applied
        self.target_runs = match.target_runs
        self.target_overs = match.target_overs
        self.team_1_runs = match.team_1_runs
        self.team_1_fours = match.team_1_fours
        self.team_1_sixes = match.team_1_sixes
        self.team_1_balls_batted = match.team_1_balls_batted
        self.team_1_runrate = match.team_1_run_rate
        self.team_1_powerplay_runs = match.team_1_powerplay_runs
        self.team_1_non_powerplay_runs = match.team_1_non_powerplay_runs
        self.team_1_runs_overs_6_to_9 = match.team_1_runs_overs_6_to_9
        self.team_1_runs_overs_10_to_14 = match.team_1_runs_overs_10_to_14
        self.team_1_runs_overs_15_to_19 = match.team_1_runs_overs_15_to_19
        self.team_1_wickets = match.team_1_wickets
        self.team_1_wides = match.team_1_wides
        self.team_1_byes = match.team_1_byes
        self.team_1_noballs = match.team_1_noballs
        self.team_1_legbyes = match.team_1_legbyes
        self.team_1_maidens = match.team_1_maidens
        self.team_1_powerplay_wickets = match.team_1_powerplay_wickets
        self.team_1_non_powerplay_wickets = match.team_1_non_powerplay_wickets
        self.team_1_runs_wickets_6_to_9 = match.team_1_wickets_overs_6_to_9
        self.team_1_runs_wickets_10_to_14 = match.team_1_wickets_overs_10_to_14
        self.team_1_runs_wickets_15_to_19 = match.team_1_wickets_overs_15_to_19
        self.team_2_runs = match.team_2_runs
        self.team_2_fours = match.team_2_fours
        self.team_2_sixes = match.team_2_sixes
        self.team_2_balls_batted = match.team_2_balls_batted
        self.team_2_runrate = match.team_2_run_rate
        self.team_2_powerplay_runs = match.team_2_powerplay_runs
        self.team_2_non_powerplay_runs = match.team_2_non_powerplay_runs
        self.team_2_runs_overs_6_to_9 = match.team_2_runs_overs_6_to_9
        self.team_2_runs_overs_10_to_14 = match.team_2_runs_overs_10_to_14
        self.team_2_runs_overs_15_to_19 = match.team_2_runs_overs_15_to_19
        self.team_2_wickets = match.team_2_wickets
        self.team_2_wides = match.team_2_wides
        self.team_2_byes = match.team_2_byes
        self.team_2_noballs = match.team_2_noballs
        self.team_2_legbyes = match.team_2_legbyes
        self.team_2_maidens = match.team_2_maidens
        self.team_2_powerplay_wickets = match.team_2_powerplay_wickets
        self.team_2_non_powerplay_wickets = match.team_2_non_powerplay_wickets
        self.team_2_runs_wickets_6_to_9 = match.team_2_wickets_overs_6_to_9
        self.team_2_runs_wickets_10_to_14 = match.team_2_wickets_overs_10_to_14
        self.team_2_runs_wickets_15_to_19 = match.team_2_wickets_overs_15_to_19


# download_from_cricinfo('data/t20s_male_json', 'data/cricinfo')
# m = Match('1310947', 'data', False)
m = Match('1263166', 'data', False)
md = MatchData(m)
print(vars(md))


def read_data(input_dir, cricsheet_dir):
    file_names_list = []
    matches_data = []
    i = 1
    data_files = os.path.join(ROOT_DIR, input_dir, cricsheet_dir)
    for dirname, _, filenames in os.walk(data_files):
        for filename in filenames:
            if filename.endswith('.json'):
                match_id = filename.rsplit(".", 1)[0]
                match = Match(match_id, input_dir, False)
                matches_data.append(MatchData(match))
                print('total files read', i)
                i = i + 1
    return matches_data


df_match = pd.DataFrame(read_data('data', 't20s_male_json'))

