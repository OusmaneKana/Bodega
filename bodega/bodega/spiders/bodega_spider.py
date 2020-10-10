import scrapy
import pandas as pd
import time
import openpyxl
from bodega.items import BodegaItem
import csv

data = pd.read_excel('C:\\Users\\Ousmane Kana\\Desktop\\Bodega\\sbler-Copy.xlsx', header=None)

ID =data[0].tolist()



def read_csv(name):
	data = pd.read_csv("C:\\Users\\Ousmane Kana\\Desktop\\Bodega\\dataBase\\"+str(name)+".csv")
	data = data.dropna(axis="columns", how="any")
	Model_Numbers = data['Model Numbers'].values.tolist()
	SKU =  data['SKU'].values.tolist()

	return(SKU)


with open(r'C:\Users\Ousmane Kana\Desktop\Bodega\dataBase\ID.txt', 'w') as f:
    for item in ID:
        f.write("%s\n" % item)

def Wholesale_Link(item):
   
    link = "https://www.thdsalvage.com/Inventory/Detail?wid=8617&sbn="+str(item)+"&wid=8617&sbn="+str(item)
    return (link)


class Wholesale_Spider(scrapy.Spider):

	name = "wholesale"

	allowed_domain = ["https://www.thdsalvage.com/"]

	link = map(Wholesale_Link, ID)

	start_urls = list(link)


	def parse(self, response):
		# filename = response.url.split("/")[-2]
		# with open(filename, "wb") as f:
		# 	f.write(response.body)



		Category = response.xpath("//table[@style=\"text-align:right; width:100%\"]//td[1]//text()").extract()[8]

		Warehouse = response.xpath("//table[@style=\"text-align:right; width:100%\"]//td[1]//text()").extract()[6]

		Container_Qty = response.xpath("//table[@style=\"text-align:right; width:100%\"]//td[1]//text()").extract()[12]

		SB = response.xpath("//table[@style=\"text-align:right; width:100%\"]//td[1]//text()").extract()[2].strip(" ;")

		# Iterate through the table to get all the stuffs

		SKU = response.xpath("//table[@style=\"border:2px #000000 solid; border-collapse:collapse; width: 100%\"]//td[1]//text()").extract()
		Model_number = response.xpath("//table[@style=\"border:2px #000000 solid; border-collapse:collapse; width: 100%\"]//td[4]//text()").extract().replace(" ","")


		#List of the important Juice 

		# print(len(SKU))
		# print(len(Model_number))


		ItemsDf = pd.DataFrame(list(zip(SKU, Model_number)), columns =['SKU', "Model Numbers"])

		ItemsDf.to_csv(r"C:\Users\Ousmane Kana\Desktop\Bodega\dataBase\\"+str(SB)+".csv", index = False, header=True)

		print(ItemsDf.head())

		#print("*****************************************")
		print("\nThe Category is {} is located in {} and the quantity of the container is {}\n\n".format(Category, Warehouse, Container_Qty))

		

		#print(SKU, Model_number)
		print("*****************************************")

		# price = response.xpath('//span[@class="price__dollars"]/text()').extract()
		# name = response.xpath('//h1[@class="product-title__title"]/text()').extract()

		# print("\n\n\n\n********************************")
		# print(f"The price is {price}")
		# print(f"The name is {name}")
		# print("\n\n\n\n********************************")

class Homedepot_spider(scrapy.Spider):





	name ="homedepot"


	allowed_domains = ["www.homedepot.com"]




	def start_requests(self):
		global itter, models, element

		itter = 0 
		models = 0
		elements = 0



		# ID  here is the list of all the elements from the BIG CSV
		for element in ID:
			elements = element
			#Models are the read of the read_csv is return a list of the model#s
			for model in read_csv(element):
				models = model


					

					
				link = ("https://www.homedepot.com/s/"+str(model))
					
				itter = itter +1


				yield scrapy.Request(link, self.parse)

	def parse(self,response):

		item = BodegaItem()

		try:
			name = response.xpath('//h1[@class="product-title__title"]/text()').extract().pop()
			price = str(response.xpath('//span[@class="price__dollars"]/text()').extract().pop()).strip()
			item['name'] =name
			item['price'] = price

			print(price)
			print(name)

		except IndexError:
			price ='Not Found'
			item['price'] = price
			print(price)

		yield item


		
		# item['name'] = response.xpath('//h1[@class="product-title__title"]/text()').extract()
		# item['price'] = int(response.xpath('//span[@class="price__dollars"]/text()').extract()[0])
			
			# with open(r"C:\Users\Ousmane Kana\Desktop\Bodega\dataBase\test1.csv", 'w') as myfile:
			# 	wr = csv.writer(myfile, delimiter='\t',lineterminator='\n')
			# 	wr.writerow(ID)

			
		







		