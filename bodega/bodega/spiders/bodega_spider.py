import scrapy
import pandas as pd
import pandas as pd 


data = pd.read_excel('C:\\Users\\Ousmane Kana\\Desktop\\Bodega\\sbler-Copy.xlsx', header=None)

serials =data[0].tolist()

def LinkMaker(ID):
    
    link = "https://www.thdsalvage.com/Inventory/Detail?wid=8617&sbn="+str(ID)+"&wid=8617&sbn="+str(ID)
    return (link)





class BodegaSpider(scrapy.Spider):
	name = "homedepot"

	allowed_domain = ["https://www.thdsalvage.com/"]

	link = map(LinkMaker, serials)

	start_urls = list(link)


	def parse(self, response):
		# filename = response.url.split("/")[-2]
		# with open(filename, "wb") as f:
		# 	f.write(response.body)

		Category = response.xpath("//table[@style=\"text-align:right; width:100%\"]//td[1]//text()").extract()[8]

		Warehouse = response.xpath("//table[@style=\"text-align:right; width:100%\"]//td[1]//text()").extract()[6]

		Container_Qty = response.xpath("//table[@style=\"text-align:right; width:100%\"]//td[1]//text()").extract()[12]

		# Iterate through the table to get all the stuffs

		SKU = response.xpath("//table[@style=\"border:2px #000000 solid; border-collapse:collapse; width: 100%\"]//td[1]//text()").extract()
		Model_number = response.xpath("//table[@style=\"border:2px #000000 solid; border-collapse:collapse; width: 100%\"]//td[4]//text()").extract()


		#List of the important Juice 

		# print(len(SKU))
		# print(len(Model_number))


		ItemsDf = pd.DataFrame(list(zip(SKU, Model_number)), columns =['SKU', "Model Numbers"])

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