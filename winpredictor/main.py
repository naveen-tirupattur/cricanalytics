import json
import os
from espncricinfo.match import Match
from winpredictor.matchdata import MatchData
from winpredictor.download import Download
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

