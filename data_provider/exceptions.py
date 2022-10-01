#!/usr/bin/env python

# TODO - Fix this
"""
This module contains various exceptions raised by python-data_provider.
"""


class MatchNotFoundError(TypeError):
    """
    Exception raised if a match_id is not valid or does not exist.
    """
    pass

class PlayerNotFoundError(TypeError):
    pass

class NoScorecardError(TypeError):
    """
    Exception raised if a match has no scorecard
    """
    pass

class NoSeriesError(TypeError):
    """
    Exception raised if a series_id is not valid or does not exist.
    """
    pass
