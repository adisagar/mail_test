import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd 

import numpy as np
import random
import pickle
from collections import Counter

lemmatizer = WordNetLemmatizer()
hm_lines = 100000

def create_lexicon(neg, pos):
	lexicon = []
	for fi in [pos,neg]:
		with open (fi,'r') as f:
			contents = f.readlines()
			for l in contents[:hm_lines]:
				all_words = l.lower().split()
				lexicon += all_words
	w_counts = Counter(lexicon)
	l2 = []
	for w in w_counts:
		l2.append(w)
	return l2

def sample_handling(sample, lexicon, classification):
	featureset = []
	with open(sample,'r') as f:
		contents = f.readlines()
		for l in contents[:hm_lines]:
			current_words = l.lower().split()
			features = np.zeros(len(lexicon))
			for word in current_words:
				if word.lower() in lexicon:
					index_value = lexicon.index(word.lower())
					features[index_value] += 1
			features = list(features)
			featureset.append([features, classification])
	return featureset

def featureset_from_lexicon(sample):
	print("Before load:")
	lexicon = pd.read_pickle('Models/lexicon.pickle')
	print("lexicon : ", len(lexicon))
	current_words = sample.lower().split()
	features = np.zeros(len(lexicon))
	for word in current_words:
		if word.lower() in lexicon:
			index_value = lexicon.index(word.lower())
			features[index_value] = 1
	return list(features)


def create_featureset_and_labels(pos, neg, test_size = 0.1):
	lexicon = create_lexicon(neg, pos)

	features = []
	features += sample_handling('replied.txt',lexicon, [1,0])
	features += sample_handling('not_replied.txt',lexicon, [0,1])
	random.shuffle(features)

	features = np.array(features)
	testing_size = int(test_size*len(features))
	train_x = list(features[:,0][:-testing_size])
	train_y = list(features[:,1][:-testing_size])

	test_x = list(features[:,0][-testing_size:])
	test_y = list(features[:,1][-testing_size:])
	print("len of lex while returnign", lexicon)
	return train_x, train_y , test_x, test_y,lexicon

if __name__ == '__main__' :
	train_x, train_y , test_x, test_y,lexicon = create_featureset_and_labels('replied.txt', 'not_replied.txt')
	with open('Models/sentiment_set.pickle','wb') as f :
		pickle.dump([train_x, train_y , test_x, test_y],f)
	with open('Models/lexicon.pickle','wb') as f :
		print("Len of lex while dumping", len(lexicon))
		pickle.dump(lexicon,f)










