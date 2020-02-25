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


'''
Used for tfidf model...
'''
# def tokenize(text):
#     words = nltk.word_tokenize(text)
#     words = [w.lower() for w in words]
#     translator = str.maketrans('', '', punctuation)
#     return [w.split('/')[0] for w in words if w not in nltk.corpus.stopwords.words('english') and not w.isdigit()]

import nltk
import pickle
from string import punctuation
import math
import dateparser
from sklearn.feature_extraction.text import TfidfVectorizer
from tfidf_model import tokenize
from word_to_num import WordToNum

class TextProcessor:
    def __init__(self, rawData):
        # Percentage of original text the summary length should be
        self.SUMMARY_PERCENTAGE = .59
        # Percentage of Keywords against the total number of words in the text
        self.KEYWORDS_PERCENTAGE = .05
        # Action Item Keywords (lower)
        self.ACTION_ITEM_KEYWORD = ["action", "item"]
        # Deadline keyword
        self.DEADLINE_KEYWORD = ["by", "in", "on"]

        # Hesitation, that occurs in the raw transcription
        self.HESITATION1 = '% HESITATION'

        self.HESITATION2 = '%HESITATION'

        # List of the speakers in the same order as the sentenceList
        self.speakerList = None

        self.raw_data = rawData

        # Master Raw List of the Sentences. This will only be initialized. Never mutated ( Same order as the sentence list)
        self.sentenceList = None

        self.stopwords = nltk.corpus.stopwords.words('english') + list(punctuation)


        self.questionStarters = ['what', 'where', 'how', 'are', 'who', 'why', 'is', 'can', 'could', 'would', 'whose'] # Add as you think of more

        # Holds the values of all of the speakers in the meeting
        self.total_speakers = None

        # Keeps track of the number of hesitations that each person says
        self.hesitations_per_person = None

        # Keeps track of the total number of hesitations said in the meeting
        self.total_hesitation_count = 0

        # Keeps track of the total number of words in a meeting
        self.total_words = 0



        self.transform_input() # Initializes speakerList and sentenceList

# def testModel():
#     tfidf = pickle.load(open('tfidf_model.pickle', 'rb'))

#     X = tfidf.transform(["Here we go, here is a good example here! This is amazing. These are just sentences"])

