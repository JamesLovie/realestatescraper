# Real Estate Scraper: James Lovie 2018
#!/usr/bin/env python3

# Pandas library for dataframe and passing out data to database/csv.
import pandas as pd
# Beautiful soup parses HTML.
from bs4 import BeautifulSoup
# Requests library
import requests
# Time-Date library
from datetime import date
import time

# Set variables.
addresses = []
urls = []
prices = []
bedrooms = []
buildtypes = []
bathrooms = []
priceDF= []
addressDF= []
bedroomsDF = []
bathroomsDF = []
buildtypesDF = []
date = str(date.today())

try:

	# Loop through first 50 pages each day and add results to dataframe at completion.
	for count in range(1, 51):

		countstr = str(count)
		page_link = 'https://www.realestate.com.au/buy/in-collingwood,+vic+3066%3b+st+kilda,+vic+3182%3b+st+kilda+east,+vic+3183%3b+st+kilda+west,+vic+3182%3b+fitzroy,+vic+3065%3b+fitzroy+north,+vic+3068%3b+clifton+hill,+vic+3068%3b+northcote,+vic+3070%3b+carlton+north,+vic+3054%3b+prahran,+vic+3181%3b+richmond,+vic+3121%3b+south+yarra,+vic+3141%3b+windsor,+vic+3181%3b+malvern,+vic+3144/list-' + countstr + '?includeSurrounding=true&activeSort=list-date&source=refinement'

		page_response = requests.get(page_link, timeout=5)

		page_content = BeautifulSoup(page_response.content, "html.parser")

		html = page_content.prettify("utf-8")

		# Set the soup variable to html in bs4.
		soup = BeautifulSoup(html, "html.parser")

		# Parse the bedrooms for each property on the nth page.

		for span in soup.find_all('span', attrs={"class":"general-features__icon general-features__beds"}):
			bedrooms.append(span)

		# Parse the buildtype for each property on the nth page.

		for span in soup.find_all('span', attrs={"class":"residential-card__property-type"}):
			buildtypes.append(span)

		# Parse the bathrooms for each property on the nth page.

		for span in soup.find_all('span', attrs={"class":"general-features__icon general-features__baths"}):
			bathrooms.append(span)

		# Parse the prices for each property on the nth page.

		for span in soup.find_all('span', attrs={"class":"property-price "}):
			prices.append(span)

		# Parse the urls for each property on nth page.

		for a in soup.find_all('a', attrs={"class":"details-link residential-card__details-link"}, href=True):
		    urls.append(a['href'])

		# Parse the address for each property on nth page.

		for a in soup.find_all('a', attrs={"class":"details-link residential-card__details-link"}):
			addresses.append(a)

		print('Page: ' + countstr + ' Scraped')

		# Sleep to avoid hitting the website too quickly.
		time.sleep(5)
	# Clean tags from prices data.

	for price in prices:
		priceDF.append(price.text)

	# Clean tags from address data.

	for address in addresses:
		addressDF.append(address.text)

	# Clean tags from buildtype data.

	for buildtype in buildtypes:
		buildtypesDF.append(buildtype.text)

	# Clean tags from bedrooms data.

	for bedroom in bedrooms:
		bedroomsDF.append(bedroom.text)

	# Clean tags from bathrooms data.

	for bathroom in bathrooms:
		bathroomsDF.append(bathroom.text)

	# Write to dataframe, then to CSV file.

	df = pd.DataFrame(list(zip(*[addressDF, priceDF, buildtypesDF, bedroomsDF, bathroomsDF, urls])))
	df.columns = ['Addresses', 'Prices', 'Building_Type', 'Bedrooms', 'Bathrooms', 'URLs']

	# This routine removes all starting and ending whitepace from dataframe.
	cols = df.select_dtypes(['object']).columns
	df[cols] = df[cols].apply(lambda x: x.str.strip())

	# Remove all non-numeric characters from prices column.
	df['Prices'] = df.Prices.str.replace(r"[a-zA-Z:!@]",'')

# Write dataframe to csv file for archive, with datestamp and iteration count.

	# df.to_csv('real_estate_data ' + date + '.csv')
	sep=','
	df.to_csv('real_estate_data.csv', mode='a', index=False, sep=sep, header=False)
	# print('File Saved: ' + 'real_estate_data ' + date + '.csv')
	print('File updated sucessfully')
	
	print('All done :)')

except Exception as e: print('Error: Failed to execute'), print(e)
