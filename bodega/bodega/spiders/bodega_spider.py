import scrapy
import time
from bodega.items import BodegaItem
import pandas as pd
import csv

# Start by extracting the data from the initial CVS and load them into the ID list
data = pd.read_excel('C:\\Users\\Ousmane Kana\\Desktop\\Bodega\\sbler-Copy.xlsx', header=None)
ID =data[0].tolist()


# Create the receiving CSVs and na,e each of them according to their ID's

for element in ID:
	with open(f'{str(element)}.csv', mode='w', newline='') as csv_file:
		fieldnames = ['SKU', 'Model_number','Name','Wholesale_Price','Price']
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		writer.writeheader()


def Wholesale_Link(item):
	""" This funcion takes as input the ID from the inital CSV and output appropriate wholesale list"""
	
	link = "https://www.thdsalvage.com/Inventory/Detail?wid=8617&sbn="+str(item)+"&wid=8617&sbn="+str(item)
	return (link)


class Wholesale_Spider(scrapy.Spider):
	

	name = "wholesale"

	allowed_domain = ["https://www.thdsalvage.com/"]


	link = map(Wholesale_Link, ID)

	start_urls = list(link)[0:2]

	def parse(self, response):

		"""This methods parses is the first crawler that goes targets the wholesale website to get to following outputs
			Category
			Warehouse location
			Container Quantity
			SB 

			And the following lists:
			SB
			Wholesale price 
			Model numbers 
			SKUs
			"""


		Category = response.xpath("//table[@style=\"text-align:right; width:100%\"]//td[1]//text()").extract()[8]

		Warehouse = response.xpath("//table[@style=\"text-align:right; width:100%\"]//td[1]//text()").extract()[6]

		Container_Qty = response.xpath("//table[@style=\"text-align:right; width:100%\"]//td[1]//text()").extract()[12]

		SB = response.xpath("//table[@style=\"text-align:right; width:100%\"]//td[1]//text()").extract()[2].strip(" ;")

		SKU = response.xpath("//table[@style=\"border:2px #000000 solid; border-collapse:collapse; width: 100%\"]//td[1]//text()").extract()
		Wholesale_Price = response.xpath("//table[@style=\"border:2px #000000 solid; border-collapse:collapse; width: 100%\"]//td[6]//text()").extract()
		Model_number = response.xpath("//table[@style=\"border:2px #000000 solid; border-collapse:collapse; width: 100%\"]//td[4]//text()").extract()

		# Itterate though all the elements of the website
		for i in range (3):
				#Generate the homepedot price according to the SKU
				new_link = 'https://www.homedepot.com/s/'+str(SKU[i])
				# if (urllib.request.urlopen(new_link).getcode()) == 200:
				# Follow the link generated to second craweler. Passes extra argument to parse_homedepot using meta {}
				yield response.follow(new_link, callback=self.parse_homedepot,meta={'SB':SB, 'SKU':SKU[i], 'Model_number': Model_number[i], 'Wholesale_Price':Wholesale_Price[i]})

	def parse_homedepot(self,response):
		
		#Instantiation of the item object for the output feed 
		item = BodegaItem()

		#Parse throught the homedepot page of the item and get the price and name if exists

		try:
			name=response.xpath('//h1[@class="product-title__title"]/text()').extract().pop()
		except IndexError:
			name = 'Not Found'

		try:
			price = str(response.xpath('//span[@class="price__dollars"]/text()').extract().pop()).strip()
		except IndexError:
			price = 'Not Found'

		
		#Load the item object before yielding it for output to pipeline.py
		item['Name'] = name
		item['SKU']  = response.meta['SKU']
		item['SB']  = response.meta['SB']
		item['Price']= price
		item['Model_number'] = response.meta['Model_number']
		item['Wholesale_Price'] = response.meta['Wholesale_Price']

		yield item




		