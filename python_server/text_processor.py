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
    def __init__(self, rawData):
        # Percentage of original text the summary length should be
        self.SUMMARY_PERCENTAGE = .59
        # Action Item Keywords (lower)
        self.ACTION_ITEM_KEYWORD = ["action", "item"]
        # List of the speakers in the same order as the sentenceList
        self.speakerList = None

        self.raw_data = rawData

        # RAW Transcription of only the sentences (or phrases)
        self.raw = None

        # Master Raw List of the Sentences. Thiswill only be initialized. Never mutated
        self.sentenceList = None

        self.stopwords = nltk.corpus.stopwords.words('english')

        self.transform_input()

        self.questionStarters = ['what', 'when', 'where', 'how', 'are', 'who', 'why', 'is', 'can', 'could', 'would']

    '''
    Transforms the input of Audio -> text to a list of usable strings
    '''
    def transform_input(self):
        self.speakerList = []
        self.sentenceList = []
        for phraseList in self.raw_data:
            self.speakerList.append(phraseList[0])
            self.sentenceList.append(phraseList[1])



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
        actionItem = False
        for sentence in self.sentenceList:
            if actionItem:
                actionItems.append(sentence)
                actionItem = False
            words = nltk.word_tokenize(sentence)
            if len(words) >= 2:
                if words[0] == self.ACTION_ITEM_KEYWORD[0] and words[1] == self.ACTION_ITEM_KEYWORD[1]:
                    # actionItems.append(self.joinWordsToSentence(words[2:]))
                    actionItem = True
        return self.joinSentenceListToSentence(actionItems)
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
        file = open('question_classifier.pickle', 'rb')
        classifier = pickle.load(file)
        # Classify the sentences and append the questions (clarify is similar to questions in our case)
        questionList = []
        for sentence in sentNoAction:
            classification = classifier.classify(self.dialogue_act_features(sentence))
            if classification == 'whQuestion':
                questionList.append(sentence)
                continue
            starting_word = nltk.word_tokenize(sentence)[0].lower()
            if starting_word in self.questionStarters:
                questionList.append(sentence)
        return questionList

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
                    # Insert at current position
                    appended = True
                    sentence_freq_sum.insert(index, ((sentence, freqSum, pos, self.speakerList[pos])))
                    break
                index += 1
            if not appended:
                sentence_freq_sum.append((sentence, freqSum, pos, self.speakerList[pos] ))
            pos += 1

        # Take only the specified percentage and sort by order of appearance in the original transcription
        summary = sorted(sentence_freq_sum[:summary_length], key=lambda sentence: sentence[2])        # Sort by sentence list ordering

        # Format summary for joinSentenceListToSentence Input
        listOfSent = []
        for sent in summary:
            listOfSent.append((sent[3], sent[0]))
        # Format the output of summary
        # returnSummary = self.joinSentenceListToSentence(listOfSent)


        return listOfSent

'''
Minimal
Testing Here
'''
if __name__ == "__main__":
    # Demo Input
    demoInput = [[0, "so have you thought of what you're gonna paint. ", 0.87, 4.3], [1, 'I did think about it. ', 5.38, 6.33], [1, "so that's what the does want me to commission I think I don't know if I told you or not but like she said she wanted like %HESITATION the only got a drummer Denny junior league memes. ", 6.81, 14.33], [1, "but I was like well you can't paint to give so I was thinking about %HESITATION. ", 14.9, 18.6], [1, 'we did I tell you this. ', 19.48, 20.51], [1, "I don't remember okay I'll think about doing that you know the the meme of those like to spider man like pointing at each other. ", 22.39, 28.06], [1, 'they also do that exit replace one of the Spiderman Iron Man. ', 28.99, 31.99], [1, 'and then I I really want to do the bold and brash paintings. ', 34.92, 38.8], [1, 'from SpongeBob. ', 39.3, 40.34], [1, "the one that's like. ", 42.28, 43.24], [1, 'Woodward but. ', 44.2, 45.0], [1, 'yeahthose are my two ideas so far. ', 48.04, 50.48], [0, "that's cool. ", 48.91, 49.65], [0, 'you have to draw all eight how do you tell us the Ironman gonna be. ', 52.36, 56.12], [1, "I don't know. ", 54.99, 55.78], [1, 'this call is probably gonna take awhile. ', 56.27, 57.99], [1, "yeah Blake they don't have faces so I don't have to worry about drawing faces. ", 60.92, 64.69], [0, "that's true. ", 66.53, 67.36], [0, 'this will be hard. ', 69.49, 70.83], [0, 'you should do something abstract to. ', 72.49, 74.24], [0, '%HESITATION like something like that you know how place. ', 75.18, 77.72], [0, 'you know when you know when painters how Blake. ', 78.6, 80.99], [0, 'a set of. ', 81.83, 82.8], [0, '%HESITATION a set of heating the whole heck for. ', 83.87, 87.06], [0, 'four paintings in one side. ', 87.63, 89.29], [1, 'sorryyeahit can all be like. ', 88.09, 89.84], [1, 'no no. ', 90.77, 91.31], [1, 'African wildlife theme. ', 92.56, 94.19], [0, 'I would think you. ', 96.53, 97.6], [0, 'yeah and you can finally have something on your wall. ', 98.53, 101.23], [1, "all I know it's just I don't know when I'm going to do it because. ", 99.38, 102.53], [1, "Friday we're going. ", 103.08, 104.1], [1, "downtownand then I've mid term on Tuesday or so probably shouldn't do it this weekend maybe I will maybe I won't care I'll just do it. ", 107.24, 114.69], [0, 'yeahyou can use it as a study break. ', 117.41, 119.58], [1, "yeahthat's true. ", 119.91, 120.49], [1, 'we still gonna do Bob Ross. ', 121.79, 123.4], [0, 'I want to. ', 126.98, 127.95], [0, 'should I mean would be invite people or would be to us. ', 131.15, 134.76], [1, "sureI don't really care. ", 134.87, 135.76], [1, 'up to you. ', 137.16, 137.99], [0, "as if it it we might before we'd have to get more stuff. ", 139.58, 144.28], [1, 'yeah. ', 142.86, 143.37], [1, '%HESITATION like the paint tubes. ', 143.96, 145.18], [1, 'are so small. ', 146.17, 146.92], [1, "is I don't know I thought the bigger. ", 148.72, 151.02], [0, 'I can get you get you a bunch of paint for Christmas and the like add to your collection. ', 152.53, 159.2], [1, "yeah I still haven't put my dog pictures. ", 159.24, 161.13], [0, 'I know do you have. ', 163.56, 164.6], [0, "you do have the condenser it's. ", 165.44, 168.02], [1, 'yeah and I like to save the image or like the picture. ', 167.1, 171.3], [1, 'sticky square things. ', 172.61, 173.94], [1, "it isn't too lazy. ", 175.05, 176.36], [1, "yeahif you wait until late next year you're not ever going to do it %HESITATION yeah I. ", 181.54, 4.32], [1, 'I know. ', 183.82, 184.45], [1, 'I need to do it sometime. ', 185.55, 186.75]]
    # Processing Object
    tp = TextProcessor(demoInput)
    print("Summary: \n")
    print(tp.summarize())
    print("Question List: \n")
    print(tp.getQuestionList())
    print("Action Items: \n")
    print(tp.getActionItems())
    print("RAW TRANSCRIPTION: \n")
    print(tp.raw)
