# -*- coding: utf-8 -*-
import sys
import os

import traceback
import ujson
from pprint import pprint
from textblob import TextBlob as tb
from textblob import Word as wd
import shutil
from collections import defaultdict

from socialconfig import config

class get_iterable(object):


	def __init__(self, rfname):
		self.read_file = rfname

	def __iter__(self):
		try:
			with open(self.read_file,'r') as file:
				for line in file:
					yield line
		except:
			print("Error iterating over file: {file}".format(file=self.read_file))
			raise

class segregate_reviews_by_category(object):

	business_to_cat = defaultdict(set)
	"""docstring for ClassName"""
	def __init__(self):
		pass

	def load_business_to_category_mapping(self,parse_directory=None):
		if not parse_directory:
			raise
		for file in os.listdir(parse_directory):
			abs_file_path = os.path.join(parse_directory,file)
			if "yelp_businesses_in_category_" in file:
				category = abs_file_path.split("_")[-1][:-4]
				with open(abs_file_path,'r'):
					businesses = get_iterable(abs_file_path)
					for busi in businesses:
						bus = ujson.loads(busi)
						bus_id = bus.split(" ")[0]
						bus_id = bus_id
						self.business_to_cat[bus_id].add(category)

	def strip_special_chars(self,word):
		if len(word.rstrip("@!#\"%&()*,-'./:;<=>?[\\]^_`{|}~").lstrip("!@#'\"%&()*,-./:;<=>?[\\]^_`{|}~")) > 1:
			if self.has_special_chars(word.rstrip("@!#\"%&()*,-'./:;<=>?[\\]^_`{|}~").lstrip("!@#'\"%&()*,-./:;<=>?[\\]^_`{|}~")):			
				self.strip_special_chars(word.rstrip("@!#\"%&()*,-'./:;<=>?[\\]^_`{|}~").lstrip("!@#'\"%&()*,-./:;<=>?[\\]^_`{|}~"))
			return word.rstrip("@!#\"%&()*,-'./:;<=>?[\\]^_`{|}~").lstrip("!@#'\"%&()*,-./:;<=>?[\\]^_`{|}~")
		else:
			return ""
	
	def has_special_chars(self,word):
		if word[0] in "@!#\"%&()*,-'./:;<=>?[\\]^_`{|}~" or word[-1] in "@!#\"%&()*,-'./:;<=>?[\\]^_`{|}~":
			return True
		return False
		
	def process(self):
		# directory where reviews are kept
		SAVE_REVIEWS_DIRECTORY = config.get("SAVE_REVIEWS_DIRECTORY",None)
		SAVE_REVIEWS_BY_CATEGORY_DIRECTORY = config.get("SAVE_REVIEWS_BY_CATEGORY_DIRECTORY",None)
		PROCESS_N_REVIEWS_ONLY = int(config.get("PROCESS_N_REVIEWS_ONLY",1000000))
		print("Will process only {num} reviews as per the directive in the socialconfig.py".format(num=str(PROCESS_N_REVIEWS_ONLY)))

		if not (SAVE_REVIEWS_DIRECTORY and SAVE_REVIEWS_BY_CATEGORY_DIRECTORY):
			print("config keys are not set correctly in the config file: socialconfig.py")
			exit(0)

		if not os.path.exists(SAVE_REVIEWS_BY_CATEGORY_DIRECTORY) and not os.path.isdir(SAVE_REVIEWS_BY_CATEGORY_DIRECTORY):
			os.makedirs(SAVE_REVIEWS_BY_CATEGORY_DIRECTORY)
		
		bars_file_counter,food_file_counter,grooming_file_counter,learn_file_counter,leisure_file_counter,municipal_file_counter,planning_file_counter,services_file_counter,shopping_file_counter,sports_file_counter,health_file_counter,other_file_counter = 0,0,0,0,0,0,0,0,0,0,0,0
		bars_dir = os.path.join(SAVE_REVIEWS_BY_CATEGORY_DIRECTORY,"bars")
		if not (os.path.exists(bars_dir) and os.path.isdir(bars_dir)):
			os.makedirs(bars_dir)
		bars_file_path = os.path.join(bars_dir,"yelp_reviews_bars_1.txt")

		food_dir = os.path.join(SAVE_REVIEWS_BY_CATEGORY_DIRECTORY,"food")
		if not (os.path.exists(food_dir) and os.path.isdir(food_dir)):
			os.makedirs(food_dir)
		food_file_path = os.path.join(food_dir,"yelp_reviews_food_1.txt")

		grooming_dir = os.path.join(SAVE_REVIEWS_BY_CATEGORY_DIRECTORY,"grooming")
		if not (os.path.exists(grooming_dir) and os.path.isdir(grooming_dir)):
			os.makedirs(grooming_dir)
		grooming_file_path = os.path.join(grooming_dir,"yelp_reviews_grooming_1.txt")

		learn_dir = os.path.join(SAVE_REVIEWS_BY_CATEGORY_DIRECTORY,"learn")
		if not (os.path.exists(learn_dir) and os.path.isdir(learn_dir)):
			os.makedirs(learn_dir)
		learn_file_path = os.path.join(learn_dir,"yelp_reviews_learn_1.txt")

		leisure_dir = os.path.join(SAVE_REVIEWS_BY_CATEGORY_DIRECTORY,"leisure")
		if not (os.path.exists(leisure_dir) and os.path.isdir(leisure_dir)):
			os.makedirs(leisure_dir)
		leisure_file_path = os.path.join(leisure_dir,"yelp_reviews_leisure_1.txt")

		municipal_dir = os.path.join(SAVE_REVIEWS_BY_CATEGORY_DIRECTORY,"municipal")
		if not (os.path.exists(municipal_dir) and os.path.isdir(municipal_dir)):
			os.makedirs(municipal_dir)
		municipal_file_path = os.path.join(municipal_dir,"yelp_reviews_municipal_1.txt")

		planning_dir = os.path.join(SAVE_REVIEWS_BY_CATEGORY_DIRECTORY,"planning")
		if not (os.path.exists(planning_dir) and os.path.isdir(planning_dir)):
			os.makedirs(planning_dir)
		planning_file_path = os.path.join(planning_dir,"yelp_reviews_planning_1.txt")

		services_dir = os.path.join(SAVE_REVIEWS_BY_CATEGORY_DIRECTORY,"services")
		if not (os.path.exists(services_dir) and os.path.isdir(services_dir)):
			os.makedirs(services_dir)
		services_file_path = os.path.join(services_dir,"yelp_reviews_services_1.txt")

		shopping_dir = os.path.join(SAVE_REVIEWS_BY_CATEGORY_DIRECTORY,"shopping")
		if not (os.path.exists(shopping_dir) and os.path.isdir(shopping_dir)):
			os.makedirs(shopping_dir)
		shopping_file_path = os.path.join(shopping_dir,"yelp_reviews_shopping_1.txt")

		sports_dir = os.path.join(SAVE_REVIEWS_BY_CATEGORY_DIRECTORY,"sports")
		if not (os.path.exists(sports_dir) and os.path.isdir(sports_dir)):
			os.makedirs(sports_dir)
		sports_file_path = os.path.join(sports_dir,"yelp_reviews_sports_1.txt")

		health_dir = os.path.join(SAVE_REVIEWS_BY_CATEGORY_DIRECTORY,"health")
		if not (os.path.exists(health_dir) and os.path.isdir(health_dir)):
			os.makedirs(health_dir)
		health_file_path = os.path.join(health_dir,"yelp_reviews_health_1.txt")

		other_dir = os.path.join(SAVE_REVIEWS_BY_CATEGORY_DIRECTORY,"other")
		if not (os.path.exists(other_dir) and os.path.isdir(other_dir)):
			os.makedirs(other_dir)
		other_file_path = os.path.join(other_dir,"yelp_reviews_other_1.txt")


		bars_file = open(bars_file_path,'w')
		food_file = open(food_file_path,'w')
		grooming_file = open(grooming_file_path,'w')
		learn_file = open(learn_file_path,'w')
		leisure_file = open(leisure_file_path,'w')
		municipal_file = open(municipal_file_path,'w')
		planning_file = open(planning_file_path,'w')
		services_file = open(services_file_path,'w')
		shopping_file = open(shopping_file_path,'w')
		sports_file = open(sports_file_path,'w')
		health_file = open(health_file_path,'w')
		other_file = open(other_file_path,'w')

		review_counter = 0
		for file in os.listdir(SAVE_REVIEWS_DIRECTORY):
			if not os.path.isdir(file):
				abs_file_path = os.path.join(SAVE_REVIEWS_DIRECTORY,file)
				if "yelp_reviews_" in file:
					reviews = get_iterable(abs_file_path)
					for review in reviews:
						review_counter += 1
						review_dict = ujson.loads(review)
						business_id = review_dict.get("business_id",None)
						review_text = review_dict.get("review_text",None)
						
						wiki = tb(review_text)
						tags = wiki.tags
						adj_words_list = [wd(fword).lemmatize("a") for fword in 
						[self.strip_special_chars(word.lower()) for word,tag in tags if tag in ["JJ","JJR","JJS"] and len(word) > 2]
						 if len(fword) > 2]					
						adj_list_string = " ".join(adj_words_list)
						review_dict.update({"adjectives":adj_list_string})
						write_line = ujson.dumps(review_dict)

						cat_list = self.business_to_cat.get(business_id,[])
						for cat in cat_list:
							if cat == "bars":
								bars_file.write(write_line + "\n")
								bars_file_counter += 1
								if bars_file_counter%25000 == 0:
									del bars_file
									old_bars_file = bars_file_path
									new_bars_file = os.path.join(bars_dir,"yelp_reviews_bars_{c}.txt".format(c=str(int((bars_file_counter+1)/25000)+1)))
									print("25000 Reviews collected in `BARS` category, creating a new file to keep file sizes manageable")
									print('Changing file from : {old_bars_file} to {new_bars_file}'.format(old_bars_file=old_bars_file,new_bars_file=new_bars_file))
									bars_file = open(new_bars_file,'w')
							elif cat == "food":
								food_file.write(write_line + "\n")
								food_file_counter += 1
								if food_file_counter%25000 == 0:
									del food_file
									old_food_file = food_file_path
									new_food_file = os.path.join(food_dir,"yelp_reviews_food_{c}.txt".format(c=str(int((food_file_counter+1)/25000)+1)))
									print("25000 Reviews collected in `food` category, creating a new file to keep file sizes manageable")
									print('Changing file from : {old_food_file} to {new_food_file}'.format(old_food_file=old_food_file,new_food_file=new_food_file))
									food_file = open(new_food_file,'w')
							elif cat == "grooming":
								grooming_file.write(write_line + "\n")
								grooming_file_counter += 1
								if grooming_file_counter%25000 == 0:
									del grooming_file
									old_grooming_file = grooming_file_path
									new_grooming_file = os.path.join(grooming_dir,"yelp_reviews_grooming_{c}.txt".format(c=str(int((grooming_file_counter+1)/25000)+1)))
									print("25000 Reviews collected in `grooming` category, creating a new file to keep file sizes manageable")
									print('Changing file from : {old_grooming_file} to {new_grooming_file}'.format(old_grooming_file=old_grooming_file,new_grooming_file=new_grooming_file))
									grooming_file = open(new_grooming_file,'w')
							elif cat == "learn":
								learn_file.write(write_line + "\n")
								learn_file_counter += 1
								if learn_file_counter%25000 == 0:
									del learn_file
									old_learn_file = learn_file_path
									new_learn_file = os.path.join(learn_dir,"yelp_reviews_learn_{c}.txt".format(c=str(int((learn_file_counter+1)/25000)+1)))
									print("25000 Reviews collected in `learn` category, creating a new file to keep file sizes manageable")
									print('Changing file from : {old_learn_file} to {new_learn_file}'.format(old_learn_file=old_learn_file,new_learn_file=new_learn_file))
									learn_file = open(new_learn_file,'w')
							elif cat == "leisure":
								leisure_file.write(write_line + "\n")
								leisure_file_counter += 1
								if leisure_file_counter%25000 == 0:
									del leisure_file
									old_leisure_file = leisure_file_path
									new_leisure_file = os.path.join(learn_dir,"yelp_reviews_leisure_{c}.txt".format(c=str(int((leisure_file_counter+1)/25000)+1)))
									print("25000 Reviews collected in `leisure` category, creating a new file to keep file sizes manageable")
									print('Changing file from : {old_leisure_file} to {new_leisure_file}'.format(old_leisure_file=old_leisure_file,new_leisure_file=new_leisure_file))
									leisure_file = open(new_leisure_file,'w')
							elif cat == "municipal":
								municipal_file.write(write_line + "\n")
								municipal_file_counter += 1
								if municipal_file_counter%25000 == 0:
									del municipal_file
									old_municipal_file = municipal_file_path
									new_municipal_file = os.path.join(municipal_dir,"yelp_reviews_municipal_{c}.txt".format(c=str(int((municipal_file_counter+1)/25000)+1)))
									print("25000 Reviews collected in `municipal` category, creating a new file to keep file sizes manageable")
									print('Changing file from : {old_municipal_file} to {new_municipal_file}'.format(old_municipal_file=old_municipal_file,new_municipal_file=new_municipal_file))
									municipal_file = open(new_municipal_file,'w')
							elif cat == "planning":
								planning_file.write(write_line + "\n")
								planning_file_counter += 1
								if planning_file_counter%25000 == 0:
									del planning_file
									old_planning_file = planning_file_path
									new_planning_file = os.path.join(planning_dir,"yelp_reviews_planning_{c}.txt".format(c=str(int((planning_file_counter+1)/25000)+1)))
									print("25000 Reviews collected in `planning` category, creating a new file to keep file sizes manageable")
									print('Changing file from : {old_planning_file} to {new_planning_file}'.format(old_planning_file=old_planning_file,new_planning_file=new_planning_file))
									planning_file = open(new_planning_file,'w')
							elif cat == "services":
								services_file.write(write_line + "\n")
								services_file_counter += 1
								if services_file_counter%25000 == 0:
									del services_file
									old_services_file = services_file_path
									new_services_file = os.path.join(services_dir,"yelp_reviews_services_{c}.txt".format(c=str(int((services_file_counter+1)/25000)+1)))
									print("25000 Reviews collected in `services` category, creating a new file to keep file sizes manageable")
									print('Changing file from : {old_services_file} to {new_services_file}'.format(old_services_file=old_services_file,new_services_file=new_services_file))
									services_file = open(new_services_file,'w')
							elif cat == "shopping":
								shopping_file.write(write_line + "\n")
								shopping_file_counter += 1
								if shopping_file_counter%25000 == 0:
									del shopping_file
									old_shopping_file = shopping_file_path
									new_shopping_file = os.path.join(shopping_dir,"yelp_reviews_shopping_{c}.txt".format(c=str(int((shopping_file_counter+1)/25000)+1)))
									print("25000 Reviews collected in `shopping` category, creating a new file to keep file sizes manageable")
									print('Changing file from : {old_shopping_file} to {new_shopping_file}'.format(old_shopping_file=old_shopping_file,new_shopping_file=new_shopping_file))
									shopping_file = open(new_shopping_file,'w')
							elif cat == "sports":
								sports_file.write(write_line + "\n")
								sports_file_counter += 1
								if sports_file_counter%25000 == 0:
									del sports_file
									old_sports_file = sports_file_path
									new_sports_file = os.path.join(sports_dir,"yelp_reviews_sports_{c}.txt".format(c=str(int((sports_file_counter+1)/25000)+1)))
									print("25000 Reviews collected in `sports` category, creating a new file to keep file sizes manageable")
									print('Changing file from : {old_sports_file} to {new_sports_file}'.format(old_sports_file=old_sports_file,new_sports_file=new_sports_file))
									sports_file = open(new_sports_file,'w')
							elif cat == "health":
								health_file.write(write_line + "\n")
								health_file_counter += 1
								if health_file_counter%25000 == 0:
									del health_file
									old_health_file = health_file_path
									new_health_file = os.path.join(health_dir,"yelp_reviews_health_{c}.txt".format(c=str(int((health_file_counter+1)/25000)+1)))
									print("25000 Reviews collected in `health` category, creating a new file to keep file sizes manageable")
									print('Changing file from : {old_health_file} to {new_health_file}'.format(old_health_file=old_health_file,new_health_file=new_health_file))
									health_file = open(new_health_file,'w')
							else:
								other_file.write(write_line + "\n")
								other_file_counter += 1
								if other_file_counter%25000 == 0:
									del other_file
									old_other_file = other_file_path
									new_other_file = os.path.join(other_dir,"yelp_reviews_other_{c}.txt".format(c=str(int((other_file_counter+1)/25000)+1)))
									print("25000 Reviews collected in `other` category, creating a new file to keep file sizes manageable")
									print('Changing file from : {old_other_file} to {new_other_file}'.format(old_other_file=old_other_file,new_other_file=new_other_file))
									other_file = open(new_other_file,'w')
								print("Excluded Category encountered: {cat}".format(cat=cat))

						if review_counter%100 == 0:
							print("{num}00 reviews processed".format(num=(str(int(review_counter/100)))))

						if review_counter >= PROCESS_N_REVIEWS_ONLY:
							break

		print("{count} Reviews processed".format(count=review_counter))


if __name__ == "__main__":
	
	SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY = config.get("SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY",None)
	if not SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY:
		print("Cannot load business_id to business_category mappings as the location(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY) of the files that hold those mappings is not specified correctly in the config file socialconfig.py")
		exit()
	if not (os.path.exists(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY) and os.path.isdir(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY)):
		print("{SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY} is either not a valid directory or it does not exist".format(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY=SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY))
		exit()

	# initialise class
	ps = segregate_reviews_by_category()

	ps.load_business_to_category_mapping(SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY)
	# call process() method
	ps.process()