#     try:
#         print(X[0, tfidf.vocabulary_['amazaaiang']])
#         print(tfidf.vocabulary_['amazing'])
#     except KeyError:
#         print("Caught the KeyError. Calculate with low idf here")
#         # Calculate Term Frequency (occurences / total words)
#         # Multiply by a really low Idf because it's not in the current vocabulary

    '''
    Gets N  Keywords pertaining to the current transcription
    '''
    def get_keywords(self):
        scores = self.tfidf()
        # print(scores)
        total_keywords = int(self.total_words * self.KEYWORDS_PERCENTAGE)
        # print(total_keywords)
        sorted_scores =  {k: v for k, v in sorted(scores.items(), key=lambda score: score[1], reverse=True)}
        # print(sorted_scores)
        # Get keywords
        keywords = []
        for keyword in sorted_scores:
            if total_keywords > 0:
                keywords.append(keyword)
                total_keywords -= 1
            else:
                break
        return keywords


        # print(scores)

    '''
    Formats the input of our meeting transcription for tfidf use
    '''
    def tfidfFormat(self):
        # Remove Action Items
        # sentNoActionItems = self.removeActionItemKeywords(self.sentenceList)

        # Remove HESITATIONS
        sentNoHesitations = self.removeHesitationFromList(self.sentenceList)

        # Get the summary length relative to the original length
        summary_length = int(len(self.sentenceList) * self.SUMMARY_PERCENTAGE)


        return self.joinSentenceListToSentence(sentNoHesitations)
        # print(self.joinSentenceListToSentence(masterSentList))


    '''
    Implements the tfidf algorithm to extract keywords
    '''
    def tfidf(self):
        tfidf = pickle.load(open('tfidf_model.pickle', 'rb'))
        raw_text = self.tfidfFormat() # Create function for getting string of entire transcription content
        # print(raw_text)
        X = tfidf.transform([raw_text])
        tfidf_scores = {}

        for word in nltk.word_tokenize(raw_text):
            try:
                if word in self.stopwords or word == "action" or word == "item":
                    continue
                tfidf_scores[word] = X[0, tfidf.vocabulary_[word]]
                # tfidf_scores.append((word, X[0, tfidf.vocabulary_[word]]))
            except KeyError:
                # Not in Brown Corpus
                # print("Word Not in Brown Corpus")
                self.get_term_frequency(word)
                tf = self.get_term_frequency(word) / self.total_words
                tfidf_scores[word] = tf * .000001
                # tfidf_scores.append((word, tf * .000001))
                # Calculate Term Frequency (occurences / total words)
                # Multiply by a really small Idf because it's not in the current vocabulary
        return tfidf_scores





    # '''
    # Implementation of the tfidf algorithm
    # This function will gather keywords from the Meeting.
    # '''
    # def tfidf(self):
    #     # Remove Action Items
    #     sentNoActionItems = self.removeActionItemKeywords(self.sentenceList)

    #     # Remove HESITATIONS
    #     sentNoHesitations = self.removeHesitationFromList(sentNoActionItems)

    #     # Get the summary length relative to the original length
    #     summary_length = int(len(self.sentenceList) * self.SUMMARY_PERCENTAGE)

    #     # Number of sentences in this case
    #     total_documents = len(self.sentenceList)
    #     # Generate Frequency Matrix
    #     freq_matrix = self.create_frequency_matrix(sentNoHesitations)

    #     # Generate Term Frequency Matrix
    #     tf_matrix = self.create_tf_matrix(freq_matrix)

    #     # Generate documents per words table
    #     word_per_doc_table = self.create_documents_per_words(freq_matrix)

    #     # Generate idf matrix
    #     idf_matrix = self.create_idf_matrix(freq_matrix, word_per_doc_table, total_documents)

    #     # Generate tf_idf matrix
    #     tf_idf_matrix = self.create_tf_idf_matrix(tf_matrix, idf_matrix)

    #     # Score the sentences
    #     sentenceValue = self.score_sentences(tf_idf_matrix)

    #     average_score = self.find_average_score(sentenceValue)

    #     print(tf_idf_matrix)


    # '''
    # Finds the average sentence score
    # '''
    # def find_average_score(self, sentenceValue) ->int:
    #     sumValues = 0
    #     for entry in sentenceValue:
    #         sumValues += sentenceValue[entry]

    #     average = (sumValues / len(sentenceValue))

    #     return average

    # '''
    # Gives weight to the sentences

    # '''
    # def score_sentences(self, tf_idf_matrix) -> dict:
    #     sentenceValue = {}

    #     for sent, f_table in tf_idf_matrix.items():
    #         total_score_per_sentence = 0

    #         count_words_in_sentence = len(f_table)
    #         for word, score in f_table.items():
    #             total_score_per_sentence += score
    #         sentenceValue[sent] = total_score_per_sentence / count_words_in_sentence

    #     return sentenceValue


    # '''
    # creates the tf-idf matrix
    # '''

    # def create_tf_idf_matrix(self, tf_matrix, idf_matrix):
    #     tf_idf_matrix = {}

    #     for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):
    #         tf_idf_table = {}

    #         for (word1, value1), (word2, value2) in zip(f_table1.items(), f_table2.items()):
    #             tf_idf_table[word1] = float(value1 * value2)

    #         tf_idf_matrix[sent1] = tf_idf_table

    #     return tf_idf_matrix

    # '''
    # Calculate IDF and generate a matrix
    # '''
    # def create_idf_matrix(self, freq_matrix, count_doc_per_words, total_documents):
    #     idf_matrix = {}

    #     for sent, f_table in freq_matrix.items():
    #         idf_table = {}

    #         for word in f_table.keys():
    #             idf_table[word] = math.log10(total_documents / float(count_doc_per_words[word]))

    #         idf_matrix[sent] = idf_table
    #     return idf_matrix

    # '''
    # Creates the documents per word table
    # " How many sentences contain a word"?
    # '''
    # def create_documents_per_words(self, freq_matrix):
    #     words_per_doc_table = {}

    #     for sent, f_table in freq_matrix.items():
    #         for word, count in f_table.items():
    #             if word in words_per_doc_table:
    #                 words_per_doc_table[word] += 1
    #             else:
    #                 words_per_doc_table[word] = 1
    #     return words_per_doc_table

    # '''
    # Create the Term Frequency Matrix
    # '''
    # def create_tf_matrix(self, freq_matrix):
    #     tf_matrix = {}

    #     for sent, f_table in freq_matrix.items():
    #         tf_table = {}

    #         count_words_in_sentence = len(f_table)
    #         for word, count in f_table.items():
    #             tf_table[word] = count / count_words_in_sentence
    #         tf_matrix[sent] = tf_table

    #     return tf_matrix




    # '''
    # Creates the frequency matrix of the words in each sentence
    # '''

    # def create_frequency_matrix(self, sentences):
    #     frequency_matrix = {}
    #     ps = nltk.PorterStemmer()

    #     for sent in sentences:
    #         freq_table = {}
    #         words = nltk.word_tokenize(sent)
    #         for word in words:
    #             word = word.lower()
    #             word = ps.stem(word)
    #             if word in self.stopwords:
    #                 continue
    #             if word in freq_table:
    #                 freq_table[word] += 1
    #             else:
    #                 freq_table[word] = 1
    #         frequency_matrix[sent[:15]] = freq_table
    #     return frequency_matrix
    '''
    Gets the Number of occurences of the given word in our document
    '''
    def get_term_frequency(self, term):
        sentNoHesitations = self.removeHesitationFromList(self.sentenceList)
        count = 0
        for sent in sentNoHesitations:
            for word in nltk.word_tokenize(sent):
                if word == term :
                    count += 1
        return count



    '''
    Gets the total number of words in the transcription
    '''
    def get_word_count(self):
        # Remove HESITATIONS
        sentNoHesitations = self.removeHesitationFromList(self.sentenceList)
        # print(sentNoHesitations)
        count = 0
        for sent in sentNoHesitations:
            for word in nltk.word_tokenize(sent):
                if word in self.stopwords:
                    continue
                else:
                    count+=1
        return count



    '''
    This function gives a percentage for each person and how much they spoke
    during a meeting.
    '''
    def timeSpoken(self):
        # Set up the number of words per person
        self.wordsPerPerson = {i: 0 for i in self.total_speakers}
        total_words = 0
        # dataPoint[0] = speaker
        # dataPoint[1] = sentence string
        for dataPoint in self.raw_data:
            listOfWords = nltk.word_tokenize(self.removeHesitationFromString(dataPoint[1]))
            for word in listOfWords:
                if word == '.' or word == '?' or word == ',' or word == '!': # Doesn't count as a real word
                    continue
                total_words += 1
                self.wordsPerPerson[dataPoint[0]] += 1
        if total_words == 0:
            return self.dicToArray2(self.wordsPerPerson) # should be all 0
        else:
            for person in self.wordsPerPerson:
                self.wordsPerPerson[person] /= total_words
            return self.dicToArray2(total_words)

