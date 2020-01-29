from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import brown
from string import punctuation
from nltk.corpus import stopwords 
from nltk import word_tokenize
import pickle

stop_words = stopwords.words('english') + list(punctuation)

def tokenize(text):
    words = word_tokenize(text)
    words = [w.lower() for w in words]
    return [w for w in words if w not in stop_words and not w.isdigit()]

'''
Used to save the model
'''
vocabulary = set()
for file_id in brown.fileids():
    words = tokenize(brown.raw(file_id))
    vocabulary.update(words)
 
vocabulary = list(vocabulary)
word_index = {w: idx for idx, w in enumerate(vocabulary)}
 
VOCABULARY_SIZE = len(vocabulary)
DOCUMENTS_COUNT = len(brown.fileids())




# tfidf = TfidfVectorizer(stop_words=stop_words, tokenizer=tokenize, vocabulary=vocabulary)
# tfidf.fit([brown.raw(file_id) for file_id in brown.fileids()])
# filename = 'tfidf_model.pickle'
# pickle.dump(tfidf, open(filename, 'wb'))




#tfidf = pickle.load(open('tfidf_model.pickle', 'rb'))

#X = tfidf.transform(["Here we go, here is a good example here! This is amazing"])

#print(tfidf.vocabulary_[creeps])
#print(brown.raw('test/14829'))





# print(brown.raw('test/14829'))