import scrapy
import pandas as pd
import time
import openpyxl
import urllib
from bodega.items import BodegaItem
import csv
import os

data = pd.read_excel('C:\\Users\\Ousmane Kana\\Desktop\\Bodega\\sbler-Copy.xlsx', header=None)

ID =data[0].tolist()

for element in ID:
	with open(f'{str(element)}.csv', mode='a') as csv_file:
		fieldnames = ['Name', 'SKU', 'BS']
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		writer.writeheader()



def Wholesale_Link(item):
   
    link = "https://www.thdsalvage.com/Inventory/Detail?wid=8617&sbn="+str(item)+"&wid=8617&sbn="+str(item)
    return (link)


class Wholesale_Spider(scrapy.Spider):

	

	name = "wholesale"

	allowed_domain = ["https://www.thdsalvage.com/"]


	link = map(Wholesale_Link, ID)

	start_urls = list(link)[0:2]

	def parse(self, response):


		Category = response.xpath("//table[@style=\"text-align:right; width:100%\"]//td[1]//text()").extract()[8]

		Warehouse = response.xpath("//table[@style=\"text-align:right; width:100%\"]//td[1]//text()").extract()[6]

		Container_Qty = response.xpath("//table[@style=\"text-align:right; width:100%\"]//td[1]//text()").extract()[12]

		SB = response.xpath("//table[@style=\"text-align:right; width:100%\"]//td[1]//text()").extract()[2].strip(" ;")

		# Iterate through the table to get all the stuffs

		SKU = response.xpath("//table[@style=\"border:2px #000000 solid; border-collapse:collapse; width: 100%\"]//td[1]//text()").extract()
		Model_number = response.xpath("//table[@style=\"border:2px #000000 solid; border-collapse:collapse; width: 100%\"]//td[4]//text()").extract()


		for sku in SKU[0:2]:
				new_link = 'https://www.homedepot.com/s/'+str(sku)
				# if (urllib.request.urlopen(new_link).getcode()) == 200:

				yield response.follow(new_link, callback=self.parse_homedepot,meta={'SB':SB, 'SKU':sku})

	def parse_homedepot(self,response):
	
		item = BodegaItem()


		try:
			name=response.xpath('//h1[@class="product-title__title"]/text()').extract().pop()
		except IndexError:
			name = 'Not Found'

		item['name'] = name
		item['SKU']  = response.meta['SKU']
		item['SB']  = response.meta['SB']
		#item['Model_number'] = 

		yield item




		