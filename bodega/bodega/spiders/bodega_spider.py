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

names =[]
prices =[]




def read_csv(name):
	data = pd.read_csv("C:\\Users\\Ousmane Kana\\Desktop\\Bodega\\dataBase\\"+str(name)+".csv")
	data = data.dropna(axis="columns", how="any")
	Model_Numbers = data['Model Numbers'].values.tolist()
	SKU =  data['SKU'].values.tolist()

	return(SKU)

def write_out(name):
	names.append(name)
	print(names)



# with open(r'C:\Users\Ousmane Kana\Desktop\Bodega\dataBase\ID.txt', 'w') as f:
#     for item in ID:
#         f.write("%s\n" % item)

def Wholesale_Link(item):
   
    link = "https://www.thdsalvage.com/Inventory/Detail?wid=8617&sbn="+str(item)+"&wid=8617&sbn="+str(item)
    return (link)


class Wholesale_Spider(scrapy.Spider):

	

	name = "wholesale"

	allowed_domain = ["https://www.thdsalvage.com/"]

	link = map(Wholesale_Link, ID)

	start_urls = list(link)[0:2]

	def parse(self, response):


	

		# filename = response.url.split("/")[-2]
		# 


		Category = response.xpath("//table[@style=\"text-align:right; width:100%\"]//td[1]//text()").extract()[8]

		Warehouse = response.xpath("//table[@style=\"text-align:right; width:100%\"]//td[1]//text()").extract()[6]

		Container_Qty = response.xpath("//table[@style=\"text-align:right; width:100%\"]//td[1]//text()").extract()[12]

		SB = response.xpath("//table[@style=\"text-align:right; width:100%\"]//td[1]//text()").extract()[2].strip(" ;")

		# Iterate through the table to get all the stuffs

		SKU = response.xpath("//table[@style=\"border:2px #000000 solid; border-collapse:collapse; width: 100%\"]//td[1]//text()").extract()
		Model_number = response.xpath("//table[@style=\"border:2px #000000 solid; border-collapse:collapse; width: 100%\"]//td[4]//text()").extract()


		for sku in SKU[0:1]:
				new_link = 'https://www.homedepot.com/s/'+str(sku)
				if (urllib.request.urlopen(new_link).getcode()) == 200:
					yield response.follow(new_link, callback=self.parse_homedepot,
	                                  meta={'SB':SB, 'SKU':sku})


		#List of the important Juice S

		#print(len(SKU))
		#print(len(Model_number))

		# price = response.xpath('//span[@class="price__dollars"]/text()').extract()
		# name = response.xpath('//h1[@class="product-title__title"]/text()').extract()

		# print("\n\n\n\n********************************")
		# print(f"The price is {price}")
		# print(f"The name is {name}")
		# print("\n\n\n\n********************************")

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

		





		


	
		


		#price= str(response.xpath('//span[@class="price__dollars"]/text()').extract().pop()).strip()
		
			# item['name'] =name
			# item['price'] = price


		




	


		#print(f"The current meta data is {response.meta['SB']}")
		#print(f"The current sku is {response.meta['SKU']}")

		# 
		# try:
		# 	item['name'] = response.xpath('//h1[@class="product-title__title"]/text()').extract().pop()
		# 	item['price'] = str(response.xpath('//span[@class="price__dollars"]/text()').extract().pop()).strip()
		# except:
		# 	item['name'] = 'Not found'
		# 	item['price'] = 'Not found'

		# item['name'] = response.xpath('//h1[@class="product-title__title"]/text()').extract().pop()
		# item['price'] = str(response.xpath('//span[@class="price__dollars"]/text()').extract().pop()).strip()
		


			# ItemsDf.to_csv(r"C:\Users\Ousmane Kana\Desktop\Bodega\dataBase\\"+str(SB)+".csv", index = False, header=True)

			# print(ItemsDf.head())

			# #print("*****************************************")
			# print("\nThe Category is {} is located in {} and the quantity of the container is {}\n\n".format(Category, Warehouse, Container_Qty))

			

			#print(SKU, Model_number)

	

		
		# item['name'] = response.xpath('//h1[@class="product-title__title"]/text()').extract()
		# item['price'] = int(response.xpath('//span[@class="price__dollars"]/text()').extract()[0])
			
			# with open(r"C:\Users\Ousmane Kana\Desktop\Bodega\dataBase\test1.csv", 'w') as myfile:
			# 	wr = csv.writer(myfile, delimiter='\t',lineterminator='\n')
			# 	wr.writerow(ID)

			
		







		