import json
import os
from data_provider.match import Match
import logging
logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
log = logging.getLogger(__name__)
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


class Main(object):
    # Create match level data for processing for matches under 'input_dir'.
    # The files should contain the match_id as the file name similar to cricsheet format
    @staticmethod
    def prepare_data(input_dir, save_data=True):
        matches_data = []
        i = 1
        data_files = os.path.join(ROOT_DIR, input_dir)
        for dirname, _, filenames in os.walk(data_files):
            for filename in filenames:
                if filename.endswith('.json'):
                    match_id = filename.rsplit(".", 1)[0]
                    match = Match(match_id, input_dir, save_data)
                    matches_data.append(match)
                    log.debug('total files read: {}'.format(i))
                    i = i + 1
        return matches_data


