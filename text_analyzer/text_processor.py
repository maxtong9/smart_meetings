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



class TextProcessor:
    def __init__(self, rawTranscription):
        self.raw = rawTranscription
        # self.wordList = None #nltk.word_tokenize(self.raw)
        # self.sentenceList = None #nltk.sent_tokenize(self.raw)
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

    def printData(self):
        print('Transcription:\n', self.raw, '\n')

    def summarize(self):
        # Remove stop words
        # Convert Paragraphs to Sentences
        # wordList = nltk.word_tokenize(self.raw)
        # print(wordList)
        # # wordList = self.removeWhiteSpace(wordList)
        # # Remove stopwords and commas
        # for word in wordList:
        #     if word.lower() in self.stopwords or word is ',' or word is ', ':
        #         wordList.remove(word)

        # print(wordList)

        # Here we are getting the list of sentences with removed stop words and commas (might need to add more things0)
        masterSentList = []
        sentList = nltk.sent_tokenize(self.raw)
        for sent in sentList:
            wordNoStopList = []
            for word in nltk.word_tokenize(sent):
                if (word.lower() not in self.stopwords) and word is not ',':
                    wordNoStopList.append(word)
            masterSentList.append(wordNoStopList)
        print(masterSentList)

        # Here we are getting the master tokenized word list
        masterTokenizeList = []
        for tokenSent in masterSentList:
            print(tokenSent)
            for word in tokenSent:
                # Remove Periods
                if word is not '.':
                    masterTokenizeList.append(word.lower())

        # Here we get the frequency distr of the most common word
        print(masterTokenizeList)
        most_occuring_value = nltk.probability.FreqDist(masterTokenizeList).most_common(1)[0][1]
        print(most_occuring_value)

        # Here we are getting the word with the corresponding freq distr
        # word_and_weighted_freq = {}
        # for word in masterTokenizeList:
        #     word = word.lower() # Might be able to remove when using Watson
        #     if word not in word_and_weighted_freq.keys():
        #         word_and_weighted_freq[word] = 1
        #     else:
        #         word_and_weighted_freq[word] += 1
        # print(word_and_weighted_freq)

        # Get frequency of eeach word
        word_and_weighted_freq = nltk.probability.FreqDist(masterTokenizeList)
        # Get weighted freq of each word relative to most common word
        for word_key in nltk.probability.FreqDist(masterTokenizeList):
            word_and_weighted_freq[word_key] = word_and_weighted_freq[word_key] / most_occuring_value
        print(word_and_weighted_freq.most_common(10))
        print("SENTENCE LIST: \n", sentList)
        print("\n")
        
        # Calculate sum of weighted frequencies by sentences
        output = []
        for sentence in sentList:
            freqSum = 0
            for word in nltk.word_tokenize(sentence):
                if word.lower() in word_and_weighted_freq.keys():
                    freqSum+=word_and_weighted_freq[word.lower()]

            # Place in order of highest first
            # Might be a better way to do this
            i = 0
            appended = False
            while len(output) is not 0 and i < len(output):
                if output[i][1] < freqSum:
                    output.insert(i, (sentence, freqSum))
                    appended = True
                    break
                i += 1
            if not appended:
                # Append to end
                output.append((sentence, freqSum))

        print("*****OUTPUT*****\n", output)
        return output
    

    # Extension to the original summarize algorithm
    # The key difference in this algorithm is that we comapare the words 
    # In each sentence and remove sentences that have close to the same words 
    # As some other sentences
    def summarize2():

'''
Testing Here
'''
if __name__ == "__main__":
    # Demo Input
    demoInput = "So, keep working. Keep striving. Never give up. Fall down seven times, get up eight. Ease is a greater threat to progress than hardship. Ease is a greater threat to progress than hardship. So, keep moving, keep growing, keep learning. See you at work."
    # Processing Object
    tp = TextProcessor(demoInput)

    tp.summarize()

            



    