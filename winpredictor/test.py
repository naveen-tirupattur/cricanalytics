import pandas as pd

from espncricinfo.match import Match
from winpredictor.main import *

# download_from_cricinfo('data/t20s_male_json', 'data/cricinfo')
# m = Match('1310947', 'data', False)
# # m = Match('1263166', 'data', False)
# md = MatchData(m)
# print(vars(md))

matches_data = Main.read_data('data', 't20s_male_json')
matches_df = pd.DataFrame()
for match_data in matches_data:
    match_df = pd.DataFrame([vars(match_data)])
    matches_df = pd.concat([matches_df, match_df], ignore_index = True, axis=0)
