import requests
from bs4 import BeautifulSoup
import json


class Download(object):

    def __init__(self, match_id, output_path):
        self.match_id = match_id
        self.match_url = "https://www.espncricinfo.com/matches/engine/match/{0}.html".format(str(self.match_id))
        self.json_url = "https://www.espncricinfo.com/matches/engine/match/{0}.json".format(str(match_id))
        self.html = self._get_html()
        self.json = self._get_json()
        self.output_path = output_path
        self._save_data()

    def _save_data(self):
        self._write("html", self.html.prettify())
        self._write("json", json.dumps(self.json))

    def _write(self, suffix, data):
        path = self.output_path + "." + suffix
        f = open(path, "w")
        f.write(data)
        f.close()

    def _get_json(self):
        r = requests.get(self.json_url)
        if r.status_code == 404:
            raise Exception('Invalid URL')
        elif 'Scorecard not yet available' in r.text:
            raise Exception('Score card not yet available')
        else:
            return r.json()

    def _get_html(self):
        page = requests.get(self.match_url)
        return BeautifulSoup(page.text, 'html.parser')
