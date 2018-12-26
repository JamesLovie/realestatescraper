# realestatescraper
A simple realestate.com.au web scraper build in python (requests, beautifulsoup, pandas).

A simple tool to extract price address and URL links for each property on a specific URL query.

You can adjust the query to add/subtract specific suburbs, price range, surrounding suburbs flag and any other search parameter on the realestate.com.au website.

Uses pandas to create a dataframe and export to a csv file.

Addtional work to be completed: To append dataframe with existing data to create one whole database that only adds new entries and removes duplicate listing data. Parses suburb into another col in the dataframe and to geotag address from Google Maps API to have coordinates data with each row for historical prices.
