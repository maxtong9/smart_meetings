'''
This File will hold all of the API related text processor functions 
'''

'''
This class is the main text processing class

Input: String Transcription of the data
Output: Text processing Functions (TBD)
'''
class TextProcessor:
    def __init__(self, textString):
        self.transcription = textString


    def printTranscription(self):
        print(self.transcription)