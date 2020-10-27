# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
import pandas as pd
import csv
import time


class BodegaPipeline:

	def open_spider(self, spider):
		self.start_time = time.time()

		#Create an text file as output log
		self.file_txt = open('dataBase\\output_log.txt', 'w')


	def close_spider(self, spider):
		
		# print("This is the CLOSE SPIDER")

		# Closes both the csv and the txt file(s)


		self.file_txt.close()

		self.file_csv.close()
		print("--- %s seconds ---" % (time.time() - self.start_time))


	def process_item(self, item, spider):


		#Overrite the CSVs that were crated at the beginning of the program execution in bodega_spider.py
		
		if item['HD_Price'] == 'Not Found':
			Final_Price = (float(item['Wholesale_Price']) *15)/100 + float(item['Wholesale_Price'])
		else:
			Final_Price = item['HD_Price']

		item['Final_Price']=Final_Price



		self.file_csv = open('dataBase\\'+str(item['SB'])+'.csv', 'a+', newline='')
		fieldnames = ['SKU', 'Model_number','Name','Wholesale_Price','HD_Price','Final_Price']
		self.writer = csv.DictWriter(self.file_csv, fieldnames=fieldnames)

		line = json.dumps(ItemAdapter(item).asdict()) +"\n"

		# Pops the SB before writing it to the CSV to avoid a Missing header Error
		item.pop('SB', None)

		self.writer.writerow(item)		
		# Writes to the output_log.txt
		self.file_txt.write(line)		
		#Footrpint
		#print(line)

		

		
		return item