# Basic Func that transforms TIMESPOKEN dictionary output to an array (Practical use for working with ruby)
    def dicToArray2(self, dic):
        arrToReturn = []
        for name in self.wordsPerPerson:
            arrToReturn.append([name, self.wordsPerPerson[name]])
        return arrToReturn

    '''
        This function will analyze people's hesitations. (The use of 'um' in their dialogue.
        It will report a percentage of the number of 'ums' against the total amount of words that they said in the transcription.

        The % Hesitations will then be removed.

        Input: rawData from th
        Output: percentage of % HESITATION s against the total number of words the person said.
    '''
    def analyzeHesitations(self):
        # Setup hesitations_per_person
        self.hesitations_per_person = {i: 0 for i in self.total_speakers}

        # Iterate through each "sentence"
        for dataPoint in self.raw_data:
            # dataPoint[0] = speaker
            # dataPoint[1] = sentence string

            # Count number of HESITATIONS in Sentence
            localCount = dataPoint[1].count(self.HESITATION2)

            # Add to total/ per person count
            self.hesitations_per_person[dataPoint[0]] += localCount
            self.total_hesitation_count += localCount


        if self.total_hesitation_count == 0:
            return self.dicToArray(self.hesitations_per_person)

        else:
            for person in self.total_speakers:
                # Divide by total count
                self.hesitations_per_person[person] /= self.total_hesitation_count

            # Higher the percentage the more the hesitations
            return self.dicToArray(self.hesitations_per_person)

    # Basic Func that transforms HESITATION dictionary output to an array (Practical use for working with ruby)
    def dicToArray(self, dic):
        arrToReturn = []
        for name in self.hesitations_per_person:
            arrToReturn.append([name, self.hesitations_per_person[name]])
        return arrToReturn

    '''
    Removes all instances of %HESITATION (self.HESITATION) from the given string, and returns a new string
    Input: String with %HESITATION
    Output: String without %HESITATION
    '''
    def removeHesitationFromString(self, string):
        return string.replace(self.HESITATION1, '').replace(self.HESITATION2, '')

    '''
    Input: List of strings
    Output: list of strings without self.HESITATION
    '''
    def removeHesitationFromList(self, listOfStrings):
        newList = []
        for string in listOfStrings:
            newList.append(self.removeHesitationFromString(string))
        return newList


    '''
    Transforms the input of Audio -> text to a list of usable strings
    '''
    def transform_input(self):
        self.speakerList = []
        self.sentenceList = []
        self.total_speakers = []
        for phraseList in self.raw_data:
            self.speakerList.append(phraseList[0])
            self.sentenceList.append(phraseList[1])
            if phraseList[0] not in self.total_speakers:
                self.total_speakers.append(phraseList[0])
        self.total_words = self.get_word_count()


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
    Joins A List Of Sentences into A String.
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
            if '.' in word or '\'' in word:
                sentence = sentence[:-1] # Remove last character from the sting
                sentence+=word + " "
            else:
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
    # def getActionItems(self):
    #     sentence_list = self.removeHesitationFromList(self.sentenceList)
    #     actionItems = []
    #     actionItem = False
    #     for sentence in self.sentenceList:
    #         if actionItem:
    #             actionItems.append(self.removeHesitationFromString(sentence))
    #             actionItem = False
    #         words = nltk.word_tokenize(sentence)
    #         if len(words) >= 2:
    #             if words[0] == self.ACTION_ITEM_KEYWORD[0] and words[1] == self.ACTION_ITEM_KEYWORD[1]:
    #                 # actionItems.append(self.joinWordsToSentence(words[2:]))
    #                 actionItem = True
    #     return self.joinSentenceListToSentence(actionItems)
    def getActionItems(self):
        #sentence_list = self.removeHesitationFromList(self.raw_data[1])
        actionItems = []
        for sentence in self.raw_data:
            # print("sentence: " + str(sentence))
            words = nltk.word_tokenize(sentence[1])
            # print("words: " + str(words))
            foundActionItem = False
            foundDeadline = False
            if len(words) >= 2:
                for i in range(0, len(words)):
                    if words[i] == self.ACTION_ITEM_KEYWORD[0] and words[i+1] == self.ACTION_ITEM_KEYWORD[1]:
                        # print("FOUND ACTION ITEM")
                        ai_index = i
                        dl_index = len(words)
                        # actionItems.append([sentence[0], self.removeHesitationFromString(self.joinWordsToSentence(words[i+2:]))])
                        foundActionItem = True
                        continue
                        # break
                    if foundActionItem == True and words[i] in self.DEADLINE_KEYWORD:
                        # print("FOUND DEADLINE")
                        if i+1 < len(words):
                            if words[i] == self.DEADLINE_KEYWORD[1]:
                                deadline = words[i:] # "in" keyword
                                dl_index = i
                            else:
                                deadline = words[i+1:] # "by" or "on" keyword
                                dl_index = i+1
                            keyword_index = i # index of the deadline keyword, without the "action item" keywords
                            otc = WordToNum()
                            deadline = otc.convert_string(deadline)
                            datetime = dateparser.parse(' '.join(deadline))
                            if datetime is not None:
                                del words[dl_index:len(words)]
                                # replace the current deadline within the action item with a properly formatted deadline
                                words[dl_index:dl_index] = deadline
                                datetime = self.format_deadline(datetime)
                                foundDeadline = True
                                # actionItems[len(actionItems)-1].append(deadline)
                                # actionItems[len(actionItems)-1][1] = actionItems[len(actionItems)-1][1][0:i]
                                break
                if foundActionItem is True:
                    actionItems.append([sentence[0], self.removeHesitationFromString(self.joinWordsToSentence(words[ai_index+2:]))])
                    if foundDeadline is True:
                        actionItems[len(actionItems)-1].append([datetime, keyword_index-2]) # subtract 2 from keyword_index to account for "action item" keywords

        return actionItems

    '''
    Helper function that formats a deadline string into a datetime object to be used by the Trello API
    yyyy-mm-ddThh:mm:ss.s+zzzzzz
    yyyy: year
    mm (first): month
    dd: day
    T: separator indicating that time-of-day follows
    hh: hour on a 24-hour clock
    mm (second): minute
    ss is whole seconds
    s (optional): fractional second
    zzzzzz: time zone
    '''
    def format_deadline(self, deadline):
        year = deadline.year
        month = deadline.month
        day = deadline.day

        datetime = str(year) + "-"
        if month < 10:
            datetime += "0"
        datetime += str(month) + "-"
        if day < 10:
            datetime += "0"
        datetime += str(day)

        datetime += "T12:00:00-08:00"

        return datetime
    
    '''
    Helper Function for getQuestionList (formats properly to be classified)
    '''
    def dialogue_act_features(self, post):
        features = {}
        for word in nltk.word_tokenize(post):
            if word == '.' or word == '?' or word == ',' or word == '!': # No bias in transcriptions
                continue
            features['contains({})'.format(word.lower())] = True
        return features

    '''
    Returns a list of questions based on the trained model
    '''
    # def getQuestionList(self):
    #
    #     sentNoAction = self.removeActionItemKeywords(self.sentenceList)
    #     sentNoHesitation = self.removeHesitationFromList(sentNoAction)
    #
    #     # Open file and trained classifier
    #     file = open('question_classifier.pickle', 'rb')
    #     classifier = pickle.load(file)
    #     # Classify the sentences and append the questions (clarify is similar to questions in our case)
    #     questionList = []
    #     for sentence in sentNoAction:
    #         classification = classifier.classify(self.dialogue_act_features(sentence))
    #         if classification == 'whQuestion':
    #             questionList.append(sentence)
    #             continue
    #         starting_word = nltk.word_tokenize(sentence)[0].lower()
    #         if starting_word in self.questionStarters:
    #             questionList.append(sentence)
    #     return questionList

    def getQuestionList(self):

        sentNoAction = self.removeActionItemKeywords(self.sentenceList)
        sentNoHesitation = self.removeHesitationFromList(sentNoAction)

        # Open file and trained classifier
        file = open('question_classifier.pickle', 'rb')
        classifier = pickle.load(file)
        # Classify the sentences and append the questions (clarify is similar to questions in our case)
        questionList = []
        for sentence in self.raw_data:
            classification = classifier.classify(self.dialogue_act_features(sentence[1]))
            sent = sentence[1][:-2] + '?'
            if classification == 'whQuestion':
                questionList.append([sentence[0], sent])
                continue
            starting_word = nltk.word_tokenize(sentence[1])[0].lower()
            if starting_word in self.questionStarters:
                questionList.append([sentence[0], sent])
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


    Outputs list of tuples [Speaker: Sentence]
    '''
    def summarize(self):
        # Remove Action Items
        sentNoActionItems = self.removeActionItemKeywords(self.sentenceList)

        # Remove HESITATIONS
        sentNoHesitations = self.removeHesitationFromList(sentNoActionItems)

        # Get the summary length relative to the original length
        summary_length = int(len(self.sentenceList) * self.SUMMARY_PERCENTAGE)

        # Remove stop words
        masterSentList = self.removeStopWords(sentNoHesitations)


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
        for sentence in sentNoHesitations:
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
    Gets a list of meeting suggestions

    Input: A dict of analysis, i.e. total time spoken, questions, action items, interruptions, meeting time etc.
    '''
    def getMeetingSuggestions(self, analyzerOutput):
        meetingSuggestions = {}
        # self.total_speakers
        print("TOTAL SPEAKERS:")
        print(self.total_speakers)

        numSpeakers = len(self.total_speakers)
        print("NUM SPEAKERS: " + str(numSpeakers))

        # Suggestions for speaking contributions
        speakingPercentages = analyzerOutput["total_time_spoken"] # speaking percentages is a list of [name, wordsPerPerson[name]]
        print("SPEAKING PERCENTAGES:")
        print(speakingPercentages)

        speakingPercentageIdeal = 1.0/numSpeakers
        print("IDEAL SPEAKING PERCENTAGES: " + str(speakingPercentageIdeal))

        # aim for each person to speak an equal amount +/- 15%
        speakingPercentageMin = speakingPercentageIdeal * 0.85
        speakingPercentageMax = speakingPercentageIdeal * 1.15
        print("SPEAKING PERCENTAGES RANGE: (" + str(speakingPercentageMin) + ", " + str(speakingPercentageMax) + ")")

        lowSpeakers = [] # list of speakers whose spoken percentages are below speakingPercentageMin
        highSpeakers = [] # list of speakers whose spoken percentages are above speakingPercentageMax

        for sp in speakingPercentages:
            percentage = sp[1]
            if percentage < speakingPercentageMin:
                lowSpeakers.append(sp)
            elif percentage > speakingPercentageMax:
                highSpeakers.append(sp)
            
        meetingSuggestions["Speaking Percentages"] = []
        if len(lowSpeakers) > 0:
            s = ""
            for i in range(len(lowSpeakers)):
                if i == len(lowSpeakers)-2:
                    s += ", and "
                elif i > 0:
                    s += ", "
                s += lowSpeakers[i][0]
            s += " appear(s) to be speaking less than their peers. Don't be afraid to contribute your great ideas!"
            meetingSuggestions["Speaking Percentages"].append(s)
        if len(highSpeakers) > 0:
            s = ""
            for i in range(len(highSpeakers)):
                if i == len(highSpeakers)-2:
                    s += ", and "
                elif i > 0:
                    s += ", "
                s += highSpeakers[i][0]
            s += " appear(s) to be dominating this meeting. Try encourging or opening the floor up to other members of the meeting!"
            meetingSuggestions["Speaking Percentages"].append(s)
        
        if len(meetingSuggestions["Speaking Percentages"]) == 0:
            meetingSuggestions["Speaking Percentages"].append("Everyone contributed to this meeting. Good job TEAM!")

        # Suggestions for action items frequencies
        actionItems = analyzerOutput["action_items"]
        print("ACTION ITEMS:")
        print(actionItems)
        meetingSuggestions["Action Items"] = []

        if len(actionItems) == 0:
            meetingSuggestions["Action Items"].append("This meeting seems to be lacking action items, which are important and helpful in finishing projects smoothly and on time.")
        else:
            numActionItemsUser = {}
            totalNumActionItems = len(actionItems)
            for ai in actionItems:
                speaker = ai[0]
                if speaker not in numActionItemsUser:
                    numActionItemsUser[speaker] = 1
                else:
                    numActionItemsUser[speaker] += 1

            numActionItemsIdeal = totalNumActionItems / numSpeakers
            numActionItemsMin = numActionItemsIdeal - 1
            numActionItemsMax = numActionItemsIdeal + 1

            fewActionItems = [] # list of people who have fewer action items than others
            manyActionItems = [] # list of people who have more action items than others

            for user, numActionItems in numActionItemsUser.items():
                if numActionItems < numActionItemsMin:
                    fewActionItems.append(user)
                elif numActionItems > numActionItemsMax:
                    manyActionItems.append(user)
            
            if len(fewActionItems) == 0 and len(manyActionItems) == 0:
                meetingSuggestions["Action Items"].append("Action items has been assigned equally amongst all members of this meeting. Great job ensuring fair task management!")
            else:
                meetingSuggestions["Action Items"].append("It appears that task division has not been allocated equally. A balanced workload reduces stress and promotes productivity!")
                if len(fewActionItems) > 0 and len(manyActionItems) > 0:
                    s1 = "" # a formatted string of the names of people who were assigned fewer action items
                    s2 = "" # a formatted string of the names of people who were assigned more action items

                    for i in range(len(fewActionItems)):
                        if i == len(fewActionItems)-2:
                            s1 += ", and "
                        elif i > 0:
                            s1 += ", "
                        s1 += fewActionItems[i]
                    for i in range(len(manyActionItems)):
                        if i == len(manyActionItems)-2:
                            s2 += ", and "
                        elif i > 0:
                            s2 += ", "
                        s2 += manyActionItems[i]
                    meetingSuggestions["Action Items"].append("For example, you could give some of " + s2 + "\'s tasks to " + s1 + ".")
                

        # Suggestions for interruptions
        interruptions = analyzerOutput["interruption"]
        print("INTERRUPTIONS:")
        print(interruptions)
        
        meetingSuggestions["Interruptions"] = []

        if len(interruptions) == 0:
            meetingSuggestions["Interruptions"].append("You all did an excellent job of making sure that everyone had the chance to finish what they had to say. Keep up the great work!")
        else:
            s = ""
            for i in range(len(interruptions)):
                if i == len(interruptions)-2:
                    s += ", and "
                elif i > 0:
                    s += ", "
                s += interruptions[i][0]
            s += " appear(s) to be interrupting other members. Make sure you're letting other people finish what they have to say!"
            meetingSuggestions["Interruptions"].append(s)

        # Suggestions for questions
        questions = analyzerOutput["questions"]
        print("QUESTIONS:")
        print(questions)
        meetingSuggestions["Questions"] = []

        if len(questions) == 0:
            meetingSuggestions["Questions"].append("This meeting seems to be lacking questions. Questions are great for promoting meeting engagement and clarity. If you're confused, don't be afraid to ask a question!")
        else:
             meetingSuggestions["Questions"].append("Awesome job asking engaging and clarifying questions! Don't forget to follow up on any questions as needed.")
        

        print("MEETING SUGGESTIONS:")
        print(meetingSuggestions)
        return meetingSuggestions

