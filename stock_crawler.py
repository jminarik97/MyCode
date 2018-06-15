from bs4 import BeautifulSoup
import lxml
from lxml import html
import requests
import csv
import time ## Timing
import os.path


##Timing
start_time = time.time()

# User input : Ticker
ticker = input("Enter Ticker : ")

##### Index fund exception [rut] #####

# Create stock class 
class Stock:
	def __init__(self, ticker):
		self.ticker = ticker

	# Scrape data
	def scrape(self):	
		# Create URL
		base_url = "https://www.marketwatch.com/investing/stock/"
		url = base_url + self.ticker
		# Spacing
		print("\n", self.ticker)

		# Scrape data
		# requests
		req = requests.get(url)
		soup = BeautifulSoup(req.text, "lxml")

		# Grab an element : price
		price_container = (soup.find("div", class_ = "intraday__data"))
		price_shell = price_container.find_all("bg-quote")
		global price
		price = (price_shell[0].text)
		
		# Fix SPX exception
		# if price > 1 element
		if self.ticker == "SPX" or self.ticker == "spx":
			index_price = (price_container.find("span", class_ = "value").text)
			print(index_price)
		else:
			print(price)

	# Create CSV
	def csv(self):
		# Use of.path to verify if stocks.csv exists 
		if os.path.isfile("stocks.csv") == False:
			with open ("stocks.csv", "w") as csv_file:
				csv_writer = csv.writer(csv_file)
				row_data = ["Ticker", "Price"]
				csv_writer = csv.writer(csv_file)
				csv_writer.writerow(row_data)
		else:
			pass		

	# Add row		
	def	add_row(self):
		with open("stocks.csv", "a") as csv_file:
			new_row_data = (self.ticker, price)
			csv_writer = csv.writer(csv_file)
			csv_writer.writerow(new_row_data)
		
def main():
	my_stock = Stock(ticker)
	my_stock.scrape()
	#my_stock.csv()
	my_stock.add_row()
main()

## Timing
print("\n-- %s seconds --" % round((time.time() - start_time),2))
