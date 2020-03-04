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
from gensim.models import KeyedVectors

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
	
	
	SAVE_WORD_EMBEDDINGS_DIR = config.get("SAVE_WORD_EMBEDDINGS_DIR", None)
	SAVE_DICTIONARY_DIR = config.get("SAVE_DICTIONARY_DIR",None)
	SAVE_WORD2VEC_MODELS_DIR = config.get("SAVE_WORD2VEC_MODELS_DIR",None)
	REVIEWS_CATEGORIES_LIST = config.get("REVIEWS_CATEGORIES_LIST",None)
	WORD2VEC_MODELS_CONF = config.get("WORD2VEC_MODELS_CONF",None)



	if not (REVIEWS_CATEGORIES_LIST and len(REVIEWS_CATEGORIES_LIST) > 0):
		print("Categories List is not defined in socialconfig.py, cannot determine the paths to category-specific word2vec stored models")
		exit()

	if not (SAVE_WORD_EMBEDDINGS_DIR and SAVE_DICTIONARY_DIR and SAVE_WORD2VEC_MODELS_DIR):
		print("config keys (SAVE_WORD_EMBEDDINGS_DIR and SAVE_DICTIONARY_DIR and SAVE_WORD2VEC_MODELS_DIR) are not set correctly in the config file: socialconfig.py")
		exit(0)

	FILTERED_DICTIONARY_DIR = os.path.join(SAVE_DICTIONARY_DIR,"Filtered")
	if not (os.path.exists(FILTERED_DICTIONARY_DIR) and os.path.isdir(FILTERED_DICTIONARY_DIR)):
		raise Exception("Filtered dictionaries do not exist, can not create embeddings for top vocab words")

	if not (os.path.exists(SAVE_WORD2VEC_MODELS_DIR) and os.path.isdir(SAVE_WORD2VEC_MODELS_DIR)):
		raise Exception("Word2Vec Models directory does not exist, can not load keyed vectors for creating embeddings")


	for category in REVIEWS_CATEGORIES_LIST:
		CATEGORY_SPECIFIC_WORD2VEC_MODELS_DIR = os.path.join(SAVE_WORD2VEC_MODELS_DIR,category)
		print("Looking for {cat}-specific word2vec keyed vectors in {d}".format(cat=category,d=CATEGORY_SPECIFIC_WORD2VEC_MODELS_DIR))

		
		for top_vocab_word_count in WORD2VEC_MODELS_CONF:
			print("Searching for keyed vectors for top{top} words".format(top=top_vocab_word_count))			
			search_in_dir = os.path.join(CATEGORY_SPECIFIC_WORD2VEC_MODELS_DIR,top_vocab_word_count)
			if not (os.path.exists(search_in_dir) and os.path.isdir(search_in_dir)):
				print("keyed vectors do not exist for top{top} words".format(top=top_vocab_word_count))
				continue
			for conf_name,conf in WORD2VEC_MODELS_CONF[top_vocab_word_count].items():
				conf_specific_dir = os.path.join(search_in_dir,conf_name)
				if not (os.path.exists(conf_specific_dir) and os.path.isdir(conf_specific_dir)):
					print("keyed vectors do not exist for {conf_name} model type".format(conf_name=conf_name))
					continue
				for entity in os.listdir(conf_specific_dir):
					if not os.path.isdir(entity):						
						if "word2vec_keyed_vectors_yelp_" in entity and entity[-4:] == ".txt":
							print("Loading keyed vectors of conf:{c}".format(c=conf_name))				
							word_vectors = None
							try:
								word_vectors = KeyedVectors.load(os.path.join(conf_specific_dir,entity))
							except:
								raise Exception("Can not load keyed vectors: {error}".format(error=traceback.format_exc()))

							if word_vectors:
								save_in_dir = conf_specific_dir.replace(SAVE_WORD2VEC_MODELS_DIR,SAVE_WORD_EMBEDDINGS_DIR)				
								if not (os.path.exists(save_in_dir) and os.path.isdir(save_in_dir)):
									os.makedirs(save_in_dir)				

								topn_wordcount = top_vocab_word_count[9:]
								filtered_words_file = os.path.join(FILTERED_DICTIONARY_DIR,category,top_vocab_word_count,"{cat}_top_{topn}_token_doc_freqs.txt".format(cat=category,topn=topn_wordcount))
								filtered_words = set()
								try:
									print("Loading doc-freqencies for top {top} filtered tokens".format(top=topn_wordcount))
									with open(filtered_words_file,'r') as rfile:
										print("Reading file:{file}".format(file=filtered_words_file))
										for line in rfile:
											split = line.split(" ")
											if len(split) > 1:
												filtered_words.add(split[0])
								except:
									print("Error Loading token doc-frequencies from file:{filtered_words_file}. Can not filter keyed vectors".format(filtered_words_file=filtered_words_file))
									raise

								save_embeddings_file_path = os.path.join(save_in_dir,entity.replace("word2vec_keyed_vectors_yelp_","word2vec_GIGA_Embeddings_yelp_"))

								try:
									print("Creating Embeddings..")
									with open(save_embeddings_file_path,'w') as efile:
										# i = 0
										print("Created file:{file}".format(file=save_embeddings_file_path))
										for word in word_vectors.vocab:
											lemword = wd(word).lemmatize("a")
											try:
												if lemword not in filtered_words:
													continue
												rp = word_vectors.get_vector(lemword)
												write_string = lemword + ' ' + ' '.join(map(str, rp))
												efile.write(write_string + "\n")
											except:
												print("{lemword} is not in word2vec vocab".format(lemword=lemword))
												pass
									print("Embeddings CREATED...")
								except:
									print("Error occurred while creating Embeddings")
									raise
								finally:
									del word_vectors
									del filtered_words
									del save_embeddings_file_path
									del filtered_words_file
									del topn_wordcount
	
