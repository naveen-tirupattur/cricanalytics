from espncricinfo.match import Match
from winpredictor.main import *

# download_from_cricinfo('data/t20s_male_json', 'data/cricinfo')
m = Match('1310947', 'data', False)
# m = Match('1263166', 'data', False)
md = MatchData(m)
print(vars(md))

df_match = pd.DataFrame(Main.read_data('data', 't20s_male_json'))