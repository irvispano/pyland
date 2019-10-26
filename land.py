import os
import requests
from bs4 import BeautifulSoup
from db import get_counties
import math

from pprint import pprint

SCRAPER_API_KEY = os.environ.get('SCRAPER_API_KEY', '')
SCRAPERAPI_URL = 'http://api.scraperapi.com'


def get_num_of_results(first_page_soup):
    resultscount_list = first_page_soup.find(
        'span', {'class': 'resultscount'}).text.split('\xa0')
    # Quest: why does this kind of soup yield characters like
    # '\xa0' when I use soup.text?
    return int(resultscount_list[5])


def gen_paginated_urls(first_page_soup, num_of_results):
    paginated_urls = []
    if num_of_results > 15:
        num_of_pages = math.ceil(num_of_results / 15)
        pagination_base_url = first_page_soup.find(
            'a', {'rel': 'next'})['href'][:-1]
        for i in range(2, num_of_pages + 1):
            paginated_urls.append(f'{pagination_base_url}{i}')
    return paginated_urls


def main():
    counties = get_counties()
    for county in counties[1:3]:
        resp = requests.get(
            SCRAPERAPI_URL,
            {'api_key': SCRAPER_API_KEY, 'url': county['landwatchurl']}
        )
        first_page_soup = BeautifulSoup(resp.content, 'html.parser')

        num_of_results = get_num_of_results(first_page_soup)
        paginated_urls = gen_paginated_urls(
            first_page_soup, num_of_results)
        pprint(paginated_urls)


if __name__ == '__main__':
    main()
