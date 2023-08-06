'''
A CLI tool to check ETF ratings
'''

import logging

import click
import requests

from bs4 import BeautifulSoup

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)


@click.group()
def cli():
    """
    CLI entrypoint
    """


@cli.command("get-ratings")
@click.argument('symbol', nargs=1)
def get_ratings(symbol):
    """
    Gets the ratings from Zacks and Morningstar for a given ETF symbol
    """
    if symbol is None:
        print("No symbol supplied!")
        return

    zacks_rating = check_zacks_rating(symbol)
    if zacks_rating is None:
        print("Can't reach Zacks at the moment.")
    else:
        print("Zacks rates {0} at {1}".format(symbol, zacks_rating))

    ms_rating = check_ms_rating(symbol)
    if ms_rating is None:
        print("Can't reach Morningstar at the moment.")
    elif ms_rating == -1:
        print("{0} doesn't seem to have a rating.".format(symbol))
    else:
        print("Morningstar rates {0} at a {1} out of 5".format(
            symbol, ms_rating))


@cli.command("get-sustainability")
@click.argument('symbol', nargs=1)
def get_sustainability(symbol):
    """
    Gets Morningstar's sustainability rating for a symbol
    """
    if symbol is None:
        print("No symbol supplied!")
        return

    sus_rating = check_ms_sustainability(symbol)
    if sus_rating is None:
        print("Can't find the sustainability rating for {0}".format(symbol))
        return
    print("Morningstar reports {0} sustainability for {1}.".format(
        sus_rating, symbol))


@cli.command("get-etf-rankings")
@click.argument('symbol', nargs=1)
def get_etf_rankings(symbol):
    """
    Gets the rankings from Morningstar and Zacks for a given ETF
    """
    # etfdb decided to refactor a ton of their shit and now they don't use
    # semi-sensible ways to scrape categories so we can only get the rank of a
    # single symbol until a better method of getting etfs by category is found
    # etf_symbol_list = get_all_etfs(cat_dict[category], limit)

    # We determine the overall ranking by checking the ratings for Zacks,
    # Morningstar, and the sustainability reported by Morningstar
    # We could weight each thing by some arbitrary amount but everything
    # will be weighted the same for now
    zacks_rating = check_zacks_rating(symbol)
    ms_rating = check_ms_rating(symbol)
    ms_sus = check_ms_sustainability(symbol)

    # Set it to 0 if it's not defined, convert to number otherwise
    if not zacks_rating:
        zacks_rating = 0
    else:
        zacks_rating = ZACKS_RANK_DICT[zacks_rating]

    if ms_rating is None:
        ms_rating = 0
    else:
        ms_rating = int(ms_rating)

    if ms_sus is None:
        ms_sus = 0
    else:
        ms_sus = SUS_RANK_DICT[ms_sus]

    print("""
    {0} Ratings:
    Zack's Rating:              {1}
    Morningstar Rating:         {2}
    Morningstar Sustainability: {3}""".format(symbol, zacks_rating, ms_rating, ms_sus))


# We want good ranks to be high numbers (5 max) so we need to convert some
# rankings
SUS_RANK_DICT = {
        "HIGH": 5,
        "ABOVE AVERAGE": 4,
        "AVERAGE": 3,
        "BELOW AVERAGE": 2,
        "LOW": 1,
        "NO RATING": 0
}

ZACKS_RANK_DICT = {
        "1 - Strong Buy": 5,
        "2 - Buy": 4,
        "3 - Hold": 3,
        "4 - Sell": 2,
        "5 - Strong Sell": 1
}


def check_zacks_rating(symbol):
    """
    Checks Zacks rating for a given ETF symbol
    """
    page = requests.get("https://www.zacks.com/funds/etf/" + symbol +
                        "/profile")

    if page.status_code != 200:
        LOGGER.debug("Zacks is returning status code %s", page.status_code)
        return None

    soup = BeautifulSoup(page.text, 'html.parser')
    rating_text = soup.find(class_='zr_rankbox').getText()
    # The below line is kinda gross but it turns the rating text (something
    # like '\nZacks ETF Rank  1 - Strong Buy 1 \xa0 \xa0 \xa0 \xa0\n')
    # into '1 - Strong Buy'. Since the ratings are things like Hold, Buy,
    # Strong Sell, etc, we can't just get the second-to last item if we split
    # the string on spaces.
    return rating_text.replace(u'\xa0', u'').strip().split("Zacks ETF Rank  ")[1][:-2].strip()


def check_ms_rating(symbol):
    """
    Checks Morningstar rating for a given ETF symbol
    """
    page = requests.get("http://www.morningstar.com/api/v1/security-identifier/" + symbol)

    if page.status_code != 200:
        LOGGER.debug("Morningstar is returning status code %s", page.status_code)
        return None

    return page.json()['starRating']


def check_ms_sustainability(symbol):
    """
    Checks Morningstar sustainability for a given ETF symbol
    """
    page = requests.get(
        "http://etfs.morningstar.com/etfq/esg-etf?&t=ARCX:" +
        symbol + (
            "&region=usa&"
            "culture=en-US&"
            "version=RET&"
            "cur=&"
            "test=QuoteiFrame&"
            "e=eyJlbmMiOiJBMTI4R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.tSDHKSXdLz9Z-"
            "95RIt28jRBS2bycBEfA83K4AAWtpDsmwZ3eZJuOatSWRjLITgGJVDutGigpcxJ"
            "x7ojDFi4SiUq93kz5skXbVz9We3sUV5xXKSDW7W5HTtV0Oh4eSYl4bjf_csXP5"
            "pexU-eAYvofcSrHtmEn_GOcQ4GJA_qzXJc.70cJ7G9sm6MH4gYA.eZUC9ESEz_"
            "SGFNEd4tF5O3eXrS6mKs8-AWDZH4r55aD1Bm0K2R-Na5bOxUmXr2XbGTrkfbi-"
            "-UTrPjvwRxAWYbMIGxs12mKL1etKxdmVImSVhN2bk4WDOfV9Vnotfu0-YigkPJ"
            "HAAPnnB5owMwmWOmSsm-Xxxo-kFLK5C1K3YYBYe2ruwZVxO1rJ6se-ruzjipYA"
            "mRR9vIjxaUvadr0bAOxnS8KbgFIdv5fBILs.nEgzKr6eTtw896WO8yE1mA&_=1"
            "518983228036"))

    if page.status_code != 200:
        LOGGER.debug("Morningstar is returning status code %s", page.status_code)
        return None

    soup = BeautifulSoup(page.text, 'html.parser')
    # The rating doesn't have a unique ID or class so we have to hope the HTML
    # doesn't change...
    rating_html = soup.find_all(class_='text-margin5 text-size14')

    if not rating_html:
        return None

    return rating_html[0].get_text().strip().upper()
