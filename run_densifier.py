# from socialsent import lexicons
import os
import sys

from socialconfig import config
from socialconfig import FOOD_POSITIVE_SEEDS,FOOD_NEGATIVE_SEEDS,BARS_POSITIVE_SEEDS,BARS_NEGATIVE_SEEDS,LEISURE_POSITIVE_SEEDS,LEISURE_NEGATIVE_SEEDS,GROOMING_POSITIVE_SEEDS,GROOMING_NEGATIVE_SEEDS,HEALTH_POSITIVE_SEEDS,HEALTH_NEGATIVE_SEEDS,LEARN_POSITIVE_SEEDS,LEARN_NEGATIVE_SEEDS,SHOPPING_POSITIVE_SEEDS,SHOPPING_NEGATIVE_SEEDS,PLANNING_POSITIVE_SEEDS,PLANNING_NEGATIVE_SEEDS,SERVICES_POSITIVE_SEEDS,SERVICES_NEGATIVE_SEEDS,SPORTS_POSITIVE_SEEDS,SPORTS_NEGATIVE_SEEDS,MUNICIPAL_POSITIVE_SEEDS,MUNICIPAL_NEGATIVE_SEEDS

from socialsent.polarity_induction_methods import random_walk
from socialsent.polarity_induction_methods import densify
from socialsent.polarity_induction_methods import pmi
from socialsent.polarity_induction_methods import label_propagate_probabilistic
from socialsent.polarity_induction_methods import graph_propagate
from socialsent.polarity_induction_methods import dist

from socialsent.evaluate_methods import binary_metrics
from socialsent.representations.representation_factory import create_representation
from textblob import TextBlob as tb
from textblob import Word as wd

import operator
import re
import traceback

from gensim.models import Word2Vec
from gensim.models import KeyedVectors

