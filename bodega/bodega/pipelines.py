# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
import pandas as pd
import csv



class BodegaPipeline:


	

	def open_spider(self, spider):
		print("This is the OPEN SPIDER")


		self.file_txt = open('test.txt', 'w')


		

	def close_spider(self, spider):
		
		print("This is the CLOSE SPIDER")

	
		self.file_txt.close()

		self.file_csv.close()


	def process_item(self, item, spider):

		self.file_csv = open(str(item['SB'])+'.csv', 'a+')
		fieldnames = ['name', 'SKU', 'SB']
		self.writer = csv.DictWriter(self.file_csv, fieldnames=fieldnames)

		self.writer.writerow(item)

		line = json.dumps(ItemAdapter(item).asdict()) + "\n"

		self.file_txt.write(line)


		print("This is the PROCESS ITEM STAGE")
		
		
		
		print(line)

		

		
		return item
