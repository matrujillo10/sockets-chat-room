"""Stock command process module"""

import csv
import logging
from urllib.parse import quote
import requests
from . import server


# Valid messages
RESULT_MSG = "{} quote is ${} per share."
# Errors messsages
LESS_PARAMS_ERROR_MSG = "I need the stock code to work with :)"
MORE_PARAMS_ERROR_MSG = (
    "Seems like you gave me a few params more than what I can handle"
)
INVALID_STOCK_CODE_ERROR_MSG = "Seems like {} is not a valid stock code :|"
REQUEST_ERROR_MSG = "Something went wrong :/ Could you please try later?"


@server.consumer()
def stock(params):
    """Process stock command"""
    logging.info("Stock Request")
    if len(params) == 0:
        return LESS_PARAMS_ERROR_MSG
    if len(params) > 1:
        return MORE_PARAMS_ERROR_MSG

    stock_code = str(params[0]).upper().strip()
    try:
        download = requests.get(
            f"https://stooq.com/q/l/?s={quote(stock_code)}&f=sd2t2ohlcv&h&e=csv"
        )
        download.raise_for_status()
        decoded_content = download.content.decode("utf-8")
        reader = csv.reader(decoded_content.splitlines(), delimiter=",")
        next(reader, None)  # skip the headers
        for row in reader:
            if len(row) != 8:
                break
            if row[1] != "N/D":
                return RESULT_MSG.format(row[0], row[-2])
            return INVALID_STOCK_CODE_ERROR_MSG.format(stock_code)
        logging.error("Invalid CSV structure")
        logging.error(decoded_content)
    except (
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
        requests.exceptions.RequestException,
        requests.exceptions.Timeout,
        Exception,
    ) as err:
        logging.error(err)

    return REQUEST_ERROR_MSG
