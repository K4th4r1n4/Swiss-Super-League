#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""
module docstring - short summary
"""

__version__ = "1.0.0"
__author__ = "K4th4r1n4"

# -----------------------------------------------------------------------------

# import stuff
import argparse
from time import sleep
from random import choice
import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import Union


DELAYS = [1, 3, 5, 8]

SEASON_MAP = {
    '2003-2004': 'se3159', '2004-2005': 'se3799', '2005-2006': 'se4053',
    '2006-2007': 'se4423', '2007-2008': 'se5120', '2008-2009': 'se112',
    '2009-2010': 'se1477', '2010-2011': 'se5847', '2011-2012': 'se7182',
    '2012-2013': 'se9080', '2013-2014': 'se12441', '2014-2015': 'se15417',
    '2015-2016': 'se18372', '2016-2017': 'se20904', '2017-2018': 'se23964',
    '2018-2019': 'se28592', '2019-2020': 'se31824', '2020-2021': 'se36440',
}


class TeamScore:
    def __init__(self):
        self.team_name = None
        self.games_played = None
        self.win = None
        self.draw = None
        self.lost = None
        self.goal_diff = None
        self.difference = None
        self.points = None

    def __iter__(self):
        yield 'team_name', self.team_name
        yield 'games_played', self.games_played
        yield 'win', self.win
        yield 'draw', self.draw
        yield 'lost', self.lost
        yield 'goal_diff', self.goal_diff
        yield 'difference', self.difference
        yield 'points', self.points


def scrape_season(season: str) -> pd.DataFrame:
    """Scrape final result of Swiss Super League for season.

    :param season: season to scrape

    :return: pandas.DataFrame containing season data
    """
    url = 'https://www.sport.de/fussball/schweiz-super-league/' + \
          f'{SEASON_MAP[season]}/{season}/ergebnisse-und-tabelle/'
    results = pd.DataFrame()

    # avoid getting blocked by adding random time delay
    sleep(choice(DELAYS))
    r = requests.get(url)
    r.raise_for_status()

    # get table of end of season
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find_all('table')[0].find_all('tr')

    # loop over teams
    for team in table:
        team_score = TeamScore()
        team_score.team_name = team.find(
            class_="team-image team-image-").find('img').get('title')
        team_score.games_played = int(
            team.find(class_="standing-games_played").text)
        team_score.win = int(team.find(class_="standing-win").text)
        team_score.draw = int(team.find(class_="standing-draw").text)
        team_score.lost = int(team.find(class_="standing-lost").text)
        team_score.goal_diff = team.find(class_="standing-goaldiff").text
        team_score.difference = team.find(class_="standing-difference").text
        team_score.points = int(team.find(class_="standing-points").text)

        # append results with results for team
        results = results.append(pd.DataFrame.from_records(
            [{**{'season': season}, **team_score.__dict__}]
        ))
    return results


def get_data(seasons: Union[list, str]) -> pd.DataFrame:
    """Get final result of Swiss Super League for seasons.

    :param seasons: season(s) to scrape

    :return: pandas.DataFrame containing data of seasons
    """
    data = pd.DataFrame()
    for season in seasons:
        data = data.append(scrape_season(season))
    return data


def save_data(data: pd.DataFrame) -> None:
    """Save final result of Swiss Super League for seasons.

    :param data: data to save
    """
    data.to_csv('../../data/raw/raw_data.csv', sep=',', index=False)


def main(args=None):
    # ToDo: get seasons from command line
    seasons = args.seasons
    if seasons == 'all':
        seasons = SEASON_MAP.keys()

    # scrape seasons
    raw_data = get_data(seasons)

    # save data
    save_data(raw_data)


if "__main__" == __name__:
    parser = argparse.ArgumentParser(description='ToDo')
    parser.add_argument('-s', '--seasons', default='all',
                        help='Seasons to scrape')
    args = parser.parse_args()
    main(args)