if __name__ == "__main__":
	SAVE_WORD_EMBEDDINGS_DIR = config.get("SAVE_WORD_EMBEDDINGS_DIR",None)
	SAVE_DICTIONARY_DIR = config.get("SAVE_DICTIONARY_DIR",None)
	SAVE_POLARITIES_DIR = config.get("SAVE_POLARITIES_DIR",None)

	if not (SAVE_WORD_EMBEDDINGS_DIR and SAVE_DICTIONARY_DIR and SAVE_POLARITIES_DIR):
		print("Keys (SAVE_WORD_EMBEDDINGS_DIR|SAVE_DICTIONARY_DIR|SAVE_POLARITIES_DIR) not set in the config file socialconfig.py")
		exit()

	SAVE_FILTERED_DICTIONARY_DIR = os.path.join(SAVE_DICTIONARY_DIR,"Filtered")

	if not (os.path.exists(SAVE_WORD_EMBEDDINGS_DIR) and os.path.isdir(SAVE_WORD_EMBEDDINGS_DIR)):
		print("Cannot load Word Embeddings: Directory:{d} does not exist".format(d=SAVE_WORD_EMBEDDINGS_DIR))
		exit()

	pos_neg_words_dict_per_category = {
		"bars":{
			"pos":BARS_POSITIVE_SEEDS,
			"neg":BARS_NEGATIVE_SEEDS
		},
		"food":{
			"pos":FOOD_POSITIVE_SEEDS,
			"neg":FOOD_NEGATIVE_SEEDS
		},
		"grooming":{
			"pos":GROOMING_POSITIVE_SEEDS,
			"neg":GROOMING_NEGATIVE_SEEDS
		},
		"health":{
			"pos":HEALTH_POSITIVE_SEEDS,
			"neg":HEALTH_NEGATIVE_SEEDS
		},
		"learn":{
			"pos":LEARN_POSITIVE_SEEDS,
			"neg":LEARN_NEGATIVE_SEEDS
		},
		"leisure":{
			"pos":LEISURE_POSITIVE_SEEDS,
			"neg":LEISURE_NEGATIVE_SEEDS
		},
		"municipal":{
			"pos":MUNICIPAL_POSITIVE_SEEDS,
			"neg":MUNICIPAL_NEGATIVE_SEEDS
		},
		"planning":{
			"pos":PLANNING_POSITIVE_SEEDS,
			"neg":PLANNING_NEGATIVE_SEEDS
		},
		"services":{
			"pos":SERVICES_POSITIVE_SEEDS,
			"neg":SERVICES_NEGATIVE_SEEDS
		},
		"shopping":{
			"pos":SHOPPING_POSITIVE_SEEDS,
			"neg":SHOPPING_NEGATIVE_SEEDS
		},
		"sports":{
			"pos":SPORTS_POSITIVE_SEEDS,
			"neg":SPORTS_NEGATIVE_SEEDS
		},
	}

	giga_embeddings_file_path = None
	embedding_num_words = None
	for file_or_dir in os.listdir(SAVE_WORD_EMBEDDINGS_DIR):
		abs_path = os.path.join(SAVE_WORD_EMBEDDINGS_DIR,file_or_dir)
		if os.path.isdir(abs_path):
			yelp_category = file_or_dir
			pos_seeds_no_lemma = pos_neg_words_dict_per_category.get(yelp_category,{}).get("pos",None)
			neg_seeds_no_lemma = pos_neg_words_dict_per_category.get(yelp_category,{}).get("neg",None)
			if not (pos_seeds_no_lemma or neg_seeds_no_lemma):
				print("Seeds not defined in socialconfig.py for {c} category, ignoring".format(c=yelp_category))
				continue
			pos_seeds = []
			neg_seeds = []

			for seed in pos_seeds_no_lemma:
				pos_seeds.append(wd(seed).lemmatize("a"))

			for seed in neg_seeds_no_lemma:
				neg_seeds.append(wd(seed).lemmatize("a"))

			for bdir,subdirs,files in os.walk(abs_path):
				if len(files) > 0:
					# any file discovered here should be an embeddings file
					for file in files:
						if file[0] != "." and "word2vec_GIGA_Embeddings_yelp" in file and file[-4:] == ".txt":
							# we found an embedding file
							embedding_abs_file_path = os.path.join(bdir,file)
							print("Using embeddings in {f}".format(f=embedding_abs_file_path))

							vocab_n = "UNKNOWN"

							# find dir where vocab fle resides (estimate from file path of embedding)
							vocab_words = set()
							find = re.findall("(vocabTop[0-9]*)",embedding_abs_file_path)
							if find:
								top_n_words_in_embedding = find[0].replace("vocabTop","vocab_top")
								vocab_n = top_n_words_in_embedding
								vocab_dir = os.path.join(SAVE_DICTIONARY_DIR,"Filtered",yelp_category,top_n_words_in_embedding)
								if os.path.exists(vocab_dir) and os.path.isdir(vocab_dir):
									for entity in os.listdir(vocab_dir):
										if not os.path.isdir(os.path.join(vocab_dir,entity)) and entity[0] != "." and "_doc_freqs.txt" in entity:
											vocab_file_path = os.path.join(vocab_dir,entity)
											print("Using Vocab file {f} for the embeddings".format(f=vocab_file_path))
											try:
												with open(vocab_file_path,'r') as vfile:
													for line in vfile:
														split = line.split(" ")
														if len(split) > 1:
															word = None
															try:
																word = split[0].decode("utf-8")
																if word:
																	word = wd(word).lemmatize("a")
																	if len(word) > 2:
																		vocab_words.add(word)
															except:
																print("Word {word} cannot be added to vocab_words. Error:{e}".format(word=word,e=traceback.format_exc()))
													break
											except:
												print("Can not read vocab words from vocab file:{f}".format(f=vocab_file_path))
												print(traceback.format_exc())
												pass
							if not vocab_words:
								print("Could not get vocab words, Moving on to other embeddings..")
								continue
							else:
								embeddings = None
								polarities = None
								sorted_x = None

								try:
									print("Loading embeddings...")
									embeddings = create_representation("GIGA", embedding_abs_file_path,
									set(vocab_words).union(pos_seeds).union(neg_seeds))

									eval_words = [word for word in embeddings.iw
											if not word in pos_seeds 
											and not word in neg_seeds]

									induction_method = "densify"
									save_dir = os.path.join(SAVE_POLARITIES_DIR,yelp_category,vocab_n,induction_method)
									if not (os.path.exists(save_dir) and os.path.isdir(save_dir)):
										os.makedirs(save_dir)

									print("Computing polarities...")
									# Substitute the method name below that will be used to induce polarities 
									polarities = densify(embeddings, pos_seeds, neg_seeds, beta=0.99, nn=10,
											sym=True, arccos=True)
									sorted_x = sorted(polarities.items(), key=operator.itemgetter(1),  reverse=True)
									word2vec_training_params_part = re.search(r"((win([0-9]){1}){1}_(dim([0-9]){3}){1}){1}",file).group()
									if isinstance(word2vec_training_params_part,str):
										save_file_name = "{category}_{vocab}_{method}_{dim_win_part}_polarities.txt".format(category=yelp_category,method=induction_method,dim_win_part=word2vec_training_params_part,vocab=vocab_n)
										with open(os.path.join(save_dir,save_file_name),'w') as polfile:
											for (word,pol) in sorted_x:
												polfile.write("{w} {p}".format(w=word,p=str(pol)) + "\n")
										print("Computed polarities using the {mthd} method and saved in {f}".format(mthd=induction_method,f=os.path.join(save_dir,save_file_name)))
									else:
										print("Cannot estimate window,dimension part that was used for word2vec training from file name: {f}".format(f=file))
								except:
									print("Error inducing polarity for {cat} using {mthd} method".format(cat=yelp_category,mthd=induction_method))
									print(traceback.format_exc())
									pass
								finally:
									del embeddings
									del polarities
									del sorted_x
									if vocab_words:
										del vocab_words

	# dist
	polarities = dist(embeddings, pos_seeds, neg_seeds, beta=0.99, nn=10,
			sym=True, arccos=True)
	sorted_x = sorted(polarities.items(), key=operator.itemgetter(1),  reverse=True)
	with open(os.path.join(save_dir,"10000_dist_polarities.txt"),'w') as polfile:
		for (word,pol) in sorted_x:
			polfile.write("{w} {p}".format(w=word,p=str(pol)) + "\n")


