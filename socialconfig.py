import os.path as path
socialsentRun_proj_dir = path.dirname(__file__)

config = {
	"YELP_DATASET_DIR" : path.join(socialsentRun_proj_dir,"yelp_dataset"),
	"YELP_REVIEWS_FILE_NAME" : "yelp_academic_dataset_review.json",
	"YELP_BUSINESSES_FILE_NAME" : "yelp_academic_dataset_business.json",
	"SAVE_BUSINESSES_BY_CATEGORY_DIRECTORY" : path.join(socialsentRun_proj_dir,"businesses","category"),
	"SAVE_BUSINESSES_BY_STATE_DIRECTORY" : path.join(socialsentRun_proj_dir,"businesses","state"),
	"SAVE_REVIEWS_DIRECTORY" : path.join(socialsentRun_proj_dir,"reviews"),
	"SAVE_REVIEWS_BY_CATEGORY_DIRECTORY" : path.join(socialsentRun_proj_dir,"reviews","category"),
	"SAVE_DICTIONARY_DIR" : path.join(socialsentRun_proj_dir,"Dictionaries"),
	"SAVE_POLARITIES_DIR" : path.join(socialsentRun_proj_dir,"InducedPolarities"),
	"SAVE_ALL_MODEL_PARAMS_COLLECTIVE_POLARITIES_DIR" : path.join(socialsentRun_proj_dir,"CollectPolaritiesForAllModelParams"),
	"SAVE_MEAN_POLARITIES_PER_CATEGORY_DIR" : path.join(socialsentRun_proj_dir,"MeanPolaritiesByCategory"),
	"SAVE_BAG_OF_WORDS_DIR" : path.join(socialsentRun_proj_dir,"ReviewsAsBagOfWords"),
	"SAVE_N_BAG_OF_WORDS_DOCS_PER_FILE" : 25000,
	"SAVE_WORD2VEC_MODELS_DIR":path.join(socialsentRun_proj_dir,"Word2Vec_Models"),
	"SAVE_WORD_EMBEDDINGS_DIR" : path.join(socialsentRun_proj_dir,"WordEmbeddings"),
	"EVALUATE_SENTIMENTS_DIR" : path.join(socialsentRun_proj_dir,"EvaluateReviewsSentimentByInducedPolarities"),
	"COLLECT_ACCURACIS_DIR" : path.join(socialsentRun_proj_dir,"CollectAccuracies"),
	"SAVE_TOP30_POS_NEG_WORDS_ALL_MODELS_DIR" : path.join(socialsentRun_proj_dir,"Top30PosNegWords"),
	"PROCESS_N_REVIEWS_ONLY" : 1000000,
	"PROCESS_N_REVIEWS_ONLY_PER_CATEGORY" : 1000000,
	"FILTERED_DICTINARIES_CONF":{
		"vocab_top5000":{
			"keep_n" : 5000,
			"no_below": 1,
		},
		"vocab_top10000":{
			"keep_n" : 10000,
			"no_below": 1,
		},
		"vocab_top15000":{
			"keep_n" : 15000,
			"no_below": 1,
		},
		"vocab_top20000":{
			"keep_n" : 20000,
			"no_below": 1,
		},
		"vocab_top25000":{
			"keep_n" : 25000,
			"no_below": 1,
		},
	},
	"WORD2VEC_MODELS_CONF":{
		"vocab_top5000":{
			"vocabTop5000_dim100_window2": {
				"size":100,
				"window":2
				},
			"vocabTop5000_dim100_window3": {
				"size":100,
				"window":3
				},
			"vocabTop5000_dim100_window4": {
				"size":100,
				"window":4
				},
			"vocabTop5000_dim200_window2": {
				"size":200,
				"window":2
				},
			"vocabTop5000_dim200_window3": {
				"size":200,
				"window":3
				},
			"vocabTop5000_dim200_window4": {
				"size":200,
				"window":4
				},
			"vocabTop5000_dim300_window2": {
				"size":300,
				"window":2
				},
			"vocabTop5000_dim300_window3": {
				"size":300,
				"window":3
				},
			"vocabTop5000_dim300_window4": {
				"size":300,
				"window":4
				},
			},
		"vocab_top10000":{
			"vocabTop10000_dim100_window2": {
				"size":100,
				"window":2
				},
			"vocabTop10000_dim100_window3": {
				"size":100,
				"window":3
				},
			"vocabTop10000_dim100_window4": {
				"size":100,
				"window":4
				},
			"vocabTop10000_dim200_window2": {
				"size":200,
				"window":2
				},
			"vocabTop10000_dim200_window3": {
				"size":200,
				"window":3
				},
			"vocabTop10000_dim200_window4": {
				"size":200,
				"window":4
				},
			"vocabTop10000_dim300_window2": {
				"size":300,
				"window":2
				},
			"vocabTop10000_dim300_window3": {
				"size":300,
				"window":3
				},
			"vocabTop10000_dim300_window4": {
				"size":300,
				"window":4
				},
			},
		"vocab_top15000":{
			"vocabTop15000_dim100_window2": {
				"size":100,
				"window":2
				},
			"vocabTop15000_dim100_window3": {
				"size":100,
				"window":3
				},
			"vocabTop15000_dim100_window4": {
				"size":100,
				"window":4
				},
			"vocabTop15000_dim200_window2": {
				"size":200,
				"window":2
				},
			"vocabTop15000_dim200_window3": {
				"size":200,
				"window":3
				},
			"vocabTop15000_dim200_window4": {
				"size":200,
				"window":4
				},
			"vocabTop15000_dim300_window2": {
				"size":300,
				"window":2
				},
			"vocabTop15000_dim300_window3": {
				"size":300,
				"window":3
				},
			"vocabTop15000_dim300_window4": {
				"size":300,
				"window":4
				},
			},
		"vocab_top20000":{
			"vocabTop20000_dim100_window2": {
				"size":100,
				"window":2
				},
			"vocabTop20000_dim100_window3": {
				"size":100,
				"window":3
				},
			"vocabTop20000_dim100_window4": {
				"size":100,
				"window":4
				},
			"vocabTop20000_dim200_window2": {
				"size":200,
				"window":2
				},
			"vocabTop20000_dim200_window3": {
				"size":200,
				"window":3
				},
			"vocabTop20000_dim200_window4": {
				"size":200,
				"window":4
				},
			"vocabTop20000_dim300_window2": {
				"size":300,
				"window":2
				},
			"vocabTop20000_dim300_window3": {
				"size":300,
				"window":3
				},
			"vocabTop20000_dim300_window4": {
				"size":300,
				"window":4
				},
			},
		"vocab_top25000":{
			"vocabTop25000_dim100_window2": {
				"size":100,
				"window":2
				},
			"vocabTop25000_dim100_window3": {
				"size":100,
				"window":3
				},
			"vocabTop25000_dim100_window4": {
				"size":100,
				"window":4
				},
			"vocabTop25000_dim200_window2": {
				"size":200,
				"window":2
				},
			"vocabTop25000_dim200_window3": {
				"size":200,
				"window":3
				},
			"vocabTop25000_dim200_window4": {
				"size":200,
				"window":4
				},
			"vocabTop25000_dim300_window2": {
				"size":300,
				"window":2
				},
			"vocabTop25000_dim300_window3": {
				"size":300,
				"window":3
				},
			"vocabTop25000_dim300_window4": {
				"size":300,
				"window":4
				},
			},
	},
	"REVIEWS_CATEGORIES_LIST":["planning","bars","food","grooming","health","learn","municipal","services","shopping","sports","leisure"],
}

