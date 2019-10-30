'''
This File will hold all of the API related text processor functions 
'''

'''
This class is the main text processing class

Input: IBM Watson Audio -> Text Output
Output: Text processing Functions (TBD)

Design Choice: 
- all of the mutated steps during the processes are stored as variables
- When they are used (ie tokenize) they will be instantiated in the class.
- Thus, any other processes we write can use them, and if they aren't defined, 
- the process will define it itself
- This will make the processor fast because it only does an operation (ie tokenize)
- when needed. And if it's already done, then the class doesn't have to do it again.

'''
import nltk
import pickle
class TextProcessor:
    def __init__(self, rawTranscription):
        # Percentage of original text the summary length should be
        self.SUMMARY_PERCENTAGE = .59
        self.raw = rawTranscription

        self.wordList = None 
        self.sentenceList = None
    
        # self.sentenceListNoStop = None #self.removeStopWords(self.sentenceList)
        self.stopwords = nltk.corpus.stopwords.words('english')


    def removeStopWords(self, list_of_sentences):
        for sentence in list_of_sentences:
            print(sentence)

    def removeWhiteSpace(self, wordList):
        newWordList = []
        for word in wordList:
            newWordList.append(word.strip()) 
        return newWordList

    def printRawTranscription(self):
        print('Transcription:\n', self.raw, '\n')

    def dialogue_act_features(self, post):
        features = {}
        for word in nltk.word_tokenize(post):
            if word is '.' or word is '?' or word is ',' or word is '!': # No bias in transcriptions
                continue
            features['contains({})'.format(word.lower())] = True
        return features

    
    def tagQuestions(self):
        # Tokenize sentence list
        if self.sentenceList is None:
            self.sentenceList = nltk.sent_tokenize(self.raw)

        # Open file and trained classifier
        file = open('question_classifier.pickle', 'rb')
        classifier = pickle.load(file)
        # Classify the sentences and append the questions (clarify is similar to questions in our case)
        questionList = []
        for sentence in self.sentenceList:
            classification = classifier.classify(self.dialogue_act_features(sentence))
            if classification == 'whQuestion' or classification == 'Clarify':
                questionList.append(sentence)
        return questionList


    def summarize(self):
        # Here we are getting the list of sentences with removed stop words and commas (might need to add more things)
        masterSentList = []
        if self.sentenceList is None:
            self.sentenceList = nltk.sent_tokenize(self.raw)
        summary_length = int(len(self.sentenceList) * self.SUMMARY_PERCENTAGE)
        

        for sent in self.sentenceList:
            wordNoStopList = []
            for word in nltk.word_tokenize(sent):
                if (word.lower() not in self.stopwords) and word is not ',':
                    wordNoStopList.append(word)
            masterSentList.append(wordNoStopList)

        # Here we are getting the master tokenized word list
        masterTokenizeList = []
        for tokenSent in masterSentList:
            for word in tokenSent:
                # Remove Periods
                if word is not '.':
                    masterTokenizeList.append(word.lower())

        # Here we get the frequency distr of the most common word
        most_occuring_value = nltk.probability.FreqDist(masterTokenizeList).most_common(1)[0][1]

        # Get frequency of eeach word
        word_and_weighted_freq = nltk.probability.FreqDist(masterTokenizeList)
        # Get weighted freq of each word relative to most common word
        for word_key in nltk.probability.FreqDist(masterTokenizeList):
            word_and_weighted_freq[word_key] = word_and_weighted_freq[word_key] / most_occuring_value
        
        sentence_freq_sum = []
        pos = 0 #Track ordering of sentences
        # Calculate sum of weighted frequencies by sentences
        for sentence in self.sentenceList:
            freqSum = 0
            for word in nltk.word_tokenize(sentence):
                if word.lower() in word_and_weighted_freq.keys():
                    freqSum+=word_and_weighted_freq[word.lower()]
            
            # Place in order by total freq in sentence_freq_sum List
            index = 0
            appended = False
            while len(sentence_freq_sum) is not 0 and index < len(sentence_freq_sum):
                if sentence_freq_sum[index][1] < freqSum:
                    # Insert at current positino
                    appended = True
                    sentence_freq_sum.insert(index, ((sentence, freqSum, pos)))
                    break
                index += 1
            if not appended:
                sentence_freq_sum.append((sentence, freqSum, pos ))
            pos += 1



        # Take only the specified percentage and sort by order of appearance in the original transcription

        
        summary = sorted(sentence_freq_sum[:summary_length], key=lambda sentence: sentence[2])        # Sort by sentence list ordering



        # Format the output
        returnSummary = ""
        for sentence in summary:
            returnSummary += (sentence[0] + " ")


        return returnSummary
    
'''
Testing Here
'''
if __name__ == "__main__":
    # Demo Input
    demoInput = "How did you get here? So, keep working. Keep striving. Never give up. Fall down seven times, get up eight. Ease is a greater threat to progress than hardship. Ease is a greater threat to progress than hardship. So, keep moving, keep growing, keep learning. See you at work."
    # Processing Object
    tp = TextProcessor(demoInput)

    tp.summarize()
    tp.tagQuestions()

            



    