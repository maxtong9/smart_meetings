from transcribe import *
from text_processor import *
'''
Main Class for dealing with Meeting Transcriptions

Input is a cumulative collection of audio files

Output is a formattable json file (or just json) that can be used to upload to S3, send over websocket, etc.

USE: Load audio files individually or as a list {___.loadAudio(...)} then call {___.run()}
'''
class TranscriptionAnalyzer:
    def __init__(self):
        self.message = "Hello, World"
        # Dictionary of audio files associated by the names
        self.audioFiles = {}

        self.transcribe = None Transcribe(["Sarita.wav", "Christina.wav"])
        self.transcription = None
        self.text_analyzer = None


    # Loads an audio file associated with the name into the object
    def loadAudio(self, name, audioFile):
        self.audioFiles[name] = audioFile

    # Fetches the transcription from the given audio files
    def transcribe(self):
        if self.audioFiles = None:
            print("Error: No Audio Files are loaded")
            return -1

        self.transcribe = Transcribe(self.audioFiles)
        self.transcription = self.transcribe.transcription

     # Analyzes the text
    def analyze(self):
        if self.transcription = None:
            print("Error: Transcription is not available")
            return -1
        self.text_analyzer = TextProcessor(self.transcription))


    # Runs all of the necessary functions. 
    # Called from the socket program after loading the audio files
    def run(self):
        if self.transcribe() == -1:
            print("Error: No audio files are loaded")
            
       if self.analyze() == -1:
           print("Error: Transcription is not available")

        
        

   

        





    
    


        




if __name__ == '__main__':
    TA = TranscriptionAnalyzer()
    TA.run()
    
