import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd 

import numpy as np
import random
import pickle
from collections import Counter
# re.search('(?<=@)(.*)', s)
lemmatizer = WordNetLemmatizer()
hm_lines = 100000

def extract_features(not_replied, replied):
	main_features = []
	for fi in [replied,not_replied]:
		with open (fi,'r') as f:
			contents = f.readlines()
			for l in contents[:hm_lines]:
				all_words = l.lower().split()
				main_features += all_words
	w_counts = Counter(main_features)
	l2 = []
	for w in w_counts:
		l2.append(w)
	return l2

def sample_handling(sample, main_features, classification):
	featureset = []
	with open(sample,'r') as f:
		contents = f.readlines()
		for l in contents[:hm_lines]:
			current_words = l.lower().split()
			features = np.zeros(len(main_features))
			for word in current_words:
				if word.lower() in main_features:
					index_value = main_features.index(word.lower())
					features[index_value] += 1
			features = list(features)
			featureset.append([features, classification])
	return featureset

def featureset_from_main_features(sample):
	lexicon = pd.read_pickle('Models/features.pickle')
	current_words = sample.lower().split()
	features = np.zeros(len(lexicon))
	for word in current_words:
		if word.lower() in lexicon:
			index_value = lexicon.index(word.lower())
			features[index_value] = 1
	return list(features)


def create_featureset_and_labels(replied, not_replied, test_size = 0.1):
	main_feautes = extract_features(not_replied, replied)

	print("Combined feature set lenght - " , len(main_feautes))
	print("\n\nHere is the main feature set------\n" , main_feautes)

	features = []
	replied_features = sample_handling('Models/replied.txt',main_feautes, [1,0])
	print("\nSample replied feature set - \n" , replied_features[0])	
	not_replied_features = sample_handling('Models/not_replied.txt',main_feautes, [0,1]) 
	print("\nSample not_replied feature set - \n" , not_replied_features[0])	
	features = replied_features + not_replied_features
	print("\nCombine both the features and shuffle it. Total number of data sets - " , len(features))
	random.shuffle(features)

	features = np.array(features)
	testing_size = int(test_size*len(features))
	print("\nDivide data into training/testing sets. Testing size(0.1)  - ",  testing_size)  
	train_x = list(features[:,0][:-testing_size])
	train_y = list(features[:,1][:-testing_size])

	test_x = list(features[:,0][-testing_size:])
	test_y = list(features[:,1][-testing_size:])
	return train_x, train_y , test_x, test_y,main_feautes

if __name__ == '__main__' :
	train_x, train_y , test_x, test_y,main_feautes = create_featureset_and_labels('Models/replied.txt', 'Models/not_replied.txt')
	print("\nData preprocessing completed!. Now saving it....")
	with open('Models/mail_set.pickle','wb') as f :
		pickle.dump([train_x, train_y , test_x, test_y],f)
		print("\nDumped the complete training and testing data sets into mail_set.pickle - This will be used by deep nueral network.")
	with open('Models/features.pickle','wb') as f :
		print("\nDumped feature set to features.pickle. This is used for prediction data.\n\n")
		pickle.dump(main_feautes,f)










