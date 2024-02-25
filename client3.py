import json
import random
import urllib.request

# Server API URLs
QUERY = "http://localhost:8080/query?id={}"

# 500 server requests
N = 500


def getDataPoint(quote):
    """ Produce all the needed values to generate a datapoint """
    stock = quote['stock']
    bid_price = float(quote['top_bid']['price'])
    ask_price = float(quote['top_ask']['price'])
    price = (bid_price + ask_price) / 2  # Calculate price using the average of bid and ask prices
    return stock, bid_price, ask_price, price


def getRatio(price_a, price_b):
    """ Get ratio of price_a and price_b """
    if price_b == 0:
        return None  # Avoid division by zero
    return price_a / price_b


# Main
if __name__ == "__main__":
    prices = {}  # Dictionary to store stock prices
    # Query the price once every N seconds.
    for _ in iter(range(N)):
        quotes = json.loads(urllib.request.urlopen(QUERY.format(random.random())).read())

        for quote in quotes:
            stock, bid_price, ask_price, price = getDataPoint(quote)
            print("Quoted %s at (bid:%s, ask:%s, price:%s)" % (stock, bid_price, ask_price, price))
            prices[stock] = price  # Store the price in the prices dictionary

    # Calculate and print the ratio
    if 'ABC' in prices and 'DEF' in prices:
        ratio = getRatio(prices["ABC"], prices["DEF"])
        if ratio is not None:
            print("Ratio ABC/DEF: %.2f" % ratio)
        else:
            print("Unable to calculate ratio: Division by zero.")
    else:
        print("Data not available for both ABC and DEF.")