'''
Minimal
Testing Here
'''
if __name__ == "__main__":
    # Demo Input
    #demoInput = [[0, "so have you thought of what you're gonna paint. ", 0.87, 4.3], [1, 'I did think about it. ', 5.38, 6.33], [1, "so that's what the does want me to commission I think I don't know if I told you or not but like she said she wanted like %HESITATION the only got a drummer Denny junior league memes. ", 6.81, 14.33], [1, "but I was like well you can't paint to give so I was thinking about %HESITATION. ", 14.9, 18.6], [1, 'we did I tell you this. ', 19.48, 20.51], [1, "I don't remember okay I'll think about doing that you know the the meme of those like to spider man like pointing at each other. ", 22.39, 28.06], [1, 'they also do that exit replace one of the Spiderman Iron Man. ', 28.99, 31.99], [1, 'and then I I really want to do the bold and brash paintings. ', 34.92, 38.8], [1, 'from SpongeBob. ', 39.3, 40.34], [1, "the one that's like. ", 42.28, 43.24], [1, 'Woodward but. ', 44.2, 45.0], [1, 'yeahthose are my two ideas so far. ', 48.04, 50.48], [0, "that's cool. ", 48.91, 49.65], [0, 'you have to draw all eight how do you tell us the Ironman gonna be. ', 52.36, 56.12], [1, "I don't know. ", 54.99, 55.78], [1, 'this call is probably gonna take awhile. ', 56.27, 57.99], [1, "yeah Blake they don't have faces so I don't have to worry about drawing faces. ", 60.92, 64.69], [0, "that's true. ", 66.53, 67.36], [0, 'this will be hard. ', 69.49, 70.83], [0, 'you should do something abstract to. ', 72.49, 74.24], [0, '%HESITATION like something like that you know how place. ', 75.18, 77.72], [0, 'you know when you know when painters how Blake. ', 78.6, 80.99], [0, 'a set of. ', 81.83, 82.8], [0, '%HESITATION a set of heating the whole heck for. ', 83.87, 87.06], [0, 'four paintings in one side. ', 87.63, 89.29], [1, 'sorryyeahit can all be like. ', 88.09, 89.84], [1, 'no no. ', 90.77, 91.31], [1, 'African wildlife theme. ', 92.56, 94.19], [0, 'I would think you. ', 96.53, 97.6], [0, 'yeah and you can finally have something on your wall. ', 98.53, 101.23], [1, "all I know it's just I don't know when I'm going to do it because. ", 99.38, 102.53], [1, "Friday we're going. ", 103.08, 104.1], [1, "downtownand then I've mid term on Tuesday or so probably shouldn't do it this weekend maybe I will maybe I won't care I'll just do it. ", 107.24, 114.69], [0, 'yeahyou can use it as a study break. ', 117.41, 119.58], [1, "yeahthat's true. ", 119.91, 120.49], [1, 'we still gonna do Bob Ross. ', 121.79, 123.4], [0, 'I want to. ', 126.98, 127.95], [0, 'should I mean would be invite people or would be to us. ', 131.15, 134.76], [1, "sureI don't really care. ", 134.87, 135.76], [1, 'up to you. ', 137.16, 137.99], [0, "as if it it we might before we'd have to get more stuff. ", 139.58, 144.28], [1, 'yeah. ', 142.86, 143.37], [1, '%HESITATION like the paint tubes. ', 143.96, 145.18], [1, 'are so small. ', 146.17, 146.92], [1, "is I don't know I thought the bigger. ", 148.72, 151.02], [0, 'I can get you get you a bunch of paint for Christmas and the like add to your collection. ', 152.53, 159.2], [1, "yeah I still haven't put my dog pictures. ", 159.24, 161.13], [0, 'I know do you have. ', 163.56, 164.6], [0, "you do have the condenser it's. ", 165.44, 168.02], [1, 'yeah and I like to save the image or like the picture. ', 167.1, 171.3], [1, 'sticky square things. ', 172.61, 173.94], [1, "it isn't too lazy. ", 175.05, 176.36], [1, "yeahif you wait until late next year you're not ever going to do it %HESITATION yeah I. ", 181.54, 4.32], [1, 'I know. ', 183.82, 184.45], [1, 'I need to do it sometime. ', 185.55, 186.75]]

   # demoInput1 = [[2, "all right so. ", 4.38, 5.64], [1, "Max you can start. ", 5.61, 6.83], [2, "yeah %HESITATION. ", 6.64, 7.81], [2, "so. ", 8.65, 19.0], [2, "the past couple days for the past day I guess. ", 9.93, 12.47], [2, "I've been working on updating the text processor class so I'm working on like moving hesitation. ", 13.05, 19.0], [2, "and just updating that class in general %HESITATION. ", 19.84, 23.71], [2, "%HESITATION %HESITATION %HESITATION I plan to keep doing. ", 24.55, 26.65], [2, "action item. ", 27.56, 28.7], [2, "is analyzing hesitation. ", 30.13, 32.75], [2, "and. ", 34.84, 38.88], [2, "that's about it no road blocks from my side. ", 36.87, 38.88], [1, "one. ", 45.37, 117.23], [4, "okay SO zero during the meet the users to meeting thing and right now %HESITATION the process of. ", 46.22, 52.86], [4, "like creating a meeting are the bosses of uploading a file isn't synonymous with creating a user slash meeting anymore. ", 53.7, 61.27], [4, "for that now %HESITATION %HESITATION when you pre meeting or you too all you need is a name you know I should need to file. ", 61.76, 66.87], [4, "and then when you want to add a file you use the %HESITATION to edit and you add an audio file. ", 67.38, 72.3], [4, "for my action item. ", 73.56, 74.93], [4, "I will be doing %HESITATION. ", 75.77, 78.1], [4, "so. ", 79.0, 81.54], [4, "okay K. okay right. ", 80.51, 81.54], [4, "action item. ", 84.2, 85.16], [4, "I will add %HESITATION so it right now the meeting or the of the follow up loads. ", 86.13, 91.56], [4, "%HESITATION they don't stick to the meeting until. ", 92.3, 95.35], [4, "unless I click at I click create like or I could analyze or whatever so. ", 95.98, 100.98], [4, "don't so that so then %HESITATION that wouldn't work. ", 101.62, 104.44], [4, "because we want a lot of people from different computers if you access and meaning. ", 105.66, 110.0], [4, "so then I need to make it so that the the meeting retained a file until someone like allies. ", 110.49, 115.3], [1, "okay. ", 116.92, 122.27], [1, "cool. ", 121.83, 124.5], [1, "Hey. ", 123.98, 130.21], [1, "I tended to integrate post press into the dog compose folly had. ", 126.09, 130.21], [1, "then I guess. ", 131.14, 132.55], [1, "Christine this issue is gonna work on. ", 136.19, 138.43], [1, "the rails doctor file because something is on that and when I did try to. ", 139.55, 143.45], [1, "like the kind of like the Rivlin militant host Chris code. ", 144.44, 147.24], [1, "into the docket compose file to the S. and also have like a. ", 147.87, 150.35], [1, "a container an image for posters which I. ", 151.45, 154.12], [1, "but. ", 155.02, 161.69], [1, "three on the real side I guess I don't know if I can like wanted posters container but so. ", 156.97, 160.63], [4, "that is. ", 159.04, 159.44], [1, "%HESITATION. ", 161.18, 166.26], [1, "if. ", 165.75, 175.23], [1, "Christina what was on the. ", 169.25, 171.22], [1, "issue that you ran into with the ruby rose talk show. ", 171.89, 175.23], [0, "it's related to the yarn check files or yarn install check files command. ", 173.84, 178.71], [1, "okay. ", 181.48, 184.54], [0, "okay yeah I don't know like what changed but now it doesn't work. ", 182.57, 185.31], [1, "this White County all right. ", 183.2, 184.54], [1, "okay. ", 188.76, 193.6], [1, "Hey Sir. ", 192.81, 193.6], [3, "soul I looked into more reacting trying to make sense of. ", 194.84, 199.52], [3, "all of the things in the HTML files. ", 200.47, 204.29], [3, "and I also looked at boot straps. ", 205.41, 208.91], [3, "so action item I will be implementing bootstrap this weekend and. ", 210.96, 217.75], [3, "also maybe try to make dinner. ", 218.85, 221.5], [3, "the link between the home hastened users didn't work. ", 222.34, 226.46], [3, "on. ", 227.17, 227.69], [3, "this job but the roadblock is linking our. ", 228.31, 232.72], [3, "king the pages and changing. ", 233.6, 235.53], [3, "that ruby stuff to. ", 236.07, 238.43], [3, "the to react. ", 239.44, 241.74], [4, "I think %HESITATION you should probably post a question on slack %HESITATION like on Monday or something. ", 242.91, 249.98], [3, "yeah. ", 249.52, 257.9], [4, "and I'm pretty sure the invoking people will have the. ", 250.46, 253.69], [4, "a good answer for you. ", 254.56, 255.66], [3, "yeah I just wanted to try. ", 256.1, 257.9], [3, "stuff first before like. ", 258.74, 260.54], [3, "asking them questions. ", 261.95, 263.13], [3, "yeah. ", 264.22, 302.26], [4, "okay. ", 264.29, 602.51], [0, "yeah so I pretty much spent almost all they are not all day like I slept a little bit too but a lot of today just trying to figure out what's going on with. ", 271.16, 281.18], [0, "that yarn install command. ", 281.65, 283.66], [0, "%HESITATION and I have not been able to figure it out. ", 284.26, 286.74], [0, "%HESITATION because for some reason like. ", 288.43, 290.11], [0, "it doesn't seem to be. ", 291.6, 293.05], [0, "like running it or something. ", 294.43, 296.54], [0, "like when I build the image. ", 297.01, 299.04], [0, "%HESITATION but if I manually like. ", 299.88, 301.69], [3, "right. ", 301.96, 437.31], [0, "open a bash cell in the container and do your install check files like it's totally fine. ", 303.07, 308.66], [0, "so I don't know like what the issue is. ", 309.74, 311.93], [0, "%HESITATION yeah so. ", 312.6, 314.57], [2, "that's weird. ", 314.34, 314.96], [0, "action item I'm gonna talk to invoke a and see if they can. ", 316.21, 319.77], [0, "help me figure this out because I'm quite lost. ", 320.35, 323.12], [1, "the general questions about. ", 326.36, 327.47], [1, "the Duggar stuff but not quite willing to when we were coming up. ", 327.99, 330.63], [0, "yeah. ", 329.57, 359.43], [1, "so %HESITATION. ", 331.35, 332.47], [1, "so if we deserve guide to the real stuff not working if I try to do like a I just try to. ", 333.09, 338.5], [1, "do like a docket compose up %HESITATION legacy Justin can help but not this is like. ", 339.06, 344.14], [1, "it starts running that. ", 345.34, 346.31], [1, "I thought our a and any kind of. ", 347.03, 348.58], [1, "just hangs there. ", 350.07, 350.75], [0, "yeah it takes it takes a super long time for the python part to run because we're installing everything from an LTE K.. ", 350.57, 357.03], [1, "that. ", 351.82, 359.9], [0, "so it looks like it's stuck but it's not. ", 357.68, 359.43], [1, "hello. ", 359.54, 367.62], [1, "okay. ", 361.93, 362.43], [0, "yeah. ", 361.99, 380.75], [1, "what is that but isn't isn't the main python script and asset to make the change it because. ", 363.04, 367.62], [1, "the main title script is now a socket that's just always on right. ", 368.54, 372.03], [0, "yeah. ", 371.51, 372.0], [0, "%HESITATION I %HESITATION I also change something in the pipeline talk about %HESITATION. ", 372.49, 376.6], [0, "%HESITATION okay yeah I think I know you're talking about yeah. ", 377.28, 379.65], [0, "%HESITATION. ", 380.23, 388.04], [0, "yeah I just if you changed the. ", 382.31, 384.83], [0, "%HESITATION. ", 385.67, 386.23], [0, "I think it's run. ", 386.74, 388.04], [0, "and then whatever that python. ", 389.25, 390.51], [0, "files name is. ", 391.09, 392.13], [0, "%HESITATION. ", 393.56, 394.08], [0, "yep run python made up P. wife if you change it to a command like C. M. D. instead of run. ", 394.71, 400.34], [0, "%HESITATION that it won't hang there anymore. ", 400.94, 403.51], [1, "okay but they will like. ", 406.5, 407.77], [1, "but then I'll get stuck on the bills paid because of the young thing. ", 408.92, 411.07], [0, "yeah. ", 410.17, 417.3], [0, "%HESITATION wait did I say to change runs to commander command to run I went command to run. ", 411.81, 417.3], [1, "okay. ", 412.06, 418.13], [1, "seven to connect. ", 417.27, 418.13], [1, "there's a command. ", 419.29, 419.81], [0, "yeah. ", 421.18, 430.18], [1, "there isn't a command here. ", 427.6, 428.64], [0, "%HESITATION it says run. ", 429.36, 430.18], [1, "yeah. ", 432.08, 435.86], [0, "%HESITATION. ", 433.07, 439.15], [1, "are you looking like mine slide twenty three. ", 433.58, 435.86], [0, "oh yeah then change it to command whatever it isn't just change it to that. ", 435.31, 439.15], [3, "yeah. ", 437.0, 715.28], [0, "and it should be good. ", 443.34, 444.2], [1, "call. ", 443.41, 453.17], [1, "I need to actually. ", 451.77, 453.17], [1, "because something else over the weekend. ", 454.22, 455.68], [1, "instead of because I can I don't know if I can continue. ", 457.54, 460.31], [2, "you want to work on something else. ", 463.89, 465.19], [1, "I don't know if I can work on. ", 466.53, 467.8], [1, "%HESITATION. ", 468.43, 468.75], [1, "as soon. ", 469.35, 470.04], [2, "well why is that. ", 472.89, 473.61], [1, "is it the host all contains a and instead of for not like hosting different. ", 473.77, 477.68], [1, "containers were using compose now to host all essentially all three from the same instance easy to instance. ", 478.19, 483.1], [1, "so we can't. ", 483.77, 484.36], [1, "we can't quite just like. ", 485.01, 486.2], [1, "make those containers independently of each other. ", 487.62, 489.65], [1, "I don't think. ", 490.26, 490.8], [2, "did you check out to get her actions thing I should do on Thursday. ", 493.16, 497.04], [1, "that's like experimental baloney. ", 497.96, 499.78], [2, "yesterday. ", 498.1, 501.08], [2, "%HESITATION on us. ", 499.81, 501.08], [2, "%HESITATION it is but was really cool about it is that every time you merge into master which is the whole point of doing that develop branch. ", 502.69, 510.54], [2, "it'll trigger an automatic build of the docker containers in the easy to instance so if you go to our get her repo there's a new tab that just popped up within the last week. ", 511.89, 523.22], [1, "yeah yeah. ", 523.62, 524.46], [2, "to the right of pull requests and it's called actions if you scroll down just a little bit. ", 523.88, 529.06], [2, "%HESITATION there is a. ", 529.54, 531.33], [2, "deployed to Amazon ECS and you can build a docker container and push it to that you see are so that I can be deployed the CS. ", 532.9, 540.79], [2, "and you can sure that and set that up. ", 541.31, 543.82], [2, "to basically rebuild our doctor Ramage every time master is close to. ", 544.39, 550.42], [2, "I think once we have that up and running. ", 550.94, 552.8], [2, "that'll take care of a lot of our hosting problems especially if we can automate that. ", 553.29, 557.1], [2, "%HESITATION. ", 557.78, 558.38], [2, "and that again that's that's kind of I know you've been slacking I know the goal was to. ", 558.95, 563.55], [2, "push %HESITATION make a poor question a master every sprint. ", 564.07, 567.05], [2, "that's kind of my bag so I kind of forgot but that's the whole point of using the develop branch in replace of just having one master branches so we can do things like that. ", 567.54, 576.48], [2, "%HESITATION so that's definitely something that if you're working on hosting we should definitely look into and starting that up. ", 577.04, 583.28], [2, "from the start. ", 584.12, 584.68], [0, "we I have a question about the python stuff. ", 588.89, 590.8], [0, "%HESITATION. ", 592.44, 597.55], [2, "yeah. ", 593.58, 601.36], [0, "do you run pain dot P. Y. or socket listener. ", 594.24, 597.55], [0, "do you which. ", 600.08, 600.8], [2, "what was that. ", 600.8, 601.36], [4, "it's me it's me. ", 601.32, 602.51], [0, "okay. ", 601.45, 604.77], [0, "call that's it. ", 603.67, 604.77], [1, "yeah. ", 607.62, 6.83], [2, "%HESITATION for the starting script. ", 607.86, 609.16], [1, "yes the cycle of things then you'd be in there. ", 609.06, 611.47], [2, "yeah okay. ", 610.25, 611.14], [1, "Africa. ", 612.39, 617.34], [4, "no. ", 614.93, 621.16], [1, "on. ", 617.11, 640.05], [4, "about eight not remove it however once you can remove. ", 618.1, 621.16], [2, "%HESITATION. ", 618.27, 627.8], [2, "I'm guessing this oculus inner does. ", 625.76, 627.8], [4, "let me to myself %HESITATION no no you don't you should remove some of this in there. ", 627.12, 631.18], [1, "okay when no no way. ", 629.7, 631.31], [1, "I look at the current %HESITATION yeah because let's say just declared class twice a day. ", 631.94, 635.83], [1, "they said it would not have this class in Mandarin but then we just. ", 637.17, 640.05], [1, "yes ninety six the class my TCP headers in Maine right now. ", 641.51, 644.92], [4, "all right the classes in Maine %HESITATION **** what. ", 642.35, 644.44], [1, "I guess we should be able to keep populace and probably and then. ", 645.62, 648.48], [4, "%HESITATION. ", 648.04, 653.65], [4, "okay can look at the top of the sinner and just change it to %HESITATION TCP handler. ", 649.6, 653.65], [4, "so. ", 655.76, 656.22], [4, "I'll probably do that whatever it's not really urgent. ", 656.98, 660.96], [1, "make an action on. ", 658.7, 659.71], [4, "action item. ", 663.46, 664.31], [4, "change. ", 665.15, 675.1], [4, "okay action item make %HESITATION to speak Heller classes from. ", 667.92, 672.5], [4, "go from Maine to suck a listener. ", 673.05, 675.1], [1, "cool. ", 676.46, 682.57], [2, "great. ", 677.97, 686.77], [1, "we can test this recording stuff. ", 678.54, 680.31], [1, "like. ", 680.79, 681.08], [1, "seventy in. ", 681.74, 682.57], [2, "on. ", 686.1, 709.08], [4, "today. ", 686.42, 760.98], [2, "or download the meeting everyone to stop and look at the same time roughly I guess it doesn't matter it mostly matters if we all start at the same time. ", 688.11, 694.91], [1, "right. ", 689.0, 702.01], [2, "%HESITATION and then let's all put it up on the drive in will make like a. ", 695.44, 698.27], [2, "data folder on Dr and we can mark this is meeting one %HESITATION and then I think like every Friday we should do this. ", 698.8, 706.19], [1, "okay. ", 701.51, 708.73], [2, "and will cumulated over time. ", 706.83, 709.08], [1, "I especially this is gonna be like a. ", 707.07, 708.73], [1, "Silas consent. ", 710.29, 711.37], [3, "this is. ", 714.83, 715.28], [2, "and especially. ", 715.03, 716.09], [2, "a guide. ", 716.7, 717.2], [3, "%HESITATION it's gonna take a really long time Kerr. ", 717.55, 720.06], [1, "yeah. ", 719.29, 755.38], [3, "get. ", 720.94, 766.14], [2, "it's gonna take like twelve minutes yeah. ", 720.99, 722.93], [2, "%HESITATION but luckily I have to do it once or. ", 723.89, 727.34], [2, "yeah %HESITATION but once we've %HESITATION migrate towards the one stream for everyone if we do choose that route later on. ", 727.91, 736.02], [2, "then we can start recording our sprints in person which will be kind of cool. ", 736.67, 741.27], [2, "%HESITATION but I think this will be a good start so at least we have some data. ", 741.89, 745.13], [2, "we'll be really nice %HESITATION I don't have anything else from my side I don't know if anyone has any more questions. ", 745.97, 751.19], [1, "I just had to like forty eight four nine eight in our shared folder. ", 751.65, 755.38], [1, "cool. ", 757.19, 761.31], [2, "great. ", 758.65, 763.8], [1, "see you on Monday I lecture again. ", 758.87, 761.31], [4, "get. ", 760.72, 768.09], [2, "yeah. ", 763.3, 765.95], [2, "we have collection on Monday. ", 764.64, 765.95], [4, "all right stop recorder whenever masses that record. ", 765.07, 768.09], [4, "%HESITATION. ", 765.72, 52.86], [2, "all right one two three stop recording. ", 768.02, 771.53]]
    #demoInput2 = [[2, "all right so. ", 4.38, 5.64], [1, "Max you can start. ", 5.61, 6.83]]
    demoInput1 = [["Tuan2", "yes %HESITATION Starscream. ", 1.65, 3.93], ["Christina1", "I worked on the front end to display simple homepage. ", 4.29, 6.83], ["Tuan2", "what have you were done. ", 8.14, 9.13], ["Christina1", "I will be working on setting up a container platform to manager application. ", 10.74, 14.75], ["Tuan2", "but will you be doing next. ", 13.22, 14.71], ["Christina1", "action item set up a container platform to manage application. ", 15.26, 18.55], ["Christina1", "what about you. ", 19.57, 20.32], ["Tuan2", "I do some diagrams for our product requirements document. ", 26.91, 30.65], ["Tuan2", "and now I will be working on hosting the application the clout action item prepare to host application in the %HESITATION clout. ", 31.34, 38.82], ["Tuan2", "all right see you tomorrow. ", 40.46, 41.48]]
    # Processing Object
    tp = TextProcessor(demoInput1)
    print("*****************************************************\n")
    print("Summary: ***** \n")
    print(tp.summarize())
    print("Question List: \n")
    print(tp.getQuestionList())
    print("Action Items: \n")
    print(tp.getActionItems())
    print("RAW TRANSCRIPTION: \n")
    print(tp.raw_data)
    print("HESITATIONS: \n")
    print(tp.analyzeHesitations())
    print("TIME SPOKEN: \n")
    print(tp.timeSpoken())
    #print(tp.tfidf())
    #tp.tfidfFormat()
    print("KEYWORDS: \n")
    print(tp.get_keywords())
    print("*****************************************************\n")
