import requests
from bs4 import BeautifulSoup
import json
import os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


class DataFetcher(object):
    # This class returns the match data scraped from cricinfo. If the data is not available as a file
    # in the input data directory it scrapes from cricinfo website and writes to files in 'cricinfo' directory
    def __init__(self, match_id, input_path):
        self.match_id = match_id
        self.match_url = "https://www.espncricinfo.com/matches/engine/match/{0}.html".format(str(self.match_id))
        self.json_url = "https://www.espncricinfo.com/matches/engine/match/{0}.json".format(str(match_id))
        self.input_path = input_path
        self.html = self._get_html()
        self.json = self._get_json()

    def _save_data(self):
        print("Writing file for match {}".format(self.match_id))
        self._write("html", self.html.prettify())
        self._write("json", json.dumps(self.json))

    @staticmethod
    def _write(path, data):
        f = open(path, "w")
        f.write(data)
        f.close()

    @staticmethod
    def _read_file(file):
        with open(os.path.join(ROOT_DIR, file)) as file:
            content = file.read()
            print('Finished reading file: {}'.format(file.name))
            file.close()
            return content

    def _get_json(self):
        file = os.path.join(ROOT_DIR, self.input_path, 'cricinfo', self.match_id + '.json')
        if os.path.exists(file):
            return json.loads(self._read_file(file))
        else:
            r = requests.get(self.json_url)
            if r.status_code == 404:
                raise Exception('Invalid URL')
            elif 'Scorecard not yet available' in r.text:
                raise Exception('Score card not yet available')
            else:
                print("Scraping JSON data for match_id: {}".format(self.match_id))
                json_data = r.json()
                self._write(file, json.dumps(json_data))
                return json_data

    def _get_html(self):
        file = os.path.join(ROOT_DIR, self.input_path, 'cricinfo', self.match_id + '.html')
        if os.path.exists(file):
            return BeautifulSoup(self._read_file(file), 'html.parser')
        else:
            r = requests.get(self.match_url)
            if r.status_code == 404:
                raise Exception('Invalid URL')
            else:
                print("Scraping html data for match_id: {}".format(self.match_id))
                html_data = BeautifulSoup(r.text, 'html.parser')
                self._write(file, html_data.prettify())
                return html_data
