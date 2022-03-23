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
from time import sleep
from random import choice
import requests
from bs4 import BeautifulSoup
import pandas as pd


DELAYS = [1.5, 4, 5, 6.5]
MATCH_DAYS = 36


class Match:
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
      season  match_day      team1      team2                 scheme   result
0  2020-2021          1  FC Lugano  FC Luzern  FC Lugano - FC Luzern      2:1
...
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
        boxes = soup.find_all('table')[0].find_all('tr')
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
    # ToDo: get seasons from command line
    # test = scrape_full_season('2020-2021')
    # save_full_season_data(test)
    pass


if "__main__" == __name__:
    parser = argparse.ArgumentParser(description='ToDo')
    parser.add_argument('-s', '--seasons', default='all',
                        help='Seasons to scrape')
    args = parser.parse_args()
    main(args)
