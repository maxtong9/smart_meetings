
'''
Main Class for dealing with Meeting Transcriptions

Input is a cumulative collection of audio files

Output is a formattable json file (or just json) that can be used to upload to S3, send over websocket, etc.
'''
class TranscriptionAnalyzer:
    def __init__(self):
        self.message = "Hello, World"
        # Dictionary of audio files associated by the names
        self.audioFiles = {}

    def run(self):
        print(self.message)

    # Loads an audio file associated with the name into the object
    def loadAudio(self, name, audioFile):
        self.audioFiles[name] = audioFile
    
    


        




if __name__ == '__main__':
    TA = TranscriptionAnalyzer()
    TA.run()
    
