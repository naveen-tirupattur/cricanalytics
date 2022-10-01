import json
import os
from data_provider.match import Match
from winpredictor.matchdata import MatchData
from data_provider.datafetcher import DataFetcher
import logging as log
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


class Main(object):
    # Entry point method to parse cricsheet data and scrape data from espncricinfo
    # This method expects the location of downloaded cricsheet json data
    # More info about cricsheet can be found here: https://cricsheet.org/
    @staticmethod
    def prepare_data(input_dir, cricsheet_data_dir):
        file_names_list = []
        matches_data = []
        i = 1
        data_files = os.path.join(ROOT_DIR, input_dir, cricsheet_data_dir)
        for dirname, _, filenames in os.walk(data_files):
            for filename in filenames:
                if filename.endswith('.json'):
                    with open(os.path.join(dirname, filename)) as file:
                        match_id = filename.rsplit(".", 1)[0]
                        cricsheet_json = json.loads(file.read())
                        # Fetch data from espncricinfo
                        cricinfo_data = DataFetcher(match_id, os.path.join(ROOT_DIR, input_dir))
                        match = Match(match_id, cricinfo_data.json, cricinfo_data.html, cricsheet_json)
                        matches_data.append(MatchData(match))
                        log.debug('total files read', i)
                        i = i + 1
        return matches_data


