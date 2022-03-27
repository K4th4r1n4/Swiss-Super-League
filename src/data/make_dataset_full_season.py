#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""
Module to create dataset of a full Swiss Super League season.
"""

__version__ = "1.0.0"
__author__ = "K4th4r1n4"

# -----------------------------------------------------------------------------

# import stuff
import argparse
from typing import List
from time import sleep
from random import choice
import requests
from bs4 import BeautifulSoup
import pandas as pd


DELAYS = [1.5, 4, 5, 6.5]
MATCH_DAYS = 36

SEASONS = [
    '2003-2004', '2004-2005', '2005-2006', '2006-2007', '2007-2008',
    '2008-2009', '2009-2010', '2010-2011', '2011-2012', '2012-2013',
    '2013-2014', '2014-2015', '2015-2016', '2016-2017', '2017-2018',
    '2018-2019', '2019-2020', '2020-2021',
]


class Match:
    """A class representing one match in the Swiss Super League.

    Attributes:
        match_day (Union[None, int]): The match day. Defaults to None.
        team1 (Union[None, str]): The home team. Defaults to None.
        team2 (Union[None, str]): The away team. Defaults to None.
        scheme (Union[None, str]): The game scheme. Defaults to None.
        result (Union[None, str]): The result. Defaults to None.
    """
    def __init__(self):
        self.match_day = None
        self.team1 = None
        self.team2 = None
        self.scheme = None
        self.result = None

    def __iter__(self):
        yield 'match_day', self.match_day
        yield 'team1', self.team1
        yield 'team2', self.team2
        yield 'scheme', self.scheme
        yield 'result', self.result


def scrape_full_season(season: str) -> pd.DataFrame:
    """Scrape full season data of Swiss Super League.

    Args:
        season (str): The season to scrape.

    Returns:
        pd.DataFrame: A dataframe containing the scraped data of full `season`.

    Examples:
        >>> scrape_full_season('2020-2021')
           season  ...  result
    0   2020-2021  ...     2:1
    0   2020-2021  ...     2:1
    0   2020-2021  ...     2:2
    0   2020-2021  ...     2:1
    0   2020-2021  ...     1:0
    ..        ...  ...     ...
    0   2020-2021  ...     2:4
    0   2020-2021  ...     1:2
    0   2020-2021  ...     1:2
    0   2020-2021  ...     4:0
    0   2020-2021  ...     4:1
    [180 rows x 6 columns]
    """
    results = pd.DataFrame()
    for i in range(1, MATCH_DAYS+1):
        url = 'https://www.weltfussball.com/spielplan/' + \
              f'sui-super-league-{season}-spieltag/{i}/'

        # avoid getting blocked by adding random time delay
        sleep(choice(DELAYS))
        r = requests.get(url)
        r.raise_for_status()

        # get table of match day results
        soup = BeautifulSoup(
            str(BeautifulSoup(r.content, "html.parser")).split(
                '<!-- DYNAMIC BOX -->')[0].split(
                '<!-- /DYNAMIC BOX -->')[0], "html.parser")

        # loop over all matches of match day 'i'
        boxes = soup.find_all('table')[1].find_all('tr')
        for box in boxes:
            match = Match()
            match.match_day = i
            match.team1 = box.find_all('a')[0].get('title')
            match.team2 = box.find_all('a')[1].get('title')
            match.scheme = box.find_all('a')[2].get('title')
            match.result = box.find_all('a')[-1].get_text().split(' ')[0]

            # append results with results for team
            results = results.append(pd.DataFrame.from_records(
                [{**{'season': season}, **match.__dict__}]
            ))
    return results


def get_full_season_data(seasons: List[str]) -> pd.DataFrame:
    """Get full season result of Swiss Super League for `seasons`.

    Args:
        seasons (List[str]): The season(s) to scrape.

    Returns:
        pd.DataFrame: A dataframe containing the scraped data of `seasons`.

    Examples:
        >>> get_full_season_data(['2019-2020', '2020-2021'])
           season  match_day  ...                                          scheme result
    0   2019-2020          1  ...                  Spielschema FC Sion - FC Basel    1:4
    0   2019-2020          1  ...       Spielschema FC Thun - Neuchâtel Xamax FCS    2:2
    0   2019-2020          1  ...           Spielschema FC St. Gallen - FC Luzern    0:2
    0   2019-2020          1  ...    Spielschema BSC Young Boys - Servette Genève    1:1
    0   2019-2020          1  ...               Spielschema FC Zürich - FC Lugano    0:4
    ..        ...        ...  ...                                             ...    ...
    0   2020-2021         36  ...  Spielschema FC Lausanne-Sport - BSC Young Boys    2:4
    0   2020-2021         36  ...               Spielschema FC Luzern - FC Lugano    1:2
    0   2020-2021         36  ...     Spielschema Servette Genève - FC St. Gallen    1:2
    0   2020-2021         36  ...                  Spielschema FC Sion - FC Basel    4:0
    0   2020-2021         36  ...                Spielschema FC Zürich - FC Vaduz    4:1
    [360 rows x 6 columns]
    """
    data = pd.DataFrame()
    for season in seasons:
        data = data.append(scrape_full_season(season))
    return data


def save_full_season_data(data: pd.DataFrame) -> None:
    """Save result of Swiss Super League for full season(s).

    Args:
        data (pd.DataFrame): The dataframe to save.

    Examples:
        >>> ssl_data_full_season = scrape_full_season('2020-2021')
        >>> save_full_season_data(ssl_data_full_season)
    """
    data.to_csv('../../data/raw/raw_data_full_season.csv',
                sep=',', index=False)


def main(args=None):
    """The main function."""
    # ToDo: get seasons from command line
    seasons = args.seasons
    if seasons == 'all':
        seasons = SEASONS

    # scrape seasons
    raw_data = get_full_season_data(seasons)

    # save data
    save_full_season_data(raw_data)


if "__main__" == __name__:
    parser = argparse.ArgumentParser(description='ToDo')
    parser.add_argument('-s', '--seasons', default='all',
                        help='Seasons to scrape')
    args = parser.parse_args()
    main(args)
