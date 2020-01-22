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

# Class names should follow the UpperCaseCamelCase convention.
class WebScraper:

	# Constructor: Instance variable names should be all lower case.
	def __init__(self, target_url):
		self.target_url = target_url

	def scrape_pages(self):
		try:

			# Loop through first 50 pages each day and add results to dataframe at completion.
			for count in range(1, 51):

				countstr = str(count)
				# Insert your desired real estate website here.
				page_link = self.target_url + countstr + '?'

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
			sep=','
			df.to_csv('real_estate_data.csv', mode='a', index=False, sep=sep, header=False)
		except Exception as e: print('Error: Failed to execute'), print(e)

def main():
	# Instantiating the class:
	webscraper = WebScraper('http://www.target-url.com/')
	# Call the function rename.
	scrape_pages = webscraper.scrape_pages()
	print('File updated sucessfully')

if __name__ == '__main__':
    main()
