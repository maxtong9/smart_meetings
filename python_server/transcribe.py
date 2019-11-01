#https://cloud.ibm.com/apidocs/speech-to-text/speech-to-text?code=python
#https://stackoverflow.com/questions/419163/what-does-if-name-main-do

import os
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ApiException
import json
from settings import *

class Transcribe:
	def __init__(self, input_audio):
		self.audio = input_audio

	def transcription(self):
		authenticator = IAMAuthenticator(WATSON_API_KEY)
		speech_to_text = SpeechToTextV1(authenticator=authenticator)
		speech_to_text.set_service_url(SERVICE_URL)

		transcription = open("example_transcription_output/transcription.txt" , "w")
		# path = '/Users/SaritaP/Desktop/speech_to_text/audio_files'
		# files = os.listdir(path);

		audio = open(self.audio, "rb")
		#API CAll
		response = str(speech_to_text.recognize(audio, content_type="audio/flac", smart_formatting=True))

		# Extract the transcript from DetailedResponse type which includes headers.
		split = response.split('\n')
		for line in split:
			if "transcript" in line:
				index = line.find("transcript")					
				transcription.write(line[index+14:-2])


		transcription.close()



# for filename in os.listdir(path):
	# 	if filename.endswith('.flac'):
	# 		audio = open(os.path.join(path,filename), 'rb')
	# 		response = speech_to_text.recognize(audio, content_type="audio/flac", smart_formatting=True)
	# 		response_str = str(response)
	# 		print(response_str)
	# 		split = response_str.split('\n')
	# 		for line in split:
	# 			if "transcript" in line:
	# 				index = line.find("transcript")
	# 				transcript.write(filename + ": " + line[index+14:-2] + "\n")
