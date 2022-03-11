#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""
module docstring - short summary
"""

__version__ = "1.0.0"
__author__ = "K4th4r1n4"

# -----------------------------------------------------------------------------

# import stuff
from time import sleep
from random import choice
import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import Union


DELAYS = [1, 3, 5, 8]


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
    """
    ToDo
    Example: season='2013-2014'
    """
    url = 'https://www.sport.de/fussball/schweiz-super-league/' + \
          f'se36440/{season}/ergebnisse-und-tabelle/'
    results = pd.DataFrame()

    # avoid getting blocked by adding random time delay
    sleep(choice(DELAYS))
    r = requests.get(url)
    if r.status_code != 200:
        # ToDo: something went wrong in this case
        pass

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
    """ToDo"""
    data = pd.DataFrame()
    for season in seasons:
        data = data.append(scrape_season(season))
    return data


def save_data(data: pd.DataFrame) -> None:
    """ToDo"""
    data.to_csv('data/raw/raw_data.csv')


def main(args=None):
    # ToDo: get seasons from command line
    seasons = ['2013-2014', '2014-2015', '2015-2016', '2016-2017',
               '2017-2018', '2018-2019', '2019-2020', '2020-2021']
    raw_data = get_data(seasons)

    # save
    save_data(raw_data)



if "__main__" == __name__:
    main()
