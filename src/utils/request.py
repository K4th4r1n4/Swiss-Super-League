# -*- coding: utf-8 -*-
"""Requesting functionalities."""

from typing import List

import requests
from bs4 import BeautifulSoup


def get_free_proxies() -> List[str]:
    """Get list of free proxies from 'https://free-proxy-list.net/'.

    Returns:
        List[str]: List containing the proxies.

    Examples:
        >>> get_free_proxies()
        ['74.208.150.121:5050',
         '93.188.161.84:80',
         '23.108.43.67:8118',
         '94.154.127.224:8085',
         '192.177.165.213:3128',
         '23.108.42.100:8118',
         '142.252.223.35:3128',
          ...
         '185.82.98.73:9093']
    """
    url = "https://free-proxy-list.net/"
    # get the HTTPS response and construct soup object
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    proxies = "\n".join(soup.find("textarea")).split("\n")[3:-1]
    return proxies
