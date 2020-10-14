# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
import pandas as pd

SB =[]

class BodegaPipeline:

	


	def open_spider(self, spider):
		print("This is the OPEN SPIDER")


		self.file = open('test.txt', 'w')


		

	def close_spider(self, spider):
		
		print("This is the CLOSE SPIDER")
		
		self.file.close()


	def process_item(self, item, spider):

		print("This is the PROCESS ITEM STAGE")
		

		SB.append(item['SB']) if item['SB'] not in SB else SB

		print(SB)

		self.file = open(str(item['SB'])+'.txt', 'a+')

		
		line = json.dumps(ItemAdapter(item).asdict()) + "\n"

		print(line)

		self.file.write(line)

		
		return item
