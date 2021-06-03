import json
import csv
import requests





#Given a filename, read a CSV and convert it to a Python data structure
#Build a method which returns the latest market price for holdings
#Build methods which calculate the book value, market value
#Build a method to convert the holding into CSV
#Build a method that writes to the output filename.
#As for writing files, use the tmp_path fixture that ships with pytest to write to temporary locations on the disk.


#Step 1 Ask for input stock symbol
#step 2 input should be written to csv file
#step 3 http request get the api json_data
#step 4 create variable and use value method and make calculation for current market value,
#the gain and loss for each holding a percentage of change

#Make sure to update requirements.txt and include any libraries required to build this project (e.g. requests, requests-mock) so they are available to Travis CI.


class Holding:
    def __init__(self, csvRow):
        self.symbol = csvRow[0]
        self.units = float(csvRow[1])
        self.cost = float(csvRow[2])
        self.current_price = 0
        self.book_value = self.cost * self.units
        self.market_value = 0
        self.gain_loss = 0
        self.change = 0

    def update_current_price(self, current_price):
        self.current_price = current_price
        self.market_value = self.current_price * self.units
        self.gain_loss = self.market_value - self.book_value
        self.change = self.gain_loss / self.book_value * 100


class Stocks:
    def __init__(self,input_file='portfolio.csv',written_file="output.csv"):
        self.input_file=input_file
        self.written_file=written_file
        self.holdings = []

    def load_data_from_csv(self):
        print("Getting data from csv...")
        if not self.input_file:
            print("... Provide File Name CSV")
        else:
            with open(self.input_file,'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)
                for line in csv_reader:
                    self.holdings.append(Holding(line))
            return "... Data Loaded"
            print("... Data loaded")

    def refresh_live_stock_price(self):
        print("getting live stock data ...")
        stocks_to_search_for = ""
        for holding in self.holdings:
            stocks_to_search_for += holding.symbol + ","
        self.response=requests.get(f"https://api.iextrading.com/1.0/tops/last?symbols={stocks_to_search_for}")
        if self.response:
            print("... Success in connecting")
            return ("... Success in connecting")
        else:
            print("... Error in connecting")
            return ("... Error in connecting")
    def convert_data(self):
        print("converting data ...")
        self.json_data=json.loads(self.response.content)
        if self.json_data:
            return("data converted")
        elif not self.json_data:
            return("Couldnt Convert data")
    def write_data(self):
        if not self.json_data:
            print(" ... Fetch Data First")
            return(" ... Fetch Data First")
        else:
            print("Writing data ...")
            length_of_rows=len(self.json_data)
            with open(self.written_file,'w',newline="") as csvfile:
                col = ["symbol","units","cost","latest_price","book_value","market_value","gain_loss","change"]
                writer = csv.DictWriter(csvfile, fieldnames=col)
                writer.writeheader()
                for i in range(length_of_rows):
                    self.holdings[i].update_current_price(self.json_data[i].get('price'))
                    writer.writerow({col[0]: self.holdings[i].symbol,
                                     col[1]: self.holdings[i].units,
                                     col[2]: self.holdings[i].cost,
                                     col[3]: self.holdings[i].current_price,
                                     col[4]: self.holdings[i].book_value,
                                     col[5]: self.holdings[i].market_value,
                                     col[6]: self.holdings[i].gain_loss,
                                     col[7]: self.holdings[i].change})
                csvfile.close()

    def refresh(self):
        self.load_data_from_csv()
        self.refresh_live_stock_price()
        self.convert_data()
        self.write_data()
        print("Refresh Complete!")
