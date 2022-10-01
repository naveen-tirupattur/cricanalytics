import pandas as pd

from data_provider.match import Match
from winpredictor.main import *
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# download_from_cricinfo('data/t20s_male_json', 'data/cricinfo')
# m = Match('1310947', 'data', False)
# m = Match('682941', 'data', False)
# md = MatchData(m)
# print(vars(md))

matches_data = Main.prepare_data('data', 't20s_male_json')
matches_df = pd.DataFrame()
for match_data in matches_data:
    match_df = pd.DataFrame([vars(match_data)])
    matches_df = pd.concat([matches_df, match_df], ignore_index=True, axis=0)

matches_df = matches_df[matches_df['match_winner'].notnull()]
for col in matches_df.columns:
    if matches_df[col].isnull().values.any():
        print(col)
        print(matches_df[col].isnull().sum())

matches_df = matches_df.fillna(0)
matches_X = matches_df.drop(['id', 'tie_breaker', 'match_result', 'match_winner'], axis=1)
matches_Y = matches_df['match_winner']

# Use one-hot encoding for Categorical values in independent variable
X = matches_X.astype({'target_overs': 'float64'})
X.dtypes
X = pd.get_dummies(X, ['venue', 'country_name', 'town_name',
                       'match_start_time_type', 'team_1_name', 'team_2_name',
                       'home_team', 'toss_winner', 'batting_first'], drop_first=True)
# Encode the dependent variable
le = LabelEncoder()
y = le.fit_transform(matches_Y)

# Create test, training data splits
x_train, x_test, y_train, y_test = train_test_split(X, y, train_size=0.8)

model = LogisticRegression(random_state=0)
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
ac = accuracy_score(y_pred, y_test)


# print(lm.score(x_test, y_test))