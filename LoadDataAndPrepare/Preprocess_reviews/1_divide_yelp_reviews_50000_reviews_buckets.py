# -*- coding: utf-8 -*-
import sys
import os

import traceback
import ujson
from pprint import pprint

from socialconfig import config

class get_reviews_iterable(object):


	def __init__(self, rfname):
		self.read_file = rfname

	def __iter__(self):
		try:
			with open(self.read_file,'r') as file:
				for line in file:
					yield line
		except:
			print("Error occurred while traversing reviews: {error}".format(error=traceback.format_exc()))
			raise

class preprocess_reviews(object):
	"""docstring for ClassName"""
	def __init__(self):
		pass
		
	def process(self):
		# directory where stories are kept
		YELP_DATASET_DIR = config.get("YELP_DATASET_DIR",None)
		YELP_REVIEWS_FILE_NAME = config.get("YELP_REVIEWS_FILE_NAME",None)
		SAVE_REVIEWS_DIRECTORY = config.get("SAVE_REVIEWS_DIRECTORY",None)

		if not (YELP_DATASET_DIR and YELP_REVIEWS_FILE_NAME and SAVE_REVIEWS_DIRECTORY):
			print("config keys are not set correctly in the config file: socialconfig.py")
			exit(0)

		if not (os.path.exists(YELP_DATASET_DIR) and os.path.isdir(YELP_DATASET_DIR)):
			print("Either Yelp Dataset directory path is not set correctly in the socialconfig.py file \nOR\
					\nThe directory does not exist. Please make sure you have downloaded the yelp dataset(in JSON format) and copied the `yelp_academic_dataset_business.json` and `yelp_academic_dataset_business.json` files into the yelp_dataset sub-directory of your project directory(socialsentRun)")
			exit()

		YELP_REVIEWS_ABS_FILE_PATH = os.path.join(YELP_DATASET_DIR,YELP_REVIEWS_FILE_NAME)
		
		YELP_BUSINESSES_FILE_NAME = config.get("YELP_BUSINESSES_FILE_NAME",None)
		YELP_BUSINESSES_ABS_FILE_PATH = os.path.join(YELP_DATASET_DIR,YELP_BUSINESSES_FILE_NAME)

		try:
			f = open(YELP_REVIEWS_ABS_FILE_PATH,'r')
			if f:
				f.close()
		except IOError:
			msg = "Error opening file: {}".format((YELP_REVIEWS_FILE_NAME))
			print(msg)
			print(traceback.format_exc())
			exit()	
		if not (os.path.exists(SAVE_REVIEWS_DIRECTORY) and os.path.isdir(SAVE_REVIEWS_DIRECTORY)):
			os.makedirs(SAVE_REVIEWS_DIRECTORY)
			print("Created directory: {d} to save yelp reviews in buckets of 50,000 reviews per file".format(d=SAVE_REVIEWS_DIRECTORY))
				
		write_file_first = os.path.join(SAVE_REVIEWS_DIRECTORY,'yelp_reviews_0_50000.json')

		wfile = open(write_file_first,'w')
		reviews = get_reviews_iterable(YELP_REVIEWS_ABS_FILE_PATH)
		i = 0

		print("Reading Yelp Reviews")
		for line in reviews:
			i += 1
			json_dict = ujson.loads(line)
			review_text = json_dict.get("text",None)
			business_id = json_dict.get("business_id",None)
			review_id = json_dict.get("review_id",None)
			review_rating = json_dict.get("stars",None)

			if not (review_id or business_id or review_text or review_rating):
				continue
			review_text = review_text
			business_id = business_id
			review_id = review_id
			write_dict = {}
			write_dict['business_id'] = business_id
			write_dict['review_text'] = review_text
			write_dict['review_id'] = review_id
			write_dict['rating'] = review_rating

			wfile.write(ujson.dumps(write_dict) + "\n")
			
			if i%100 == 0:
				print("{num}00 reviews processed".format(num=str(int(i/100))))
			if i%50000 == 0:
				new_file = os.path.join(SAVE_REVIEWS_DIRECTORY,'yelp_reviews_{from_num}_{to_num}.json'.format(from_num=(i+1),to_num=(i+50000)))
				old_file = write_file_first
				print("Changing file from {old_file} to {new_file}".format(old_file=old_file,new_file=new_file))
				del wfile
				wfile = open(new_file,'w')
		del wfile		
		print("Processed {total} reviews".format(total=str(i)))

if __name__ == "__main__":
	# initialise class
	ps = preprocess_reviews()

	# call process() method
	ps.process()