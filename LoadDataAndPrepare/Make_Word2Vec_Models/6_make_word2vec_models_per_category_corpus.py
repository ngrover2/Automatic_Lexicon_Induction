from gensim.models import Word2Vec
import ujson
import os
import sys
import traceback
import ujson
from pprint import pprint
from textblob import TextBlob as tb
from textblob import Word as wd
import shutil
from collections import defaultdict

from socialconfig import config

class get_iterator(object):

	def __init__(self, file_name):
		self.file_name = file_name

	def __iter__(self):
		with open(self.file_name,'r') as open_file:
			for line in open_file:
				yield(line)

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

if __name__ == "__main__":
	
	SAVE_BAG_OF_WORDS_DIR = config.get("SAVE_BAG_OF_WORDS_DIR", None)
	SAVE_WORD2VEC_MODELS_DIR = config.get("SAVE_WORD2VEC_MODELS_DIR", None)
	PROCESS_N_REVIEWS_ONLY_PER_CATEGORY = int(config.get("PROCESS_N_REVIEWS_ONLY_PER_CATEGORY", 25000))
	SAVE_N_BAG_OF_WORDS_DOCS_PER_FILE = int(config.get("SAVE_N_BAG_OF_WORDS_DOCS_PER_FILE",25000))
	FILTERED_DICTINARIES_CONF = config.get("FILTERED_DICTINARIES_CONF",{})
	FILTER_DICTIONARY_TOP_N_WORDS_PER_CATEGORY = int(config.get("FILTER_DICTIONARY_TOP_N_WORDS_PER_CATEGORY",10000))
	SAVE_DICTIONARY_DIR = config.get("SAVE_DICTIONARY_DIR",None)
	WORD2VEC_MODELS_CONF = config.get("WORD2VEC_MODELS_CONF",None)

	if not (WORD2VEC_MODELS_CONF and isinstance(WORD2VEC_MODELS_CONF,dict) and len(WORD2VEC_MODELS_CONF)):
		print("No Model Configurations specified in the socialconfig.py file for training the Word2vec models")
		exit()

	if not (SAVE_BAG_OF_WORDS_DIR and SAVE_WORD2VEC_MODELS_DIR and SAVE_DICTIONARY_DIR):
		print("config keys (SAVE_BAG_OF_WORDS_DIR and SAVE_WORD_EMBEDDINGS_DIR and SAVE_DICTIONARY_DIR) are not set correctly in the config file: socialconfig.py")
		exit(0)

	process_files_till_index = int(PROCESS_N_REVIEWS_ONLY_PER_CATEGORY/SAVE_N_BAG_OF_WORDS_DOCS_PER_FILE)
	try:
		for file_or_dir in os.listdir(SAVE_BAG_OF_WORDS_DIR):
			abs_path = os.path.join(SAVE_BAG_OF_WORDS_DIR,file_or_dir)
			if os.path.isdir(abs_path) and "." not in file_or_dir:
				yelp_category = file_or_dir
				print("Reading the files for category:{c} in {d}..".format(d=abs_path,c=yelp_category))
				rev_count = 0
				review_docs = []
				for entry in os.listdir(abs_path):
					if not os.path.isdir(os.path.join(abs_path,entry)):
						if ".DS_Store" in entry and entry[0] != ".":
							print("Ignoring hidden file: {hid}".format(hid=entry))
							continue
						file_index = int(entry.split(".")[0].split("_")[-1]) # That'sho it was formatted
						if file_index <= process_files_till_index:
							reviews = get_iterator(os.path.join(abs_path,entry))
							for rev in reviews:
								# just to check if the line is not empty or junk
								if len(rev) > 3:
									try:
										rev_string = ujson.loads(rev)
									except ValueError:
										print("Parsing Error,string not valid json: " + rev)
										continue
									except:
										print("Parsing Error, string: " + rev)
										continue
									adjectives_list = [wd(w).lemmatize("a") for w in [reviews.strip_special_chars(word) for word in rev_string.split(" ")] if len(w) > 2]
									if adjectives_list:
										review_docs.append(adjectives_list)
									rev_count += 1
									if rev_count > PROCESS_N_REVIEWS_ONLY_PER_CATEGORY:
										break
						else:
							# We don't break here as os.listdir does not guarantee to walk the files in order
							continue
				print("Read {count} documents for {c} category".format(count=str(rev_count),c=yelp_category))
				# Now we have all the review docs for the specific category
				if review_docs:
					CATEGORY_SPECIFIC_WORD2VEC_MODELS_DIR = os.path.join(SAVE_WORD2VEC_MODELS_DIR,yelp_category)
					if not (os.path.exists(CATEGORY_SPECIFIC_WORD2VEC_MODELS_DIR) and os.path.isdir(CATEGORY_SPECIFIC_WORD2VEC_MODELS_DIR)):
						os.makedirs(CATEGORY_SPECIFIC_WORD2VEC_MODELS_DIR)

					for top_vocab_word_count in WORD2VEC_MODELS_CONF:
						# Add top_vocab_word_count to dir path, to save models for diff vocab counts in separate subdirs
						save_in_dir = os.path.join(CATEGORY_SPECIFIC_WORD2VEC_MODELS_DIR,top_vocab_word_count)
						if not (os.path.exists(save_in_dir) and os.path.isdir(save_in_dir)):
							os.makedirs(save_in_dir)
						for conf_name,conf in WORD2VEC_MODELS_CONF[top_vocab_word_count].items():
							print("Creating word2vec model for configuration: {c} as per directive in socialconfig.py."
								.format(c=conf_name))
							# Train word2vec with review_docs
							window = conf.get("window",None)
							size = conf.get("size",None)
							workers = 4
							if not (window and size):
								print("Model config: `{configuration}` does not define values for window and size, skipping.".format(configuration=conf_name))
							

							print("Training model with size={s}, window={w} on {cores} cores".format(s=str(size),w=str(window),cores=str(workers)))
							try:
								model = Word2Vec(review_docs, size=size, window=window, min_count=1, workers=4)
							except:
								raise Exception("Error occurred during Word2vec Training:{error}".format(error=traceback.format_exc()))

							# Add config type to dir path, to save models of diff conf type in separate subdirs
							save_in_subdir = os.path.join(save_in_dir,conf_name)
							if not (os.path.exists(save_in_subdir) and os.path.isdir(save_in_subdir)):
								os.makedirs(save_in_subdir)

							save_model_file_path = os.path.join(save_in_subdir,"word2vec_model_yelp_{num}reviews_win{win}_dim{sz}.model".format(win=window,sz=size,num=rev_count))
							model.save(save_model_file_path)

							word_vectors = model.wv
							save_keyedvectors_file_path = os.path.join(save_in_subdir,"word2vec_keyed_vectors_yelp_{num}reviews_win{win}_dim{sz}.txt".format(win=window,sz=size,num=rev_count))				
							word_vectors.save(save_keyedvectors_file_path)
							
							print("Word2Vec models(and its keyvectors) saved for category:{c}".format(c=yelp_category))

							print("Deleting model to save memory..")
							del model
							del word_vectors
							print("Deleted.")
					del review_docs
					del rev_count
							
	except:
		raise
