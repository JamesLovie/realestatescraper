#!/usr/bin/env python3

# For dealing with json.
import json
# Pandas library for dataframe and passing out data to database.
import pandas as pd
# Beautiful soup parses HTML.
from bs4 import BeautifulSoup
# Requests library
import requests
# Regex library
import re
# Date-Time library
from datetime import date

# Set variables.
addresses = []
urls = []
prices = []
priceDF = []
addressDF = []
date = str(date.today())

try:

	# Loop through first 20 pages each day and add results to dataframe at completion.
	for count in range(1, 21):

		countstr = str(count)
		page_link = 'https://www.realestate.com.au/buy/between-150000-600000-in-collingwood,+vic+3066%3b+st+kilda,+vic+3182%3b+st+kilda+east,+vic+3183%3b+st+kilda+west,+vic+3182%3b+fitzroy,+vic+3065%3b+fitzroy+north,+vic+3068%3b+clifton+hill,+vic+3068%3b+northcote,+vic+3070%3b+carlton+north,+vic+3054%3b+prahran,+vic+3181%3b+richmond,+vic+3121%3b+south+yarra,+vic+3141%3b+windsor,+vic+3181%3b+malvern,+vic+3144/list-' + countstr + '?includeSurrounding=false&activeSort=list-date&source=refinement'

		page_response = requests.get(page_link, timeout=5)

		page_content = BeautifulSoup(page_response.content, "html.parser")

		html = page_content.prettify("utf-8")

		# Set the soup variable to html in bs4.
		soup = BeautifulSoup(html, "html.parser")

		# Parse the prices for each property on the nth page.

		for span in soup.find_all('span', attrs={"class":"property-price "}):
			prices.append(span)

		# Parse the urls for each property on nth page.

		for a in soup.find_all('a', attrs={"class":"details-link residential-card__details-link"}, href=True):
			urls.append(a['href'])

		# Parse the address for each property on nth page.

		for a in soup.find_all('a', attrs={"class":"details-link residential-card__details-link"}):
			addresses.append(a)

		print(countstr)

	# Clean tags from prices data.

	for price in prices:
		priceDF.append(price.text)

	# Clean tags from address data.

	for address in addresses:
		addressDF.append(address.text)

	# Write to dataframe, then to CSV file.

	df = pd.DataFrame(list(zip(*[addressDF, priceDF, urls])))
	df.columns = ['Addresses', 'Prices', 'URLs']

	# This routine removes all starting and ending whitepace from dataframe.
	cols = df.select_dtypes(['object']).columns
	df[cols] = df[cols].apply(lambda x: x.str.strip())

	# Remove all non-numeric characters from prices column.
	df['Prices'] = df.Prices.str.replace(r"[a-zA-Z:!@]",'')

# Write dataframe to csv file for archive, with datestamp and iteration count.

	df.to_csv('real_estate_data ' + date + '.csv')

# file.close()
	
	print('All done :)')

except:
	
	print('Error: Failed to execute, likely unable to connect to the internet or webpage url has changed.')

# Old Code:

		# textContent = []
		# for i in range(0, 20):
		#     paragraphs = page_content.find_all("div")[i].text
		#     textContent.append(paragraphs)

		# with open('data_real.txt', 'w') as file:
		# 	file.write(json.dumps(page_content))

		# ///////////////////////

				# with open("real_data.txt", "wb") as file:
		#     file.write(html)

		# ///////////////////////

		# json = json.dumps(textContent)
		# print(json[5].find("$"))

		# data = ""
		# with open("real_data.txt", encoding='utf8') as file:
		# 	html = file.read().rstrip("\n")
