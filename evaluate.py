import os
import sys

import pandas as pd
import numpy as np
import ujson
from sklearn.preprocessing import MinMaxScaler,StandardScaler
import re

import sys
from textblob import TextBlob as tb

from collections import defaultdict
from socialconfig import config

from textblob import TextBlob as tb
from textblob import Word as wd
scaler = MinMaxScaler(feature_range=(-1, 1))


SAVE_POLARITIES_DIR = config.get("SAVE_POLARITIES_DIR",None)
SAVE_REVIEWS_DIRECTORY = config.get("SAVE_REVIEWS_DIRECTORY",None)
EVALUATE_SENTIMENTS_DIR = config.get("EVALUATE_SENTIMENTS_DIR",None)
if not SAVE_POLARITIES_DIR:
	print("SAVE_POLARITIES_DIR is not defined in socialconfig.py, can not load embeddings")
	exit()

if not SAVE_REVIEWS_DIRECTORY:
	print("SAVE_REVIEWS_DIRECTORY is not defined in socialconfig.py, can not load documents to evaluate polarities")
	exit()

for category_entity in os.listdir(SAVE_POLARITIES_DIR):
	embedding_category_abs_path = os.path.join(SAVE_POLARITIES_DIR,category_entity)
	if category_entity[0] != "." and os.path.isdir(embedding_category_abs_path):
		yelp_category = category_entity
		print("yelp_category: {v}".format(v=yelp_category))
		for vocab_type_entity in os.listdir(embedding_category_abs_path):
			vocab_type_abs_path = os.path.join(embedding_category_abs_path,vocab_type_entity)
			if vocab_type_entity[0] != "." and os.path.isdir(vocab_type_abs_path):
				vocab_type = vocab_type_entity
				print("vocab_type: {v}".format(v=vocab_type))
				for induction_method_entity in os.listdir(vocab_type_abs_path):
					induction_method_abs_path = os.path.join(vocab_type_abs_path,induction_method_entity)
					if induction_method_entity[0] != "." and os.path.isdir(induction_method_abs_path):
						induction_method = induction_method_entity
						print("induction_method: {v}".format(v=induction_method_entity))
						# print(str(len(os.listdir(induction_method_abs_path))) + " entities below")
						for parameterised_polarity_file_entity in os.listdir(induction_method_abs_path):
							parameterised_polarity_file_abs_path = os.path.join(induction_method_abs_path,parameterised_polarity_file_entity)
							pamameterised_polarity_file = parameterised_polarity_file_entity
							print("pamameterised_polarity_file: {v}".format(v=pamameterised_polarity_file))
							# continue

							temp_dict = defaultdict(float)
							with open(parameterised_polarity_file_abs_path,'r') as pol_file:
								for line in pol_file:
									if line and len(line) > 1:
										split = line.split()
										polarity = split[1]
										token = split[0]
										temp_dict[token] = polarity

							print("Polarities loaded from file: {f}".format(f=parameterised_polarity_file_abs_path))
							print(str(len(temp_dict)) + " tokens found in file")

							df = pd.DataFrame(temp_dict.items())
							del temp_dict
							df['token'] = df[0]
							df['polarity'] = df[1]
							df = df.drop([0,1],axis=1)
							a = np.array(df['polarity'])
							a = a.reshape(-1,1)
							df['scl_polarity'] = scaler.fit_transform(a)
							print("Polarities scaled to the range [-1 and 1]")

							temp_file_scaled_polarities = "./temp_scaled_" + pamameterised_polarity_file
							with open(temp_file_scaled_polarities,"w") as scl_file:
								for row in df.iterrows():
									scl_file.write(row[1].to_json() + "\n")

							scaled_pol_dict = defaultdict(float)
							with open(temp_file_scaled_polarities,"r") as scl_file:
								for row in scl_file:
									ujdict = ujson.loads(row)
									tok = ujdict.get("token",None)
									pol = ujdict.get("scl_polarity",None)
									if not (tok and pol):
										continue
									else:
										scaled_pol_dict[tok] = pol

							print(str(len(scaled_pol_dict)) + " elements in scaled pol dictionary")
							print("Deleting temp_file: {t}".format(t=temp_file_scaled_polarities))
							if scl_file:
								scl_file.close()
							os.remove(temp_file_scaled_polarities)

							CAT_SPECIFIC_REVIEWS_DIR = os.path.join(SAVE_REVIEWS_DIRECTORY,"category",yelp_category)

							parameters_part = re.search(r"((win([0-9]){1}){1}_(dim([0-9]){3}){1}){1}",pamameterised_polarity_file).group()
							save_evaluation_in_dir = os.path.join(EVALUATE_SENTIMENTS_DIR,yelp_category,vocab_type,induction_method,parameters_part)
							if not (os.path.exists(save_evaluation_in_dir) and os.path.isdir(save_evaluation_in_dir)):
								os.makedirs(save_evaluation_in_dir)

							save_evaluation_in_file = pamameterised_polarity_file.replace(".txt","_evaluation.txt")

							cannot_classify_count = 0
							name,ext = os.path.splitext(save_evaluation_in_file)
							first_file_name = name + "_1"
							eval_file = open(os.path.join(save_evaluation_in_dir,"{name}{ext}".format(name=first_file_name,ext=ext)),'w')
							
							print("Reading docs and classifying sentiment..")
							eval_doc_count = 0
							for file in os.listdir(CAT_SPECIFIC_REVIEWS_DIR):
								if not(file[0] == "." and os.path.isdir(os.path.join(CAT_SPECIFIC_REVIEWS_DIR,file))):
									with open(os.path.join(CAT_SPECIFIC_REVIEWS_DIR,file),'r') as rev_file:
										for line in rev_file:
											try:
												ujdict = ujson.loads(line)
											except:
												continue
											rat = float(ujdict.get("rating",None))
											text = ujdict.get("review_text",None)
											adjs = ujdict.get("adjectives",None)
											rev_id = ujdict.get("review_id",None)
											classified_right = None
											if not (rat and adjs and rev_id and text):
												continue
											else:
												induced_polarity = None
												for word in adjs.split():
													word = wd(word).lemmatize("a")
													if len(word) > 1:
														scpol = scaled_pol_dict.get(word,None)
														# print(scpol)
														# exit()
														if not scpol:
															continue
														if induced_polarity is None:
															induced_polarity = float(scpol)
														else:
															induced_polarity += float(scpol)
											if induced_polarity is not None and isinstance(induced_polarity,float):
												if rat <=3 and induced_polarity > 0:
													classified_right = False
												elif rat >3 and induced_polarity > 0:
													classified_right = True
												elif rat >3 and induced_polarity < 0:
													classified_right = False
												elif rat <=3 and induced_polarity < 0:
													classified_right = True
												else:
													pass
											else:
												cannot_classify_count += 1
											if classified_right is not None:
												wdict = {}
												wdict['review_id'] = rev_id
												wdict['adjectives'] = adjs
												wdict['rating'] = rat
												wdict['adj_count'] = len(adjs.split())
												wdict['word_count'] = len(text.split())
												wdict['induced_polarity'] = induced_polarity
												wdict['classified_right'] = str(classified_right)
												write = ujson.dumps(wdict)
												eval_file.write(write + "\n")
												eval_doc_count += 1
											if eval_doc_count%25000 == 0:
												if eval_file:
													eval_file.close()
												eval_file = open(os.path.join(save_evaluation_in_dir,"{subsq_file_name}{ext}".
													format(subsq_file_name=name + "_{idx}".format(idx=str((eval_doc_count/25000)+1)),ext=ext)),'w')
							if eval_file:
								eval_file.close()

							true_count = 0
							false_count = 0
							doc_count = 0
							print("Evaluating sentiment induction..")
							for file in os.listdir(save_evaluation_in_dir):
								if file[0] == "." or os.path.isdir(file):
									continue
								with open(os.path.join(save_evaluation_in_dir,file),'r') as rfile:
									for line in rfile:
										try:
											d = ujson.loads(line)
										except:
											continue
										c_r = d.get('classified_right',None)
										if c_r is not None:
											doc_count += 1
											if c_r == "True":
												true_count += 1
											else:
												false_count += 1

							with open(os.path.join(save_evaluation_in_dir,"evaluation_report.txt"),'w') as efile:
								efile.write("Accuracy of classified documents for |{method} - {vocab_type} tokens - {embedding_params}| is: ".format(method=induction_method,vocab_type=vocab_type,embedding_params=parameters_part) + str((float(float(true_count)/float(doc_count)))) + "%" + "\n")
								efile.write("Total number of documents classified:{n}".format(n=doc_count))
								efile.write("Cannot classify {n} docs".format(n=str(cannot_classify_count)))
							print("Accuracy of classified documents for |{method} - {vocab_type} tokens - {embedding_params}| is: ".format(method=induction_method,vocab_type=vocab_type,embedding_params=parameters_part) + str((float(float(true_count)/float(doc_count))*100))[:5] + "%")
							print("Total number of documents classified:{n}".format(n=doc_count))
							print("Cannot classify {n} docs".format(n=str(cannot_classify_count)))

