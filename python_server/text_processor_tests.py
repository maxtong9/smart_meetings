# from transcribe import *
from text_processor import *

'''
Test Data:
* [["Tuan2", "yes %HESITATION Starscream. ", 1.65, 3.93], ["Christina1", "I worked on the front end to display simple homepage. ", 4.29, 6.83], ["Tuan2", "what have you were done. ", 8.14, 9.13], ["Christina1", "I will be working on setting up a container platform to manager application. ", 10.74, 14.75], ["Tuan2", "but will you be doing next. ", 13.22, 14.71], ["Christina1", "action item set up a container platform to manage application. ", 15.26, 18.55], ["Christina1", "what about you. ", 19.57, 20.32], ["Tuan2", "I do some diagrams for our product requirements document. ", 26.91, 30.65], ["Tuan2", "and now I will be working on hosting the application the clout action item prepare to host application in the %HESITATION clout. ", 31.34, 38.82], ["Tuan2", "all right see you tomorrow. ", 40.46, 41.48]]
* 
'''

class TextProcessorTests:
    def __init__(self, testRawData):
        print("hello, world")

        self.passTest = "*** Passed ***"
        self.failTest = "*** Failed ***"

        self.totalTestNum = 0
        self.testsPassed = 0
        self.data = testRawData


    def new_tp_object(self):
        return TextProcessor(self.data)


    # Prints Test ID Passed
    def passTestPrint(self, id):
        print(id, self.passTest, '\n')

    # Prints Test ID Failed
    def failTestPrint(self, id):
        print(id, self.failTest, '\n')


    # Tests the sentence List
    def test1(self):
        print("Test 1")
        tp = self.new_tp_object()
        if tp.sentenceList == ['yes %HESITATION Starscream. ', 'I worked on the front end to display simple homepage. ', 'what have you were done. ', 'I will be working on setting up a container platform to manager application. ', 'but will you be doing next. ', 'action item set up a container platform to manage application. ', 'what about you. ', 'I do some diagrams for our product requirements document. ', 'and now I will be working on hosting the application the clout action item prepare to host application in the %HESITATION clout. ', 'all right see you tomorrow. ']:
            self.passTestPrint(1)
        else:
            self.failTestPrint(1)

    # Tests for removed hesitations
    def test2(self):
        tp = self.new_tp_object()
        newList = tp.removeHesitationFromList(tp.sentenceList)
        for sentence in newList:
            if sentence.count('%HESITATION'):
                self.failTestPrint(2)
                return
        self.passTestPrint(2)


    # Tests for removal of stopwords
    def test3(self):
        tp = self.new_tp_object()
        if tp.removeStopWords(tp.sentenceList) == [['yes', '%', 'HESITATION', 'Starscream', '.'], ['worked', 'front', 'end', 'display', 'simple', 'homepage', '.'], ['done', '.'], ['working', 'setting', 'container', 'platform', 'manager', 'application', '.'], ['next', '.'], ['action', 'item', 'set', 'container', 'platform', 'manage', 'application', '.'], ['.'], ['diagrams', 'product', 'requirements', 'document', '.'], ['working', 'hosting', 'application', 'clout', 'action', 'item', 'prepare', 'host', 'application', '%', 'HESITATION', 'clout', '.'], ['right', 'see', 'tomorrow', '.']]:
            self.passTestPrint(3)
        else:
            self.failTestPrint(3)

    # Tests getActionItems
    def test4(self):
        tp = self.new_tp_object()
        if tp.getActionItems() == [['Christina', 'set up a container platform to manage application..'], ['Tuan', 'prepare to host application in the  clout..']]:
            self.passTestPrint(4)
        else:
            self.failTestPrint(4)

    # Tests getQuestionList    
    def test5(self):
        tp = self.new_tp_object()
        if tp.getQuestionList() == [['Tuan', 'what have you were done. '], ['Christina', 'what about you. ']]:
            self.passTestPrint(5)
        else:
            self.failTestPrint(5)



    def run_tests(self):
        print("Running Tests...")
        print(self.data)
        self.test1()
        self.test2()
        self.test3()
        self.test4()
        self.test5()














if __name__ == "__main__":
    tpt = TextProcessorTests([["Tuan2", "yes %HESITATION Starscream. ", 1.65, 3.93], ["Christina1", "I worked on the front end to display simple homepage. ", 4.29, 6.83], ["Tuan2", "what have you were done. ", 8.14, 9.13], ["Christina1", "I will be working on setting up a container platform to manager application. ", 10.74, 14.75], ["Tuan2", "but will you be doing next. ", 13.22, 14.71], ["Christina1", "action item set up a container platform to manage application. ", 15.26, 18.55], ["Christina1", "what about you. ", 19.57, 20.32], ["Tuan2", "I do some diagrams for our product requirements document. ", 26.91, 30.65], ["Tuan2", "and now I will be working on hosting the application the clout action item prepare to host application in the %HESITATION clout. ", 31.34, 38.82], ["Tuan2", "all right see you tomorrow. ", 40.46, 41.48]])

    tpt.run_tests()

    # runTests();
    