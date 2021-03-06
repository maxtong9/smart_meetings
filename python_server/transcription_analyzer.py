from transcribe import *
from text_processor import *
import json
from tfidf_model import tokenize
'''
Main Class for dealing with Meeting Transcriptions

Input is a cumulative collection of audio files

Output is a formattable json file (or just json) that can be used to upload to S3, send over websocket, etc.

USE: Load audio files individually or as a list {___.loadAudio(...)} then call {___.run()}
'''
class TranscriptionAnalyzer:
    def __init__(self, name):
        self.message = "Hello, World"
        # Dictionary of audio files associated by the names
        self.audioFiles = []
        self.nameList = []
        self.meeting = name
        self.transcribe = None #Transcribe(["Sarita.wav", "Christina.wav"])
        self.transcription = None
        self.interruption = None

        self.text_analyzer = None

        self.analyzer_output = {}

        self.output = None


    # Loads an audio file associated with the name into the object
    def loadAudio(self, name, audioFile):
        self.audioFiles.append(audioFile)
        self.nameList = name

    # Fetches the transcription from the given audio files
    def transcribeAudio(self):
        if self.audioFiles == None:
            print("Error: No Audio Files are loaded")
            return -1

        self.transcribe = Transcribe(self.audioFiles, self.nameList)
        self.transcription = self.transcribe.transcription_with_recognition()
        self.interruption = self.transcribe.overlap()
        self.time = self.transcribe.time()
        # print(self.transcription)

     # Analyzes the text
    def analyze(self):
        # print(self.transcription)
        if self.transcription == None:
            print("Error: Transcription is not available")
            return -1

        self.text_analyzer = TextProcessor(self.transcription)

        self.analyzer_output["summary"] = self.text_analyzer.summarize()
        self.analyzer_output["questions"] = self.text_analyzer.getQuestionList()
        self.analyzer_output["action_items"] = self.text_analyzer.getActionItems()
        self.analyzer_output["hesitation_analytics"] = self.text_analyzer.analyzeHesitations()
        self.analyzer_output["interruption"] = self.interruption
        self.analyzer_output["total_time_spoken"] = self.text_analyzer.timeSpoken()
        self.analyzer_output["keywords"] = self.text_analyzer.get_keywords()
        self.analyzer_output["raw"] = self.text_analyzer.raw_data
        self.analyzer_output["meeting_time"] = self.time
        self.output = json.dumps(self.analyzer_output)
        self.analyzer_output["meeting_suggestions"] = self.text_analyzer.getMeetingSuggestions(self.analyzer_output)

        with open('./tmp/' + self.meeting + '.json', 'w') as outfile:
            json.dump(self.analyzer_output, outfile)

    # Runs all of the necessary functions.
    # Called from the socket program after loading the audio files
    def run(self):
        # print("In TA.run()")
        if self.transcribeAudio() == -1:
            print("Error: No audio files are loaded")
        if self.analyze() == -1:
           print("Error: Transcription is not available")

        if self.output == None:
            print("Error: No output available")

        # print("****JSON*****")
        # print(self.output)

        # print("Done with TA.run()")
        return self.output


if __name__ == "__main__":
    # move audio files to frontmost python_server directory
   TA = TranscriptionAnalyzer("fakekey")
   TA.loadAudio('Christina', 'Christina.mp3')
   TA.loadAudio('Jackson', 'Jackson.mp3')
#    TA.loadAudio('Max', 'Max.mp3')
#    TA.loadAudio('Sarita', 'Sarita.mp3')
#    TA.loadAudio('Tuan', 'Tuan.mp3')
# #    TA.load()
#    TA.load()
#    TA.load()
#    TA.load()
   print(TA.run())
