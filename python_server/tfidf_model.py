from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import brown # NEEDS TO BE TURNED ON WHEN GENE
from string import punctuation
from nltk.corpus import stopwords 
from nltk import word_tokenize
import pickle

stop_words = stopwords.words('english') + list(punctuation)

# Set up translation table for use with string.translate(translator)

'''
Gets all the words in the Brown Corpus
'''

# def getDoc():
#     translator = str.maketrans('', '', punctuation)
#     docs = brown.fileids()
#     for f in docs:
#         doc = brown.words(f)
#         doc = [w.lower().translate(translator).strip() for w in doc]
        

def tokenize(text):
    words = word_tokenize(text)
    words = [w.lower() for w in words]
    translator = str.maketrans('', '', punctuation)
    return [w.split('/')[0] for w in words if w not in stop_words and not w.isdigit()]

# '''
# Used to save the model
# '''

def getVocabulary():
    vocabulary = set()
    for file_id in brown.fileids():
        words = tokenize(brown.raw(file_id))
        vocabulary.update(words)
        print(words)
    
    vocabulary = list(vocabulary)
    word_index = {w: idx for idx, w in enumerate(vocabulary)}
    
    VOCABULARY_SIZE = len(vocabulary)
    DOCUMENTS_COUNT = len(brown.fileids())
    return vocabulary

def saveModel():
    vocabulary = getVocabulary()
    tfidf = TfidfVectorizer(stop_words=stop_words, tokenizer=tokenize, vocabulary=vocabulary)
    tfidf.fit([brown.raw(file_id) for file_id in brown.fileids()])
    filename = 'tfidf_model.pickle'
    pickle.dump(tfidf, open(filename, 'wb'))

def testModel():
    tfidf = pickle.load(open('tfidf_model.pickle', 'rb'))

    X = tfidf.transform(["Here we go, here is a good example here! This is amazing. These are just sentences"])

    try:
        print(X[0, tfidf.vocabulary_['amazaaiang']])
        print(tfidf.vocabulary_['amazing'])
    except KeyError:
        print("Caught the KeyError. Calculate with low idf here")
        # Calculate Term Frequency (occurences / total words)
        # Multiply by a really low Idf because it's not in the current vocabulary





# print(brown.raw('test/14829'))

if __name__ == '__main__':
    # TURN ONE ON OR OFF TO EITHER SAVE A MODEL (PROBABLY DELETE .PICKLE FIRST)
    # OR TEST THE WORKING MODEL (NEED A .PICKLE TO DO)
    #saveModel()

    testModel()




