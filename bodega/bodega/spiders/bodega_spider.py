import scrapy
import sys
import time
from ..items import BodegaItem
import pandas as pd
import csv
import re
import os 
from tkinter import filedialog
from tkinter import *


# Start by extracting the data from the initial CVS and load them into the ID list

# Use the GUI to ask where is the inintial csv located at. 

current_dir = os.getcwd()
root = Tk()

root.filename =  filedialog.askopenfilename(initialdir = current_dir,title = "Select file",filetypes = (("excel file ma niggah","*.xlsx"),("all files","*.*")))
print(root.filename)
root.destroy()

data = pd.read_excel(f'{root.filename}', header=None)
ID =data[0].tolist()


# Create the receiving CSVs and na,e each of them according to their ID's

# Use the GUI to also ask where the saving DataBase is ????
if not os.path.exists('dataBase'):
    os.makedirs('dataBase')

for element in ID:
	with open(f'dataBase\\{str(element)}.csv', mode='w', newline='') as csv_file:
		fieldnames = ['SKU', 'Model_number','Name','Wholesale_Price','HD_Price','Final_Price']
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

	start_urls = list(link)

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
		for i in range(len(SKU)):
				#Generate the homepedot price according to the SKU
				new_link = 'https://www.homedepot.com/s/'+str(Model_number[i])
				# if (urllib.request.urlopen(new_link).getcode()) == 200:
				# Follow the link generated to second craweler. Passes extra argument to parse_homedepot using meta {}
				yield response.follow(new_link, callback=self.parse_homedepot,meta={'SB':SB, 'SKU':SKU[i], 'Model_number': Model_number[i], 'Wholesale_Price':Wholesale_Price[i].strip("$"), 'Iterated': False})

	def parse_homedepot(self,response):
		
		#Instantiation of the item object for the output feed
		SKU = response.meta['SKU']
		SB = response.meta['SB']
		Model_number = response.meta['Model_number']
		Wholesale_Price = response.meta['Wholesale_Price']
 
		print(f"*********\nThe Current page being parsed is{response.url} in HD1\n***********")

		try:
			name=response.xpath('//h1[@class="product-title__title"]/text()').extract().pop()
		except IndexError:
			
			try:
				name=response.xpath('//h1[@class="product-details__title"]/text()').extract().pop()
			except IndexError:
				name = "Not found"

		if name =="Not found":
			new_link = 'https://www.homedepot.com/s/'+str(SKU)
			yield response.follow(new_link, callback=self.parse_homedepot2,meta={'SB':SB, 'SKU':SKU, 'Model_number': Model_number, 'Wholesale_Price':Wholesale_Price})
		else:
			try:
				price = response.xpath('//div[@class="price"]')[0].extract()
				price = re.findall(r'\d+',price)
				price ="$"+".".join(price[:2])  
			except IndexError:
				
				try:
					price = response.xpath('//span[@id="ajaxPrice"]').extract().pop()
					price = re.findall(r'\d+',price)
					price ="$"+".".join(price[:2])
				except IndexError:
					price = 'Not Found'

			item = BodegaItem()
			item['Name'] = name
			item['HD_Price']= price
			item['SKU']  = response.meta['SKU']
			item['SB']  = response.meta['SB']
			item['Model_number'] = response.meta['Model_number']
			item['Wholesale_Price'] = response.meta['Wholesale_Price']


			yield item



	def parse_homedepot2(self, response):
		item = BodegaItem()
		SKU = response.meta['SKU']
		SB = response.meta['SB']
		Model_number = response.meta['Model_number']
		Wholesale_Price = response.meta['Wholesale_Price']



		print(f"*********\nThe Current page being parsed is{response.url} in HD2 \n***********")
		#Parse throught the homedepot page of the item and get the price and name if exists
		try:
			name=response.xpath('//h1[@class="product-details__title"]/text()').extract().pop()

		except IndexError:
			print('Second Name try hd2')
			try:
				name=response.xpath('//h1[@class="product-title__title"]/text()').extract().pop()
			except IndexError:
				name = 'Not found'


		try:
			price = response.xpath('//div[@class="price"]')[0].extract()
			price = re.findall(r'\d+',price)
			price ="$"+".".join(price[:2])  
		except IndexError:
			print('Second price try')
			try:
				price = response.xpath('//span[@id="ajaxPrice"]').extract().pop()
				price = re.findall(r'\d+',price)
				price ="$"+".".join(price[:2])
			except IndexError:
				price = 'Not Found'

		
		#Load the item object before yielding it for output to pipeline.py
		item['Name'] = name
		item['HD_Price']= price
		item['SKU']  = response.meta['SKU']
		item['SB']  = response.meta['SB']
		item['Model_number'] = response.meta['Model_number']
		item['Wholesale_Price'] = response.meta['Wholesale_Price']
		

		yield item