FOOD_POSITIVE_SEEDS = ["good","great","delicious","best","nice","excellent","amazing","friendly","fresh","tasty","awesome","perfect","clean","fantastic","wonderful","reasonable","beautiful"]
FOOD_NEGATIVE_SEEDS = ["disappointed","bad","wrong","terrible","worst","poor","awful","sad","soggy","ridiculous","dirty","odd","burnt","undercooked","bitter","stupid","messy"]

BARS_POSITIVE_SEEDS = ["great","nice","amazing","awesome","favorite","happy","perfect","fantastic","tasty","wonderful","beautiful","clean"]
BARS_NEGATIVE_SEEDS = ["bad","small","terrible","horrible","disappointed","rude","awful","ridiculous","sad","dirty","soggy","unprofessional"]

LEISURE_POSITIVE_SEEDS = ["great","nice","excellent","helpful","fantastic","super","fun","professional","incredible","pleasant","gorgeous"]
LEISURE_NEGATIVE_SEEDS = ["bad","horrible","rude","disappointed","cheap","dirty","awful","ridiculous","uncomfortable","unacceptable","crappy"]

GROOMING_POSITIVE_SEEDS = ["amazing","friendly","beautiful","professional","fantastic","knowledgeable","sweet","fabulous","relaxing","affordable"]
GROOMING_NEGATIVE_SEEDS = ["horrible","rude","unprofessional","disappointed","poor","awful","upset","ridiculous","uncomfortable","disappointing"]

