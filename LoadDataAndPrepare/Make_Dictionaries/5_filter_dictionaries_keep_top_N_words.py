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
from gensim.corpora import Dictionary

from socialconfig import config
from socialconfig import FOOD_POSITIVE_SEEDS,FOOD_NEGATIVE_SEEDS,BARS_POSITIVE_SEEDS,BARS_NEGATIVE_SEEDS,LEISURE_POSITIVE_SEEDS,LEISURE_NEGATIVE_SEEDS,GROOMING_POSITIVE_SEEDS,GROOMING_NEGATIVE_SEEDS,HEALTH_POSITIVE_SEEDS,HEALTH_NEGATIVE_SEEDS,LEARN_POSITIVE_SEEDS,LEARN_NEGATIVE_SEEDS,SHOPPING_POSITIVE_SEEDS,SHOPPING_NEGATIVE_SEEDS,PLANNING_POSITIVE_SEEDS,PLANNING_NEGATIVE_SEEDS,SERVICES_POSITIVE_SEEDS,SERVICES_NEGATIVE_SEEDS,SPORTS_POSITIVE_SEEDS,SPORTS_NEGATIVE_SEEDS,MUNICIPAL_POSITIVE_SEEDS,MUNICIPAL_NEGATIVE_SEEDS

class filter_dictionaries(object):
	"""docstring for ClassName"""
	def __init__(self):
		pass

	def filter(self):
		SAVE_DICTIONARY_DIR = config.get("SAVE_DICTIONARY_DIR",None)
		FILTERED_DICTINARIES_CONF = config.get("FILTERED_DICTINARIES_CONF",None)
		if not (SAVE_DICTIONARY_DIR):
			print("config keys - SAVE_DICTIONARY_DIR is not set correctly in the config file: socialconfig.py")
			exit(0)

		if not (FILTERED_DICTINARIES_CONF and len(FILTERED_DICTINARIES_CONF) > 0):
			print("Configuration for filtering dictionaries is not defined in socialconfig.py")
			exit()
		
		SAVE_UNFILTERED_DICTIONARY_DIR = os.path.join(SAVE_DICTIONARY_DIR,"Unfiltered")
		if not os.path.exists(SAVE_UNFILTERED_DICTIONARY_DIR) and not os.path.isdir(SAVE_UNFILTERED_DICTIONARY_DIR):
			raise("Directory {d} does not exist".format(d=SAVE_UNFILTERED_DICTIONARY_DIR))
		
		SAVE_FILTERED_DICTIONARY_DIR = os.path.join(SAVE_DICTIONARY_DIR,"Filtered")
		if not (os.path.exists(SAVE_FILTERED_DICTIONARY_DIR) and os.path.isdir(SAVE_FILTERED_DICTIONARY_DIR)):
			os.makedirs(SAVE_FILTERED_DICTIONARY_DIR)
		

		for bdir, subdirs, files in os.walk(SAVE_UNFILTERED_DICTIONARY_DIR):
			if "negative" in bdir:
				continue
			if "positive" in bdir:
				continue
			if len(files) > 0:
				for file in files:
					if "_dict.dict" in file:
						dictionary = Dictionary.load(os.path.join(bdir,file))
						yelp_category = file.split("_dict.dict")[0]
						if yelp_category == "food":
							FOOD_POSITIVE_SEEDS.extend(FOOD_NEGATIVE_SEEDS)
							keep_tokens = FOOD_POSITIVE_SEEDS
						elif yelp_category == "bars":
							BARS_POSITIVE_SEEDS.extend(BARS_NEGATIVE_SEEDS)
							keep_tokens = BARS_POSITIVE_SEEDS
						elif yelp_category == "leisure":
							LEISURE_POSITIVE_SEEDS.extend(LEISURE_NEGATIVE_SEEDS)
							keep_tokens = LEISURE_POSITIVE_SEEDS
						elif yelp_category == "grooming":
							GROOMING_POSITIVE_SEEDS.extend(GROOMING_NEGATIVE_SEEDS)
							keep_tokens = GROOMING_POSITIVE_SEEDS
						elif yelp_category == "health":
							HEALTH_POSITIVE_SEEDS.extend(HEALTH_NEGATIVE_SEEDS)
							keep_tokens = HEALTH_POSITIVE_SEEDS
						elif yelp_category == "learn":
							LEARN_POSITIVE_SEEDS.extend(LEARN_NEGATIVE_SEEDS)
							keep_tokens = LEARN_POSITIVE_SEEDS
						elif yelp_category == "municipal":
							MUNICIPAL_POSITIVE_SEEDS.extend(MUNICIPAL_NEGATIVE_SEEDS)
							keep_tokens = MUNICIPAL_POSITIVE_SEEDS
						elif yelp_category == "sports":
							SPORTS_POSITIVE_SEEDS.extend(SPORTS_NEGATIVE_SEEDS)
							keep_tokens = SPORTS_POSITIVE_SEEDS
						elif yelp_category == "planning":
							PLANNING_POSITIVE_SEEDS.extend(PLANNING_NEGATIVE_SEEDS)
							keep_tokens = PLANNING_POSITIVE_SEEDS
						elif yelp_category == "services":
							SERVICES_POSITIVE_SEEDS.extend(SERVICES_NEGATIVE_SEEDS)
							keep_tokens = SERVICES_POSITIVE_SEEDS
						elif yelp_category == "shopping":
							SHOPPING_POSITIVE_SEEDS.extend(SHOPPING_NEGATIVE_SEEDS)
							keep_tokens = SHOPPING_POSITIVE_SEEDS
						else:
							keep_tokens = []
						
						keep_token_ids = []
						for token in keep_tokens:
							l = []
							l.append(token)
							res = dictionary.doc2bow(l,return_missing=True)
							found,missing = res
							if token in missing:
								continue
							else:
								keep_token_ids.append(found[0])

						CATEGORY_SPECIFIC_FILTERED_DICT_DIR = os.path.join(SAVE_FILTERED_DICTIONARY_DIR,yelp_category)
						if not (os.path.exists(CATEGORY_SPECIFIC_FILTERED_DICT_DIR) and os.path.isdir(CATEGORY_SPECIFIC_FILTERED_DICT_DIR)):
							os.makedirs(CATEGORY_SPECIFIC_FILTERED_DICT_DIR)

						for conf_name,conf in FILTERED_DICTINARIES_CONF.items():
							keep_n = conf.get("keep_n",None)
							no_below = conf.get("no_below",None)
							if not (keep_n and no_below):
								print("Dictionary config: `{configuration}` does not define values for keep_n and no_below, skipping.".format(configuration=conf_name))
								continue
							else:
								save_in_dir = os.path.join(CATEGORY_SPECIFIC_FILTERED_DICT_DIR,conf_name)
								if not (os.path.exists(save_in_dir) and os.path.isdir(save_in_dir)):
									os.makedirs(save_in_dir)
								save_type_dict_file_name = os.path.join(save_in_dir,"{cat}_filtered_top_{keepn}_tokens_dict.dict".format(cat=yelp_category,keepn=keep_n))
								save_type_text_file_name = os.path.join(save_in_dir,"{cat}_filtered_top_{keepn}_tokens_dict.txt".format(cat=yelp_category,keepn=keep_n))
								save_type_token_docfreqs_file_name = os.path.join(save_in_dir,"{cat}_top_{keepn}_token_doc_freqs.txt".format(cat=yelp_category,keepn=keep_n))
								
								dictionary.filter_extremes(keep_n=keep_n,no_below=no_below,keep_tokens=keep_token_ids)
								dictionary.save(save_type_dict_file_name)
								dictionary.save_as_text(save_type_text_file_name)
								sorted_doc_freqs = sorted(dictionary.dfs.items(),key = lambda x : x[1],reverse=True)
															
								with open(save_type_token_docfreqs_file_name,'w') as socialfile:
									for (token_id,doc_freq) in sorted_doc_freqs:
										socialfile.write(str(dictionary.get(token_id,"Unknown").encode("utf-8")) + " " + str(doc_freq) + "\n")
										print("Saved filtered dictionary ({conf_type}) and token document frequencies for tokens in {category}-reviews in directory: {d}".format(category=yelp_category,d=CATEGORY_SPECIFIC_FILTERED_DICT_DIR,conf_type=conf_name))
								del sorted_doc_freqs	
						del dictionary
					else:
						print("{file} ignored, not of type dict".format(file=file))
						continue

if __name__ == "__main__":
	ob = filter_dictionaries()
	ob.filter()
