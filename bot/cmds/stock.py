"""Stock command process module"""

import csv
import requests
from . import server


@server.consumer()
def stock(params):
    """Process stock command"""
    if len(params) == 0:
        return "I need the stock code to work with :)"
    if len(params) > 2:
        return "Seems like you gave me a few params more than what I can handle"

    stock_code = str(params[0]).lower()

    try:
        download = requests.get(
            f"https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcv&h&e=csv"
        )
        decoded_content = download.content.decode("utf-8")
        reader = csv.reader(decoded_content.splitlines(), delimiter=",")
        next(reader, None)  # skip the headers
        for row in reader:
            return f"{row[0]} quote is ${row[3]} per share."
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)

    return "Something went wrong :/ Check stock code, but if problem continues it is most likely to be my fault"
