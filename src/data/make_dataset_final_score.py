#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""
Module to create dataset of Swiss Super League final scores.
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
from typing import List, Union


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
    """A class representing the final score of a team in the Swiss Super League
    at the end of one season.

    Attributes:
        team_name (Union[None, str]): The team name. Defaults to None.
        rank (Union[None, int]): The final ranking. Defaults to None.
        games_played (Union[None, int]): The number of games played. Defaults
            to None.
        win (Union[None, int]): The number of games won. Defaults to None.
        draw (Union[None, int]): The number of draws. Defaults to None.
        lost (Union[None, int]): The number of games lost. Defaults to None.
        goal_diff (Union[None, str]): The number of goals scored and goals
            conceded. The Defaults to None.
        difference (Union[None, int]): The goal difference, meaning the number
            of goals scored across the season, minus the number of goals
            conceded. Defaults to None.
        points (Union[None, int]): The final number of points. Defaults to
            None.
    """
    def __init__(self):
        self.team_name = None
        self.rank = None
        self.games_played = None
        self.win = None
        self.draw = None
        self.lost = None
        self.goal_diff = None
        self.difference = None
        self.points = None

    def __iter__(self):
        yield 'team_name', self.team_name
        yield 'rank', self.rank
        yield 'games_played', self.games_played
        yield 'win', self.win
        yield 'draw', self.draw
        yield 'lost', self.lost
        yield 'goal_diff', self.goal_diff
        yield 'difference', self.difference
        yield 'points', self.points


def scrape_season_final_score(season: str) -> pd.DataFrame:
    """Scrape final result of Swiss Super League for season.

    Args:
        season (str): The season to scrape.

    Returns:
        pd.DataFrame: A dataframe containing the scraped data of `season`.

    Examples:
        >>> scrape_season_final_score('2020-2021')
          season          team_name  rank  ...  goal_diff  difference  points
    0  2020-2021     BSC Young Boys     1  ...      74:29          45      84
    0  2020-2021           FC Basel     2  ...      60:53           7      53
    0  2020-2021    Servette Genève     3  ...      45:56         -11      50
    0  2020-2021          FC Lugano     4  ...      40:42          -2      49
    0  2020-2021          FC Luzern     5  ...      62:59           3      46
    0  2020-2021  FC Lausanne-Sport     6  ...      52:55          -3      46
    0  2020-2021      FC St. Gallen     7  ...      45:48          -3      44
    0  2020-2021          FC Zürich     8  ...      53:57          -4      43
    0  2020-2021            FC Sion     9  ...      48:58         -10      38
    0  2020-2021           FC Vaduz    10  ...      36:58         -22      36
    [10 rows x 10 columns]
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
    for i, team in enumerate(table):
        team_score = TeamScore()
        team_score.team_name = team.find(
            class_="team-image team-image-").find('img').get('title')
        team_score.rank = i + 1
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


def get_final_score_data(seasons: List[str]) -> pd.DataFrame:
    """Get final result of Swiss Super League for `seasons`.

    Args:
        seasons (List[str]): The season(s) to scrape.

    Returns:
        pd.DataFrame: A dataframe containing the scraped data of `seasons`.

    Examples:
        >>> get_final_score_data(['2019-2020', '2020-2021'])
          season            team_name  rank  ...  goal_diff  difference  points
    0  2019-2020       BSC Young Boys     1  ...      80:41          39      76
    0  2019-2020        FC St. Gallen     2  ...      79:56          23      68
    0  2019-2020             FC Basel     3  ...      74:38          36      62
    0  2019-2020      Servette Genève     4  ...      57:48           9      49
    0  2019-2020            FC Lugano     5  ...      46:46           0      47
    0  2019-2020            FC Luzern     6  ...      42:50          -8      46
    0  2019-2020            FC Zürich     7  ...      45:72         -27      43
    0  2019-2020              FC Sion     8  ...      40:55         -15      39
    0  2019-2020              FC Thun     9  ...      45:67         -22      38
    0  2019-2020  Neuchâtel Xamax FCS    10  ...      33:68         -35      27
    0  2020-2021       BSC Young Boys     1  ...      74:29          45      84
    0  2020-2021             FC Basel     2  ...      60:53           7      53
    0  2020-2021      Servette Genève     3  ...      45:56         -11      50
    0  2020-2021            FC Lugano     4  ...      40:42          -2      49
    0  2020-2021            FC Luzern     5  ...      62:59           3      46
    0  2020-2021    FC Lausanne-Sport     6  ...      52:55          -3      46
    0  2020-2021        FC St. Gallen     7  ...      45:48          -3      44
    0  2020-2021            FC Zürich     8  ...      53:57          -4      43
    0  2020-2021              FC Sion     9  ...      48:58         -10      38
    0  2020-2021             FC Vaduz    10  ...      36:58         -22      36
    [20 rows x 10 columns]
    """
    data = pd.DataFrame()
    for season in seasons:
        data = data.append(scrape_season_final_score(season))
    return data


def save_final_score_data(data: pd.DataFrame) -> None:
    """Save final result of Swiss Super League for seasons.

    Args:
        data (pd.DataFrame): The dataframe to save.

    Examples:
        >>> ssl_data_final = get_final_score_data(['2019-2020', '2020-2021'])
        >>> save_final_score_data(ssl_data_final)
    """
    data.to_csv('../../data/raw/raw_data_final_score.csv',
                sep=',', index=False)


def main(args=None):
    """The main function."""
    # ToDo: get seasons from command line
    seasons = args.seasons
    if seasons == 'all':
        seasons = SEASON_MAP.keys()

    # scrape seasons
    raw_data = get_final_score_data(seasons)

    # save data
    save_final_score_data(raw_data)


if "__main__" == __name__:
    parser = argparse.ArgumentParser(description='ToDo')
    parser.add_argument('-s', '--seasons', default='all',
                        help='Seasons to scrape')
    args = parser.parse_args()
    main(args)
