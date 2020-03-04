
# -*- coding: utf-8 -*-
import sys
import os
import copy
import traceback

from LoadDataAndPrepare.Category_to_subcat_mappings.advice_and_planning_subcategories_yelp import advice_and_planning_categories
from LoadDataAndPrepare.Category_to_subcat_mappings.bars_subcategories_yelp import bars_categories
from LoadDataAndPrepare.Category_to_subcat_mappings.food_subcategories_yelp import food_categories
from LoadDataAndPrepare.Category_to_subcat_mappings.grooming_subcategories_yelp import grooming_categories
from LoadDataAndPrepare.Category_to_subcat_mappings.health_and_doctor_subcategories_yelp import health_and_doctor_categories
from LoadDataAndPrepare.Category_to_subcat_mappings.learning_subcategories_yelp import learning_categories
from LoadDataAndPrepare.Category_to_subcat_mappings.municipal_subcategories_yelp import municipal_categories
from LoadDataAndPrepare.Category_to_subcat_mappings.services_subcategories_yelp import services_categories
from LoadDataAndPrepare.Category_to_subcat_mappings.sports_subcategories_yelp import sports_categories
from LoadDataAndPrepare.Category_to_subcat_mappings.travel_and_leisure_subcategories_yelp import travel_and_leisure_categories
from LoadDataAndPrepare.Category_to_subcat_mappings.shopping_subcategories_yelp import shopping_categories
from socialconfig import config

category_dict = {}
category_dict['bars'] = bars_categories
category_dict['grooming'] = grooming_categories
category_dict['food'] = food_categories
category_dict['planning'] = advice_and_planning_categories
category_dict['health'] = health_and_doctor_categories
category_dict['learn'] = learning_categories
category_dict['municipal'] = municipal_categories
category_dict['services'] = services_categories
category_dict['shopping'] = shopping_categories
category_dict['sports'] = sports_categories
category_dict['leisure'] = travel_and_leisure_categories

import ujson
from pprint import pprint

class get_businesses_iterable(object):


	def __init__(self, rfname):
		self.read_file = rfname

	def __iter__(self):
		try:
			with open(self.read_file,'r') as file:
				for line in file:
					yield line
		except:
			print("Error Occurred while iterating file: {f}".format(f=self.read_file))
			raise

class preprocess_businesses(object):
	"""docstring for ClassName"""
	def __init__(self):
		pass
		
	def process(self):
		# directory where stories are kept
		YELP_DATASET_DIR = config.get("YELP_DATASET_DIR",None)
		YELP_BUSINESSES_FILE_NAME = config.get("YELP_BUSINESSES_FILE_NAME",None)
		SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY = config.get("SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY",None)
		SAVE_BUSINESSES_BY_STATE_DIRECTORY = config.get("SAVE_BUSINESSES_BY_STATE_DIRECTORY",None)

		if not (YELP_DATASET_DIR and YELP_BUSINESSES_FILE_NAME and SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY and SAVE_BUSINESSES_BY_STATE_DIRECTORY):
			print("config keys are not set correctly in the config file: socialconfig.py")
			exit(0)

		if not (os.path.exists(YELP_DATASET_DIR) and os.path.isdir(YELP_DATASET_DIR)):
			print("Either Yelp Dataset directory path is not set correctly in the socialconfig.py file \nOR\
					\nThe directory does not exist. Please make sure you have downloaded the yelp dataset(in JSON format) and copied the `yelp_academic_dataset_business.json` and `yelp_academic_dataset_business.json` files into the yelp_dataset sub-directory of your project directory(socialsentRun)")
			exit()

		YELP_BUSINESSES_ABS_FILE_PATH = os.path.join(YELP_DATASET_DIR,YELP_BUSINESSES_FILE_NAME)
		try:
			f = open(YELP_BUSINESSES_ABS_FILE_PATH,'r')
			if f:
				f.close()
		except IOError:
			msg = "Error opening file: {f}".format(f=YELP_BUSINESSES_ABS_FILE_PATH)
			print(msg)
			print(traceback.format_exc())
			exit()
		
		if not (os.path.exists(SAVE_BUSINESSES_BY_STATE_DIRECTORY) and os.path.isdir(SAVE_BUSINESSES_BY_STATE_DIRECTORY)):
			os.makedirs(SAVE_BUSINESSES_BY_STATE_DIRECTORY)
		if not (os.path.exists(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY) and os.path.isdir(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY)):
			os.makedirs(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY)

		yelp_food_businesses_file = os.path.join(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY,"yelp_businesses_category_food.json")
		yelp_travel_and_leisure_businesses_file = os.path.join(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY,"yelp_businesses_category_travel_and_leisure.json")
		yelp_health_and_doctor_businesses_file = os.path.join(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY,"yelp_businesses_category_health_and_doctor.json")
		yelp_sports_businesses_file = os.path.join(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY,"yelp_businesses_category_sports.json")
		yelp_bars_businesses_file = os.path.join(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY,"yelp_businesses_category_bars.json")
		yelp_shopping_businesses_file = os.path.join(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY,"yelp_businesses_category_shopping.json")
		yelp_grooming_businesses_file = os.path.join(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY,"yelp_businesses_category_grooming.json")
		yelp_learning_businesses_file = os.path.join(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY,"yelp_businesses_category_learning.json")
		yelp_advice_businesses_file = os.path.join(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY,"yelp_businesses_category_advice.json")
		yelp_services_businesses_file = os.path.join(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY,"yelp_businesses_category_services.json")
		yelp_municipal_businesses_file = os.path.join(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY,"yelp_businesses_category_municipal.json")

				
									
		businesses = get_businesses_iterable(YELP_BUSINESSES_ABS_FILE_PATH)
		i = 0
		for line in businesses:
			i += 1
			json_dict = ujson.loads(line)
			bus_id = json_dict.get("business_id",None)
			state = json_dict.get("state",None)
			city = json_dict.get("city",None)
			sub_cats = json_dict.get("categories",None)
			rev_count = json_dict.get("review_count",None)

			classified_categories = set()
			if not (sub_cats and bus_id):
				continue
			for sub_cat in sub_cats.split(","):
				sub_cat = sub_cat.strip()
				for classfied_category in category_dict:
					for subcat in category_dict[classfied_category]:
						if sub_cat == subcat:
							classified_categories.add(classfied_category)
			write_files = []
			for final_cat in classified_categories:
				write_files.append(os.path.join(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY,"yelp_businesses_in_category_{final_cat}.csv".format(final_cat=final_cat)))

			if state:
				write_files.append(os.path.join(SAVE_BUSINESSES_BY_STATE_DIRECTORY,"yelp_businesses_in_state_{state}.csv".format(state=state)))

			for file in write_files:
				if os.path.exists(file) and os.path.isfile(file):
					write_mode = 'a'
				else:
					write_mode = 'w'

				if not state:
					state = "NoStateName_EncodingIssue"
				if not city:
					city = "NoCityName_EncodingIssue"
				if not rev_count:
					rev_count = 0
				
				write_str = ujson.dumps(' '.join([bus_id,state,city,str(rev_count)]))

				with open(file,write_mode) as wfile:
					try:
						wfile.write(write_str + "\n")
					except:
						print("Cannot write business_id:{bus_id} to {file}".format(bus_id=bus_id,file=file))
						print(traceback.format_exc())
						continue
			if i%100 == 0:
				print("{num}00 businesses processed".format(num=str(int(i/100))))
		print("Processed {num} businesses".format(num=str(i)))
				

# initialise class
ps = preprocess_businesses()

# call process() method
ps.process()