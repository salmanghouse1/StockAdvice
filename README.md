# Stock Portfolio

## Purpose
A application that gives you stock info

## Built With
Python


## Contribution
Made with ❤️ by [Salman Ghouse](http://www.salmanwebdeveloper.com)

### ©️2020 Stock Advice 

# Stock Portfolio



- Reading and writing to the file system
- Making HTTP requests
- Testing read & write operations to the disk
- Testing HTTP requests using a mock library
- Packaging the script using `setup.py`


## Description
a program which will generate up-to-date performance reports for a given
stock portfolio. The program will accept two arguments: an input CSV file which
contains the holdings information, and, a path to output the CSV report.

We will use the [IEX Trading API](https://iextrading.com/developer/docs/), as
the market data source – it is a public (free) API.


### Requirements
The program will read a CSV file containing our portfolio data. Based on this
data, a new CSV report will be generated using live market value to indicate
our current holding performance using the IEX API.

The program will be installable using `pip`, and requires a `setup.py`
file. When installed, a binary will be added to the Python path which can be
invoked from anywhere on the filesystem.

An example interaction with the script looks like this:

```
$ portfolio_report --source portfolio.csv --target report1.csv
```

#### Input file
The input CSV will have 3 columns (example provided).

- `symbol`: the ticker symbol (e.g. AAPL is Apple)
- `units`: the quantity of shares held
- `cost`: the original / average purchase price of the holding


Example:

symbol | units | cost
-------| ------|------
AAPL   | 1000  | 123.56
AMZN   |  20   | 2001.1



Using the list of symbols from the input CSV, get quotes from IEX to fetch the
latest price. This can be done in a batch request – meaning, multiple quotes
can be requested in a single HTTP request. See:

Docs: https://iextrading.com/developer/docs/#tops

#### Example request & response
Example request: GET the latest quotes for Apple, Facebook & Snapchat:

https://api.iextrading.com/1.0/tops/last?symbols=AAPL,AMZN,SNAP

```json
[{
    "symbol": "AAPL",
        "price": 204.29,
        "size": 100,
        "time": 1563307196175
}, {
    "symbol": "AMZN",
        "price": 2008.395,
        "size": 1,
        "time": 1563307196058
}, {
    "symbol": "SNAP",
        "price": 15,
        "size": 100,
        "time": 1563307196047
}]
```


Once the latest price is obtained, a series of calculations are made to
establish the current performance of the portfolio: what the current market
value is, the gain and loss for each holding and a percentage of change.

If a symbol listed in the input CSV is not found on the exchange, the IEX API
ignores it. Your script should account for this situation by warning the user
that the symbol was not found, but continue to process the rest of the valid
symbols.


#### Output file

The expected CSV report will have the following columns

* `symbol`: The stock ticker symbol (i.e. AAPL)
* `units`: The amount of shares held
* `cost`: The original cost per share
* `latest_price`: The latest market price per share
* `book_value`: The value of the shares at time of purchase
* `market_value`: The value of the shares based on the latest market value
* `gain_loss`: The dollar amount either gained or lost
* `change`: A percentage (decimal) of the gain/loss


##### Sample output CSV
symbol  | units | cost     |   latest_price | book_value  |   market_value | gain_loss |   change
------- |-------|----------|----------------|-------------|----------------| ----------|----------
AAPL    | 1000  | 123.56   |   156.23       | 12356       |   15623        | 3267      |   0.264
AMZN    | 20    | 2001.1   |   1478.19      | 40022       |   29563        | -10459    |   -0.261



## Testing

Testing against third-party services can be challenging as they are out of our
control. As developers, we must build our application with the expectation of
specific behaviours from these services. Mocks (faking) are a handy way to
isolate the dependency and replace it with a constant to which we can build
tests. For this, we will use the `requests-mock` library to stub out
HTTP requests.

https://requests-mock.readthedocs.io/en/latest/pytest.html

Install using `pip install requests-mock`.

As for writing files, use the `tmp_path` fixture that ships with pytest to
write to temporary locations on the disk.


## Packaging

As described above, provide a `setup.py` configuration to package your
application. Ensure that dependencies required to run your script are included
(e.g. requests)


