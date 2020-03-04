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

class get_reviews_iterable(object):


	def __init__(self, rfname):
		self.read_file = rfname

	def __iter__(self):
		try:
			print("Opening file:{file}".format(file=self.read_file))
			with open(self.read_file,'r') as file:
				for line in file:
					yield line
		except:
			raise
			print("Error reading {f}:".format(f=self.read_file))
			# print(traceback.format_exc())


class make_dictionaries(object):
	"""docstring for ClassName"""
	def __init__(self):
		pass

	def create_dictionary(self):
		YELP_DATASET_DIR = config.get("YELP_DATASET_DIR",None)
		SAVE_REVIEWS_BY_CATEGORY_DIRECTORY = config.get("SAVE_REVIEWS_BY_CATEGORY_DIRECTORY",None)
		SAVE_DICTIONARY_DIR = config.get("SAVE_DICTIONARY_DIR",None)
		SAVE_BAG_OF_WORDS_DIR = config.get("SAVE_BAG_OF_WORDS_DIR",None)
		SAVE_N_BAG_OF_WORDS_DOCS_PER_FILE = int(config.get("SAVE_N_BAG_OF_WORDS_DOCS_PER_FILE",25000))

		if not (YELP_DATASET_DIR and SAVE_REVIEWS_BY_CATEGORY_DIRECTORY and SAVE_DICTIONARY_DIR and SAVE_BAG_OF_WORDS_DIR and SAVE_DICTIONARY_DIR):
			print("config keys are not set correctly in the config file: socialconfig.py")
			exit(0)

		SAVE_UNFILTERED_DICTIONARY_DIR = os.path.join(SAVE_DICTIONARY_DIR,"Unfiltered")

		if not os.path.exists(SAVE_REVIEWS_BY_CATEGORY_DIRECTORY) and not os.path.isdir(SAVE_REVIEWS_BY_CATEGORY_DIRECTORY):
			raise("Directory {d} does not exist".format(d=SAVE_REVIEWS_BY_CATEGORY_DIRECTORY))

		if not (os.path.exists(SAVE_BAG_OF_WORDS_DIR) and os.path.isdir(SAVE_BAG_OF_WORDS_DIR)):
			os.makedirs(SAVE_BAG_OF_WORDS_DIR)

		if not (os.path.exists(SAVE_UNFILTERED_DICTIONARY_DIR) and os.path.isdir(SAVE_UNFILTERED_DICTIONARY_DIR)):
			os.makedirs(SAVE_UNFILTERED_DICTIONARY_DIR)

			
		for pardir, sub_dirs, files in os.walk(SAVE_REVIEWS_BY_CATEGORY_DIRECTORY):
			
			if len(files) > 0:
				error_count = 0
				review_docs = []
				negative_docs = []
				positive_docs = []
				
				doc_count = 0
				docs_per_file = SAVE_N_BAG_OF_WORDS_DOCS_PER_FILE
				file_num = str((doc_count/docs_per_file) + 1)
				for file in files:
					if "yelp_reviews_" in file and "category" in pardir:
						reviews = get_reviews_iterable(os.path.join(pardir,file))
						yelp_category = pardir.split('/')[-1]						

						CATEGORY_SPECIFIC_BAG_OF_WORDS_DIR = os.path.join(SAVE_BAG_OF_WORDS_DIR,yelp_category)
						if not (os.path.exists(CATEGORY_SPECIFIC_BAG_OF_WORDS_DIR) and os.path.isdir(CATEGORY_SPECIFIC_BAG_OF_WORDS_DIR)):
							os.makedirs(CATEGORY_SPECIFIC_BAG_OF_WORDS_DIR)

						fname = os.path.join(SAVE_BAG_OF_WORDS_DIR,yelp_category,"{cat}_file_{file_num}.txt".format(cat=yelp_category,file_num=file_num))
						bow_file = open(fname,'w')
						print("Writing docs (in bag of words form) for {cat} to directory: {d}".format(cat=yelp_category,d=os.path.join(SAVE_BAG_OF_WORDS_DIR,yelp_category)))
						for review in reviews:
							try:
								review_dict = ujson.loads(review)
							except:
								error_count += 1
								pass
							adjs = review_dict.get("adjectives",None)
							rating = int(review_dict.get("rating",-1))
							if adjs:
								doc_count += 1
								bow_file.write(ujson.dumps(adjs.encode("utf-8")) + "\n")
								review_docs.append(adjs.strip().split())
								if (doc_count%docs_per_file) == 0:
									if bow_file:
										bow_file.close()
									file_num = str((doc_count/docs_per_file) + 1)
									fname = os.path.join(SAVE_BAG_OF_WORDS_DIR,yelp_category,"{cat}_file_{file_num}.txt".format(cat=yelp_category,file_num=file_num))
									bow_file = open(fname,'w')
							if rating:
								if rating > 3:
									positive_docs.append(adjs.strip().split())
								elif rating < 3:
									negative_docs.append(adjs.strip().split())
								else:
									pass
				print("Wrote {total} docs in {cat} category".format(total=str(doc_count),cat=yelp_category))
				
				dictionary = Dictionary(review_docs)

				CATEGORY_SPECIFIC_DICT_DIR = os.path.join(SAVE_UNFILTERED_DICTIONARY_DIR,yelp_category)
				POSITIVE_SUB_DIR = os.path.join(CATEGORY_SPECIFIC_DICT_DIR,"positive")
				NEGATIVE_SUB_DIR = os.path.join(CATEGORY_SPECIFIC_DICT_DIR,"negative")
				if not (os.path.exists(CATEGORY_SPECIFIC_DICT_DIR) and os.path.isdir(CATEGORY_SPECIFIC_DICT_DIR)):
					os.makedirs(CATEGORY_SPECIFIC_DICT_DIR)
					os.makedirs(POSITIVE_SUB_DIR)
					os.makedirs(NEGATIVE_SUB_DIR)

				dictionary.save(os.path.join(CATEGORY_SPECIFIC_DICT_DIR,"{yelp_category}_dict.dict".format(yelp_category=yelp_category)))
				dictionary.save_as_text(os.path.join(CATEGORY_SPECIFIC_DICT_DIR,"{yelp_category}_dict.txt".format(yelp_category=yelp_category)))
				sorted_doc_freqs = sorted(dictionary.dfs.items(),key = lambda x : x[1],reverse=True)
				
				# print("Will save file in:\n " + os.path.join(CATEGORY_SPECIFIC_DICT_DIR,"{yelp_category}_dict.txt".format(yelp_category=yelp_category)))
				with open(os.path.join(CATEGORY_SPECIFIC_DICT_DIR,"{yelp_category}_words_doc_frequencies.txt".format(yelp_category=yelp_category)),'w') as df_file:
					for (token_id,doc_freq) in sorted_doc_freqs:
						df_file.write(str(dictionary.get(token_id,"Unknown").encode('utf-8')) + " " + str(doc_freq) + "\n")

				del dictionary
				del review_docs
				del sorted_doc_freqs
				
				pos_dictionary = Dictionary(positive_docs)
				del positive_docs

				neg_dictionary = Dictionary(negative_docs)
				del negative_docs

				pos_dictionary.save(os.path.join(POSITIVE_SUB_DIR,"{yelp_category}_pos_dict.dict".format(yelp_category=yelp_category)))
				pos_dictionary.save_as_text(os.path.join(POSITIVE_SUB_DIR,"{yelp_category}_pos_dict.txt".format(yelp_category=yelp_category)))
				
				sorted_pos_doc_freqs = sorted(pos_dictionary.dfs.items(),key = lambda x : x[1],reverse=True)
				with open(os.path.join(POSITIVE_SUB_DIR,"{yelp_category}_pos_words_doc_frequencies.txt".format(yelp_category=yelp_category)),'w') as df_file:
					for (token_id,doc_freq) in sorted_pos_doc_freqs:
						df_file.write(str(pos_dictionary.get(token_id,"Unknown").encode('utf-8')) + " " + str(doc_freq) + "\n")

				del pos_dictionary
				del sorted_pos_doc_freqs

				neg_dictionary.save(os.path.join(NEGATIVE_SUB_DIR,"{yelp_category}_neg_dict.dict".format(yelp_category=yelp_category)))
				neg_dictionary.save_as_text(os.path.join(NEGATIVE_SUB_DIR,"{yelp_category}_neg_dict.txt".format(yelp_category=yelp_category)))
				sorted_neg_doc_freqs = sorted(neg_dictionary.dfs.items(),key = lambda x : x[1],reverse=True)
				with open(os.path.join(NEGATIVE_SUB_DIR,"{yelp_category}_neg_words_doc_frequencies.txt".format(yelp_category=yelp_category)),'w') as df_file:
					for (token_id,doc_freq) in sorted_neg_doc_freqs:
						df_file.write(str(neg_dictionary.get(token_id,"Unknown").encode('utf-8')) + " " + str(doc_freq) + "\n")

				del neg_dictionary
				del sorted_neg_doc_freqs

				print("{count} {cat} reviews were discarded because of parsing errors".format(count=error_count,cat=yelp_category))
				print("Created dictionary for {cat} tokens".format(cat=yelp_category))

if __name__ == "__main__":
	try:
		mk = make_dictionaries()
		mk.create_dictionary()
	except:
		raise

	
