import json
import requests
from bs4 import BeautifulSoup
from espncricinfo.exceptions import MatchNotFoundError, NoScorecardError
import os
import pandas as pd
import re
import logging as log


class Match(object):

    def __init__(self, match_id, input_path=None, download=True):
        self.match_id = match_id
        self.match_url = "https://www.espncricinfo.com/matches/engine/match/{0}.html".format(str(match_id))
        self.json_url = "https://www.espncricinfo.com/matches/engine/match/{0}.json".format(str(match_id))
        self.download = download
        self.input_path = input_path
        self.json = self.get_json()
        self.html = self.get_html()
        self.cric_sheet_data = self.get_cric_sheet_data()
        self.comms_json = self.get_comms_json()
        if self.json:
            self.__unicode__ = self._description()
            self.status = self._status()
            self.match_class = self._match_class()
            self.season = self._season()
            self.description = self._description()
            self.legacy_scorecard_url = self._legacy_scorecard_url()
            self.series = self._series()
            self.series_name = self._series_name()
            self.series_id = self._series_id()
            self.event_url = "http://core.espnuk.org/v2/sports/cricket/leagues/{0}/events/{1}".format(
                str(self.series_id), str(match_id))
            self.details_url = self._details_url()
            self.officials = self._officials()
            self.current_summary = self._current_summary()
            self.present_datetime_local = self._present_datetime_local()
            self.present_datetime_gmt = self._present_datetime_gmt()
            self.start_datetime_local = self._start_datetime_local()
            self.start_datetime_gmt = self._start_datetime_gmt()
            self.cancelled_match = self._cancelled_match()
            self.rain_rule = self._rain_rule()
            self.dl_applied = self._is_dl_applied()
            self.date = self._date()
            self.continent = self._continent()
            self.country_name = self._country_name()
            self.town_area = self._town_area()
            self.town_name = self._town_name()
            self.town_id = self._town_id()
            self.weather_location_code = self._weather_location_code()
            self.match_title = self._match_title()
            self.result = self._result()
            self.result_name = self._result_name()
            self.tie_breaker_name = self._tie_breaker_name()
            self.ground_id = self._ground_id()
            self.ground_name = self._ground_name()
            self.lighting = self._lighting()
            self.followon = self._followon()
            self.scheduled_overs = self._scheduled_overs()
            self.innings_list = self._innings_list()
            self.innings = self._innings()
            self.latest_batting = self._latest_batting()
            self.latest_bowling = self._latest_bowling()
            self.latest_innings = self._latest_innings()
            self.latest_innings_fow = self._latest_innings_fow()
            self.target_runs = self._target_runs()
            self.target_overs = self._target_overs()
            self.team_1 = self._team_1()
            self.team_1_id = self._team_1_id()
            self.team_1_name = self._team_1_name()
            self.team_1_abbreviation = self._team_1_abbreviation()
            self.team_1_players = self._team_1_players()
            self.team_1_innings_num = self._get_innings_num(self.team_1_id)
            self.team_1_innings = self._team_1_innings()
            self.team_1_innings_detailed = self._get_innings_detailed(self.team_1_innings_num)
            self.team_1_runs = self._team_1_runs()
            self.team_1_fours = self.fours(self.team_1_innings_num)
            self.team_1_sixes = self.sixes(self.team_1_innings_num)
            self.team_1_runs_by_over = self._get_runs_by_over(self.team_1_innings_num)
            self.team_1_powerplay_runs = self._get_powerplay_data(self.team_1_innings_num, 'runs')
            self.team_1_non_powerplay_runs = self._get_non_powerplay_data(self.team_1_innings_num, 'runs')
            self.team_1_runs_overs_6_to_9 = self._get_agg_scores(self.team_1_innings_num, 'runs', 6, 9)
            self.team_1_runs_overs_10_to_14 = self._get_agg_scores(self.team_1_innings_num, 'runs', 10, 14)
            self.team_1_runs_overs_15_to_19 = self._get_agg_scores(self.team_1_innings_num, 'runs', 15, 19)
            self.team_1_run_rate = self._team_1_run_rate()
            self.team_1_balls_batted = self._team_1_balls_batted()
            self.team_1_overs_batted = self._team_1_overs_batted()
            self.team_1_batting_result = self._team_1_batting_result()
            self.team_2 = self._team_2()
            self.team_2_id = self._team_2_id()
            self.team_2_name = self._team_2_name()
            self.team_2_abbreviation = self._team_2_abbreviation()
            self.team_2_players = self._team_2_players()
            self.team_2_innings_num = self._get_innings_num(self.team_2_id)
            self.team_2_innings = self._team_2_innings()
            self.team_2_innings_detailed = self._get_innings_detailed(self.team_2_innings_num)
            self.team_2_runs = self._team_2_runs()
            self.team_2_fours = self.fours(self.team_2_innings_num)
            self.team_2_sixes = self.sixes(self.team_2_innings_num)
            self.team_2_runs_by_over = self._get_runs_by_over(self.team_2_innings_num)
            self.team_2_powerplay_runs = self._get_powerplay_data(self.team_2_innings_num, 'runs')
            self.team_2_non_powerplay_runs = self._get_non_powerplay_data(self.team_2_innings_num, 'runs')
            self.team_2_runs_overs_6_to_9 = self._get_agg_scores(self.team_2_innings_num, 'runs', 6, 9)
            self.team_2_runs_overs_10_to_14 = self._get_agg_scores(self.team_2_innings_num, 'runs', 10, 14)
            self.team_2_runs_overs_15_to_19 = self._get_agg_scores(self.team_2_innings_num, 'runs', 15, 19)
            self.team_2_run_rate = self._team_2_run_rate()
            self.team_2_balls_batted = self._team_2_balls_batted()
            self.team_2_overs_batted = self._team_2_overs_batted()
            self.team_2_batting_result = self._team_2_batting_result()
            self.team_1_byes = self._byes(self.team_2_innings_num)
            self.team_1_legbyes = self._legbyes(self.team_2_innings_num)
            self.team_1_wides = self._wides(self.team_2_innings_num)
            self.team_1_noballs = self._noballs(self.team_2_innings_num)
            self.team_1_wickets = self._team_1_wickets()
            self.team_1_wickets_by_over = self._get_wickets_by_over(self.team_2_innings_num)
            self.team_1_powerplay_wickets = self._get_powerplay_data(self.team_2_innings_num, 'wickets')
            self.team_1_non_powerplay_wickets = self._get_non_powerplay_data(self.team_2_innings_num, 'wickets')
            self.team_1_wickets_overs_6_to_9 = self._get_agg_scores(self.team_2_innings_num, 'wickets', 6, 9)
            self.team_1_wickets_overs_10_to_14 = self._get_agg_scores(self.team_2_innings_num, 'wickets', 10, 14)
            self.team_1_wickets_overs_15_to_19 = self._get_agg_scores(self.team_2_innings_num, 'wickets', 15, 19)
            self.team_1_maidens = self._get_maidens(self.team_2_innings_num)
            self.team_2_byes = self._byes(self.team_1_innings_num)
            self.team_2_legbyes = self._legbyes(self.team_1_innings_num)
            self.team_2_wides = self._wides(self.team_1_innings_num)
            self.team_2_noballs = self._noballs(self.team_1_innings_num)
            self.team_2_wickets = self._team_2_wickets()
            self.team_2_wickets_by_over = self._get_wickets_by_over(self.team_1_innings_num)
            self.team_2_powerplay_wickets = self._get_powerplay_data(self.team_1_innings_num, 'wickets')
            self.team_2_non_powerplay_wickets = self._get_non_powerplay_data(self.team_1_innings_num, 'wickets')
            self.team_2_wickets_overs_6_to_9 = self._get_agg_scores(self.team_1_innings_num, 'wickets', 6, 9)
            self.team_2_wickets_overs_10_to_14 = self._get_agg_scores(self.team_1_innings_num, 'wickets', 10, 14)
            self.team_2_wickets_overs_15_to_19 = self._get_agg_scores(self.team_1_innings_num, 'wickets', 15, 19)
            self.team_2_maidens = self._get_maidens(self.team_1_innings_num)
            if not self.status == 'dormant':
                self.home_team = self._home_team()
                self.batting_first = self._batting_first()
                self.match_winner = self._match_winner()
                self.win_by_runs = self._win_by_runs()
                self.win_by_wickets = self._win_by_wickets()
                self.toss_winner = self._toss_winner()
                self.toss_decision = self._toss_decision()
                self.toss_decision_name = self._toss_decision_name()
                self.toss_choice_team_id = self._toss_choice_team_id()
                self.toss_winner_team_id = self._toss_winner_team_id()
                self.espn_api_url = self._espn_api_url()
                # from comms_json
                self.rosters = self._rosters()
                self.all_innings = self._all_innings()

    def __str__(self):
        return self.description

    def __repr__(self):
        return (f'{self.__class__.__name__}('f'{self.match_id!r})')

    def _read_file(self, data_dir, extension):
        root_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        with open(os.path.join(root_dir, self.input_path, data_dir, self.match_id + '.' + extension)) as file:
            content = file.read()
            log.debug('Finished reading file: {}'.format(file.name))
            file.close()
            return content

    def get_cric_sheet_data(self):
        if self.input_path is not None:
            return json.loads(self._read_file('t20s_male_json', 'json'))

    def get_json(self):
        if not self.download:
            return json.loads(self._read_file('cricinfo', 'json'))
        else:
            r = requests.get(self.json_url)
            if r.status_code == 404:
                raise MatchNotFoundError
            elif 'Scorecard not yet available' in r.text:
                raise NoScorecardError
            else:
                return r.json()

    def get_html(self):
        if not self.download:
            return BeautifulSoup(self._read_file('cricinfo', 'html'), 'html.parser')
        else:
            r = requests.get(self.match_url)
            if r.status_code == 404:
                raise MatchNotFoundError
            else:
                return BeautifulSoup(r.text, 'html.parser')

    def match_json(self):
        return self.json['match']

    def innings_comms_url(self, innings=1, page=1):
        return f"https://hsapi.espncricinfo.com/v1/pages/match/comments?lang=en&leagueId={self.series_id}&eventId={self.match_id}&period={innings}&page={page}&filter=full&liveTest=false"

    def get_comms_json(self):
        try:
            text = self.html.find_all('script')[38].string
            return json.loads(text)
        except:
            return None

    def _espn_api_url(self):
        return "https://site.api.espn.com/apis/site/v2/sports/cricket/{0}/summary?event={1}".format(self.series_id,
                                                                                                    self.match_id)

    def _legacy_scorecard_url(self):
        return "https://static.espncricinfo.com" + self.match_json()['legacy_url']

    def _details_url(self, page=1, number=1000):
        return self.event_url + "/competitions/{0}/details?page_size={1}&page={2}".format(str(self.match_id),
                                                                                          str(number), str(page))

    def __str__(self):
        return self.json['description']

    def __unicode__(self):
        return self.json['description']

    def _status(self):
        return self.match_json()['match_status']

    def _match_class(self):
        if self.match_json()['international_class_card'] != "":
            return self.match_json()['international_class_card']
        else:
            return self.match_json()['general_class_card']

    def _season(self):
        return self.match_json()['season']

    def _description(self):
        return self.json['description']

    def _series(self):
        return self.json['series']

    def _series_name(self):
        try:
            return self.json['series'][-1]['series_name']
        except:
            return None

    def _series_id(self):
        return self.json['series'][-1]['core_recreation_id']

    def _officials(self):
        return self.json['official']

    # live matches only
    def _current_summary(self):
        return self.match_json().get('current_summary')

    def _present_datetime_local(self):
        return self.match_json()['present_datetime_local']

    def _present_datetime_gmt(self):
        return self.match_json()['present_datetime_gmt']

    def _start_datetime_local(self):
        return self.match_json()['start_datetime_local']

    def _start_datetime_gmt(self):
        return self.match_json()['start_datetime_gmt_raw']

    def _cancelled_match(self):
        if self.match_json()['cancelled_match'] == 'N':
            return False
        else:
            return True

    def _rain_rule(self):
        if self.match_json().get('rain_rule') == "1":
            return self.match_json()['rain_rule_name']
        else:
            return None

    def _is_dl_applied(self):
        return not self.rain_rule is None

    def _date(self):
        return self.match_json()['start_date_raw']

    def _continent(self):
        return self.match_json().get('continent_name')

    def _country_name(self):
        return self.match_json().get('country_name')

    def _town_area(self):
        return self.match_json().get('town_area')

    def _town_name(self):
        return self.match_json().get('town_name')

    def _town_id(self):
        return self.match_json().get('town_id')

    def _weather_location_code(self):
        return self.match_json().get('weather_location_code')

    def _match_title(self):
        return self.match_json()['cms_match_title']

    def _result(self):
        return self.json['live']['status']

    def _result_name(self):
        return self.match_json()['result_name']

    def _tie_breaker_name(self):
        return self.match_json()['tiebreaker_name'] if not self.match_json()['tiebreaker_name'] == '' else None

    def _ground_id(self):
        return self.match_json()['ground_id']

    def _ground_name(self):
        return self.match_json()['ground_name']

    def _lighting(self):
        return self.match_json()['floodlit_name']

    def _followon(self):
        if self.match_json().get('followon') == '1':
            return True
        else:
            return False

    def _scheduled_overs(self):
        try:
            return int(self.match_json()['scheduled_overs'])
        except:
            return None

    def _innings_list(self):
        try:
            return self.json['centre']['common']['innings_list']
        except:
            return None

    def _innings(self):
        return self.json['innings']

    def _latest_batting(self):
        try:
            return self.json['centre']['common']['batting']
        except:
            return None

    def _latest_bowling(self):
        try:
            return self.json['centre']['common']['bowling']
        except:
            return None

    def _latest_innings(self):
        try:
            return self.json['centre']['common']['innings']
        except:
            return None

    def _latest_innings_fow(self):
        return self.json['centre'].get('fow')

    def _get_innings(self, innings):
        try:
            # return [inn for inn in self.json['innings'] if str(inn['batting_team_id']) == team_id][0]
            return self.json['innings'][innings]
        except:
            return None

    def _get_innings_num(self, team_id):
        return [i for i, inn in enumerate(self.json['innings']) if str(inn['batting_team_id']) == team_id][0]

    def _get_innings_detailed(self, innings):
        if self.cric_sheet_data is None or (len(self.cric_sheet_data['innings']) - 1) < innings:
            return None
        else:
            return self.cric_sheet_data['innings'][innings]

    def _team_1(self):
        return self.json['team'][0]

    def _team_1_id(self):
        return self._team_1()['team_id']

    def _team_1_name(self):
        return self._team_1()['team_name']

    def _team_1_abbreviation(self):
        return self._team_1()['team_abbreviation']

    def _team_1_players(self):
        return self._team_1().get('player', [])

    def _team_1_innings(self):
        return self._get_innings(self.team_1_innings_num)

    def _team_1_runs(self):
        return int(self.team_1_innings['runs'])

    def _team_1_run_rate(self):
        try:
            return float(self._team_1_innings()['run_rate'])
        except:
            return None

    def _team_1_overs_batted(self):
        try:
            return float(self._team_1_innings()['overs'])
        except:
            return None

    def _team_1_balls_batted(self):
        return self._team_1_innings()['balls']

    def _team_1_batting_result(self):
        try:
            return self._team_1_innings()['event_name']
        except:
            return None

    def _team_2(self):
        return self.json['team'][1]

    def _team_2_id(self):
        return self._team_2()['team_id']

    def _team_2_name(self):
        return self._team_2()['team_name']

    def _team_2_abbreviation(self):
        return self._team_2()['team_abbreviation']

    def _team_2_players(self):
        return self._team_2().get('player', [])

    def _team_2_runs(self):
        return int(self.team_2_innings['runs'])

    def _team_2_innings(self):
        return self._get_innings(self.team_2_innings_num)

    def _team_2_run_rate(self):
        try:
            return float(self._team_2_innings()['run_rate'])
        except:
            return None

    def _team_2_balls_batted(self):
        return self._team_2_innings()['balls']

    def _team_2_overs_batted(self):
        try:
            return float(self._team_2_innings()['overs'])
        except:
            return None

    def _team_2_batting_result(self):
        try:
            return self._team_2_innings()['event_name']
        except:
            return None

    def _team_1_wickets(self):
        return int(self.team_2_innings['wickets'])

    def _team_2_wickets(self):
        return int(self.team_1_innings['wickets'])

    def _wides(self, innings):
        return int(self._get_innings(innings)['wides'])

    def _byes(self, innings):
        return int(self._get_innings(innings)['byes'])

    def _noballs(self, innings):
        return int(self._get_innings(innings)['noballs'])

    def _legbyes(self, innings):
        return int(self._get_innings(innings)['legbyes'])

    def _home_team(self):
        if self._team_1_id() == self.match_json()['home_team_id']:
            return self.team_1_name
        else:
            return self.team_2_name

    def _batting_first(self):
        if self._team_1_id() == self.match_json()['batting_first_team_id']:
            return self.team_1_name
        else:
            return self.team_2_name

    def _outcome(self):
        if self.cric_sheet_data is not None:
            return self.cric_sheet_data['info']['outcome']

    def _match_winner(self):
        if self._outcome() is None:
            return None

        if 'winner' in self._outcome():
            return self._outcome()['winner']
        elif 'bowl_out' in self._outcome():
            return self._outcome()['bowl_out']
        elif 'eliminator' in self._outcome():
            return self._outcome()['eliminator']
        else:
            return None

    def _target(self):
        if self.cric_sheet_data is None or len(self.cric_sheet_data['innings']) == 1:
            return None
        elif 'target' in self.cric_sheet_data['innings'][1]:
            return self.cric_sheet_data['innings'][1]['target']

    def _target_runs(self):
        if not self._target() is None:
            return self._target()['runs']

    def _target_overs(self):
        if not self._target() is None:
            return self._target()['overs']

    def _win_by_wickets(self):
        if self._outcome() is not None and 'by' in self._outcome():
            if 'wickets' in self._outcome()['by']:
                return int(self._outcome()['by']['wickets'])

    def _win_by_runs(self):
        if self._outcome() is not None and 'by' in self._outcome():
            if 'runs' in self._outcome()['by']:
                return int(self._outcome()['by']['runs'])

    def _toss_winner(self):
        if self._team_1_id() == self.match_json()['toss_winner_team_id']:
            return self.team_1_name
        else:
            return self.team_2_name

    def _toss_decision(self):
        if self.match_json()['toss_decision'] == '' and len(self.innings) > 0:
            if self.innings[0]['batting_team_id'] == self.toss_winner:
                decision = '1'
            else:
                decision = '2'
        else:
            decision = self.match_json()['toss_decision']
        return decision

    def _toss_decision_name(self):
        if self.match_json()['toss_decision_name'] == '' and len(self.innings) > 0:
            if self.innings[0]['batting_team_id'] == self.toss_winner:
                decision_name = 'bat'
            else:
                decision_name = 'bowl'
        else:
            decision_name = self.match_json()['toss_decision_name']
        return decision_name

    def _toss_choice_team_id(self):
        return self.match_json()['toss_choice_team_id']

    def _toss_winner_team_id(self):
        return self.match_json()['toss_winner_team_id']

    # comms_json methods

    def _rosters(self):
        try:
            return self.comms_json['props']['appPageProps']['data']['content']['matchPlayers']
        except:
            return None

    def _all_innings(self):
        try:
            return self.comms_json['props']['appPageProps']['data']['content']['scorecard']['innings']
        except:
            return self.json['innings']

    def _overs(self, innings):
        return float(self._get_innings(innings)['overs'])

    def batsmen(self, innings):
        try:
            return self.comms_json['props']['appPageProps']['data']['content']['scorecard']['innings'][innings][
                'inningBatsmen']
        except:
            return None

    def fours(self, innings):
        if self.batsmen(innings) is None:
            return 0
        count = 0
        for batsman in self.batsmen(innings):
            if not batsman['fours'] is None:
                count = count + batsman['fours']
        return count

    def sixes(self, innings):
        if self.batsmen(innings) is None:
            return 0
        count = 0
        for batsman in self.batsmen(innings):
            if not batsman['sixes'] is None:
                count = count + batsman['sixes']
        return count

    def bowlers(self, innings):
        try:
            return self.comms_json['props']['appPageProps']['data']['content']['scorecard']['innings'][innings][
                'inningBowlers']
        except:
            return None

    def extras(self, innings):
        try:
            return self.comms_json['props']['appPageProps']['data']['content']['scorecard']['innings'][innings][
                'extras']
        except:
            return None

    def fows(self, innings):
        try:
            return self.comms_json['props']['appPageProps']['data']['content']['scorecard']['innings'][innings][
                'inningFallOfWickets']
        except:
            return None

    def _powerplays(self, innings):
        if not self._get_innings_detailed(innings) is None and 'powerplays' in self._get_innings_detailed(innings):
            return self._get_innings_detailed(innings)['powerplays']

    # TODO - This code will work for T20s only. Modify this to work for other formats
    def _powerplay_start(self, innings):
        if not self._powerplays(innings) is None:
            return int(self._powerplays(innings)[0]['from'])

    def _powerplay_end(self, innings):
        if not self._powerplays(innings) is None:
            return int(self._powerplays(innings)[0]['to'])

    def _get_runs_by_over(self, innings):
        if self._get_scores_by_over(innings) is None:
            return None
        else:
            return self._get_scores_by_over(innings)['runs']

    def _get_wickets_by_over(self, innings):
        if self._get_scores_by_over(innings) is None:
            return None
        else:
            return self._get_scores_by_over(innings)['wickets']

    def _get_non_powerplay_data(self, innings, key):
        start = self._powerplay_end(innings)
        if start is not None:
            start = start + 1
            end = int(self._overs(innings))
            return self._get_agg_scores(innings, key, start, end)

    def _get_powerplay_data(self, innings, key):
        start = self._powerplay_start(innings)
        end = self._powerplay_end(innings)
        return self._get_agg_scores(innings, key, start, end)

    def _get_agg_scores(self, innings, key, start, end):
        if start is None or end is None:
            return 0
        else:
            scores = self._get_scores_by_over(innings)
            if scores is not None and key in scores:
                count = 0
                for i in range(start, end + 1):
                    if i in scores[key]:
                        count = count + scores[key][i]
                return count
            else:
                return 0

    def _get_scores_by_over(self, innings):
        mp = dict()
        mp['runs'] = dict()
        mp['wickets'] = dict()
        team_innings = self._get_innings_detailed(innings)
        if team_innings is None:
            return None
        for over in team_innings['overs']:
            runs = 0
            wickets = 0
            for delivery in over['deliveries']:
                ov = over['over']
                runs = runs + delivery['runs']['total']
                if 'wickets' in delivery and not delivery['wickets'] is None:
                    for wicket in delivery['wickets']:
                        if not wicket['kind'] == 'retired hurt':
                            wickets = wickets + 1
            mp['runs'][ov] = runs
            mp['wickets'][ov] = wickets
        return mp

    def _get_maidens(self, innings):
        if self.bowlers(innings) is None:
            return 0
        count = 0
        for bowler in self.bowlers(innings):
            if not bowler['maidens'] is None:
                count = count + bowler['maidens']
        return count

    # HTML Parsed Code
    def _get_batting_card(self):
        table_body = self.html.find_all('tbody')
        batsmen_df = pd.DataFrame(columns=["Name", "Desc", "Runs", "Minutes", "Balls", "4s", "6s", "SR", "Team"])
        for i, table in enumerate(table_body[0:4:2]):
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [x.text.strip() for x in cols]
                if len(cols) == 8:
                    batsmen_card = pd.Series(
                        [re.sub(r"\W+", ' ', cols[0].split("(c)")[0]).strip(), cols[1],
                         cols[2], cols[3], cols[4], cols[5], cols[6], cols[7], i + 1],
                        index=batsmen_df.columns)
                    batsmen_df = pd.concat([batsmen_df, batsmen_card.to_frame().T], ignore_index=True)
                else:
                    continue

        return batsmen_df

    def _get_bowling_card(self):
        table_body = self.html.find_all('tbody')
        bowler_df = pd.DataFrame(columns=['Name', 'Overs', 'Maidens', 'Runs', 'Wickets',
                                          'Econ', 'Dots', '4s', '6s', 'Wd', 'Nb', 'Team'])
        for i, table in enumerate(table_body[1:4:2]):
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [x.text.strip() for x in cols]
                if len(cols) == 11:
                    bowler_card = pd.Series([cols[0], cols[1], cols[2], cols[3], cols[4], cols[5],
                                             cols[6], cols[7], cols[8], cols[9], cols[10], (i == 0) + 1],
                                            index=bowler_df.columns)
                    bowler_df = pd.concat([bowler_df, bowler_card.to_frame().T], ignore_index=True)
                else:
                    continue

        return bowler_df

    def _get_dnb(self):
        # TODO - Implement this
        return None

    def _get_dismissals(self):
        # TODO - Implement this
        return None

    @staticmethod
    def get_recent_matches(date=None):
        if date:
            url = "https://www.espncricinfo.com/ci/engine/match/index.html?date=%sview=week" % date
        else:
            url = "https://www.espncricinfo.com/ci/engine/match/index.html?view=week"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return [x['href'].split('/', 4)[4].split('.')[0] for x in soup.findAll('a', href=True, text='Scorecard')]

    @staticmethod
    def get_match():
        return Match('1310947', 'data', False)
