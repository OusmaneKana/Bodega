import scrapy
import pandas as pd
import pandas as pd 


data = pd.read_excel('C:\\Users\\Ousmane Kana\\OneDrive\\Projects\\Bodega\\sbler.xlsx', header=None)

serials =data[0].tolist()


class BodegaSpider(scrapy.Spider):
	name = "homedepot"
	allowed_domain = ["https://www.thdsalvage.com/"]



	start_urls = ['https://www.thdsalvage.com/Inventory/Detail?wid=8617&sbn=557223&wid=8617&sbn=557223']


	def parse(self, response):
		# filename = response.url.split("/")[-2]
		# with open(filename, "wb") as f:
		# 	f.write(response.body)


		SKU = response.xpath("//table[@style=\"border:2px #000000 solid; border-collapse:collapse; width: 100%\"]//td[1]//text()").extract()

		Model_number = response.xpath("//table[@style=\"border:2px #000000 solid; border-collapse:collapse; width: 100%\"]//td[4]//text()").extract()

		print("*****************************************")

		print("The current output is ")


		print(SKU, Model_number)

		print("*****************************************")

		# price = response.xpath('//span[@class="price__dollars"]/text()').extract()
		# name = response.xpath('//h1[@class="product-title__title"]/text()').extract()

		# print("\n\n\n\n********************************")
		# print(f"The price is {price}")
		# print(f"The name is {name}")
		# print("\n\n\n\n********************************")