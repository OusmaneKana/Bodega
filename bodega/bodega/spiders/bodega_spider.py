import scrapy
import pandas as pd
import time


data = pd.read_excel('C:\\Users\\Ousmane Kana\\Desktop\\Bodega\\sbler-Copy.xlsx', header=None)

ID =data[0].tolist()


def read_csv(name):
	data = pd.read_csv(r'C:\Users\Ousmane Kana\Desktop\Bodega\dataBase\557223.csv')
	Model_Numbers = data['Model Numbers'].values.tolist()
	SKU =  data['SKU'].values.tolist()

	return(SKU)


with open(r'C:\Users\Ousmane Kana\Desktop\Bodega\dataBase\ID.txt', 'w') as f:
    for item in ID:
        f.write("%s\n" % item)

def Wholesale_Link(item):
   
    link = "https://www.thdsalvage.com/Inventory/Detail?wid=8617&sbn="+str(item)+"&wid=8617&sbn="+str(item)
    return (link)


def HD_Link(item):
    
    links= []
    
    for models in read_csv(ID):
        link = ("https://www.homedepot.com/s/"+str(models))
        links.append(link)

    return(links)


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
		Model_number = response.xpath("//table[@style=\"border:2px #000000 solid; border-collapse:collapse; width: 100%\"]//td[4]//text()").extract()


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


	allowed_domain = ["www.homedepot.com"]

	Links = map(HD_Link, ID)
	Link = list(Links)
	flat_list = [item for sublist in Link for item in sublist]
	print(flat_list[0:5])

	start_urls = flat_list[0:5]





	


	def parse(self,response):


		price = response.xpath('//span[@class="price__dollars"]/text()').extract()
		name = response.xpath('//h1[@class="product-title__title"]/text()').extract()

		print("\n\n\n\n********************************")
		print(response.url)
		print(f"The price is {price}")
		print(f"The name is {name}")
		print("\n\n\n\n********************************")







		