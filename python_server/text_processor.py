'''
This File will hold all of the API related text processor functions 
'''

'''
This class is the main text processing class

Input: IBM Watson Audio Text Output
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
        # Action Item Keywords (lower case)
        self.ACTION_ITEM_KEYWORD = ["action", "item"]

        # RAW Transcription
        self.raw = rawTranscription

        # Master Raw List of the Sentences. Thiswill only be initialized. Never mutated
        self.sentenceList = None
    
        self.stopwords = nltk.corpus.stopwords.words('english')

    '''
    Removes The Stop Words From a List of Sentences
    Input: List of Sentences with presumably stop words
    Output: List of Sentences with no stop words included
    '''
    def removeStopWords(self, list_of_sentences):
        noStopWordSentenceList = []
        for sent in list_of_sentences:
            wordNoStopList = []
            for word in nltk.word_tokenize(sent):
                if (word.lower() not in self.stopwords) and word != ',':
                    wordNoStopList.append(word)
            noStopWordSentenceList.append(wordNoStopList)
        return noStopWordSentenceList

    '''
    Helper Function, Removes the white space from each word
    '''
    def removeWhiteSpace(self, wordList):
        newWordList = []
        for word in wordList:
            newWordList.append(word.strip()) 
        return newWordList


    '''
    Joins A List Of Sentences into A Sentence String
    '''
    def joinSentenceListToSentence(self, listOfSentences):
        sentString = ""
        for sent in listOfSentences:
            sentString += sent + " "
        return sentString[:-1]


    
    '''
    Joins a list of words into a sentence string.
    '''
    def joinWordsToSentence(self, listOfWords):
        sentence = ""
        for word in listOfWords:
            if word != '.':
                sentence += word + " "

        # [:-1] gets rid of the last " " and then we add a period
        return sentence[:-1] + '.'


    '''
    Removes any action items from the original transcription (sanitizes)
    - In: Sentence List (with supposed action words)
    - Out: Sentence List Without action item keywords
    PRESUMPTION: Key Phrase is at the beginning of a sentence
    '''    
    def removeActionItemKeywords(self, sentList):
        newSentList = []
        for sentence in sentList:
            words = nltk.word_tokenize(sentence)
            if len(words) >= 2:
                if words[0] == self.ACTION_ITEM_KEYWORD[0] and words[1] == self.ACTION_ITEM_KEYWORD[1]:
                    newSentList.append(self.joinWordsToSentence(words[2:]))
                else:
                    newSentList.append(self.joinWordsToSentence(words))
        return newSentList

    '''
    This Function returns a list of all of the action Items in the Transcription
    Presumption: Key Phrase is at the beginning of the sentence
    If Presumption does not hold, then will have to implement another way
    '''
    # TODO: Might need to use .lower()
    def getActionItems(self):
        if self.sentenceList is None:
            self.sentenceList = nltk.sent_tokenize(self.raw)
        actionItems = []
        for sentence in self.sentenceList:
            words = nltk.word_tokenize(sentence)
            if len(words) >= 2:
                if words[0] == self.ACTION_ITEM_KEYWORD[0] and words[1] == self.ACTION_ITEM_KEYWORD[1]:
                    actionItems.append(self.joinWordsToSentence(words[2:]))
        return actionItems
    '''
    Helper Function for getQuestionList (formats properly to be classified)
    '''
    def dialogue_act_features(self, post):
        features = {}
        for word in nltk.word_tokenize(post):
            if word is '.' or word is '?' or word is ',' or word is '!': # No bias in transcriptions
                continue
            features['contains({})'.format(word.lower())] = True
        return features

    '''
    Returns a list of questions based on the trained model
    '''
    def getQuestionList(self):
        # Tokenize sentence list
        if self.sentenceList is None:
            self.sentenceList = nltk.sent_tokenize(self.raw)
        sentNoAction = self.removeActionItemKeywords(self.sentenceList)

        # Open file and trained classifier
        file = open('python_server/question_classifier.pickle', 'rb')
        classifier = pickle.load(file)
        # Classify the sentences and append the questions (clarify is similar to questions in our case)
        questionList = []
        for sentence in sentNoAction:
            classification = classifier.classify(self.dialogue_act_features(sentence))
            if classification == 'whQuestion' or classification == 'Clarify':
                questionList.append(sentence)
        return self.joinSentenceListToSentence(questionList)

    '''
    Removes Punctuation in a word list
    Input: List of words with presumably punctuation
    Output: List of words without punctuation
    '''
    def removePunctuationFromWords(self, wordList):
        newWordList = []
        for word in wordList:
            if not (word == '.' or word == ',' or word == ',' or word == '?' or word == '!'):
                newWordList.append(word)
        return newWordList
                

    '''
    Returns a summary of the transcription
    - Takes the Highest freq word and gives all of the words a relative weighted frequency based on that word.
    - Sums sentence words (besides stop words) and sorts sentences in order
    - Takes n % sentences and resorts them in the order of which they were in the original transcription
    '''
    def summarize(self):
        if self.sentenceList is None:
            self.sentenceList = nltk.sent_tokenize(self.raw)

        sentNoActionItems = self.removeActionItemKeywords(self.sentenceList)

        summary_length = int(len(self.sentenceList) * self.SUMMARY_PERCENTAGE)
        
        masterSentList = self.removeStopWords(sentNoActionItems)

        # Here we are getting the master tokenized word list
        masterTokenizeList = []
        for tokenSent in masterSentList:
            for word in tokenSent:
               masterTokenizeList.append(word)
        masterTokenizeList = self.removePunctuationFromWords(masterTokenizeList)

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
        for sentence in sentNoActionItems:
            freqSum = 0
            for word in nltk.word_tokenize(sentence):
                if word.lower() in word_and_weighted_freq.keys():
                    freqSum+=word_and_weighted_freq[word.lower()]
            
            # Place in order by total freq in sentence_freq_sum List
            index = 0
            appended = False
            while len(sentence_freq_sum) != 0 and index < len(sentence_freq_sum):
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
Minimal 
Testing Here
'''
if __name__ == "__main__":
    # Demo Input
    demoInput = " action item How did you get here. Go back to work. I do not know what you want from me. This is getting very annoying. We need to focus on the meeting. How are we supposed to do that."
    # Processing Object
    tp = TextProcessor(demoInput)
    print("Summary: \n")
    print(tp.summarize())
    print("Question List: \n")
    print(tp.getQuestionList())
    print("Action Items: \n")
    print(tp.getActionItems())