HEALTH_POSITIVE_SEEDS = ["great","friendly","professional","happy","amazing","clean","wonderful","knowledgeable","awesome","excellent","fantastic"]
HEALTH_NEGATIVE_SEEDS = ["bad","rude","unprofessional","terrible","disappointed","awful","uncomfortable","frustrating","incompetent","unacceptable","shady"]

LEARN_POSITIVE_SEEDS = ["great","nice","friendly","fantastic","impressed","beautiful","helpful","perfect","wonderful","fun","professional","knowledgeable"]
LEARN_NEGATIVE_SEEDS = ["wrong","terrible","expensive","ridiculous","disappointing","unprofessional","gross","difficult","unacceptable","boring","shady","unhelpful"]

SHOPPING_POSITIVE_SEEDS = ["best","happy","amazing","awesome","professional","knowledgeable","perfect","wonderful","beautiful","fantastic","courteous","outstanding"]
SHOPPING_NEGATIVE_SEEDS = ["bad","rude","horrible","disappointed","unprofessional","ridiculous","awful","dirty","disrespectful","frustrating","unacceptable","filthy"]

PLANNING_POSITIVE_SEEDS = ["knowledgeable","amazing","awesome","wonderful","responsive","informative","fabulous","approachable","respectful","compassionate","phenomenal","impeccable","superb"]
PLANNING_NEGATIVE_SEEDS = ["terrible","horrible","unprofessional","frustrating","dishonest","outrageous","disrespectful","unwilling","unresponsive","pathetic","incompetent","unprofessional","unethical"]

SERVICES_POSITIVE_SEEDS = ["great","awesome","fantastic","courteous","impressed","pleased","affordable","efficient","fast","incredible","spacious","fabulous","reliable","informative","gorgeous","timely"]
SERVICES_NEGATIVE_SEEDS = ["horrible","rude","terrible","disappointed","unprofessional","uncomfortable","disrespectful","frustrating","outrageous","pathetic","miserable","overpriced","horrendous","lousy","unhappy","unhelpful"]

SPORTS_POSITIVE_SEEDS = ["excellent","beautiful","fantastic","perfect","wonderful","awesome","perfect","fun"]
SPORTS_NEGATIVE_SEEDS = ["bad","rude","horrible","terrible","disappointed","ridiculous","unprofessional",""]

MUNICIPAL_POSITIVE_SEEDS = ["great","awesome","wonderful","excellent","fantastic","friendly","nice","best","perfect"]
MUNICIPAL_NEGATIVE_SEEDS = ["rude","wrong","terrible","horrible","unprofessional","ridiculous","disappointed","frustrating","nasty"]

