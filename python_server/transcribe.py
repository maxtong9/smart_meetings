'''
This class contains audio to text processing

Input: Audio files from S3
Output: Create a json file with the transcription and returns a string.
'''

import os
import numpy as np
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ApiException
import json
from settings import *

class Transcribe:
	def __init__(self, input_audio):
		self.audio = input_audio

	def transcription(self):
		''' Returns transcription of the inputed audio files '''
		authenticator = IAMAuthenticator(WATSON_API_KEY)
		speech_to_text = SpeechToTextV1(authenticator=authenticator)
		speech_to_text.set_service_url(SERVICE_URL)

		transcription = open("transcription.txt" , "w")
		results = []
		#Iterating through all inputted files
		for item in self.audio:
			file = open(item, "rb")
			#API CAlL
			response = speech_to_text.recognize(file, content_type="audio/wav", smart_formatting=True, timestamps=True, inactivity_timeout=90)
			results.append(response.get_result());

		phrase = []
		t_string = ""
		t_start = 0
		temp = []

		# Obtain the timestamps of each word to include periods.
		for speaker, item in enumerate(results):
			for i in item['results']:
				for j in i['alternatives']:
					for index, word in enumerate(j['timestamps']):
						#Take into account seperation in transcript from Watson IBM
						if index == 0:
							if temp:
								if (word[1])-(temp[1][2]) < 0.45:
									t_string += " " + str(word[0])
								else:
									t_string += ". "
									phrase.append([speaker, t_string, t_start, temp[1][2]])
									t_string = ""
									t_start = word[1]
									t_string += str(word[0])
									temp = []
								continue
							t_string += word[0]
							t_start = word[1]
						# The amount of time to determine when a period is placed is decided here. 
						elif (word[1])-(j['timestamps'][index-1][2]) < 0.45:
							t_string += " " + str(word[0])
							if index == len(j['timestamps'])-1:
								if len(results) == 1:
									phrase.append([speaker, t_string, t_start, word[2]])
									t_string = ""
									continue
								temp = [index, word];
						else:
							t_string += ". "
							phrase.append([speaker, t_string, t_start, j['timestamps'][index-1][2]])
							t_string = ""
							t_start = word[1]
							t_string += str(word[0])

		#Sort the phrases from all the audio transcriptions in chronological order
		phrase.sort(key = lambda x: x[2])
		print(phrase)
		s = ""

		#Format output
		for index, sentence in enumerate(phrase):
			if index == 0:
				s = "Person " + str(sentence[0]+1) + ": "
				s += str(sentence[1])
			elif (sentence[0] == phrase[index-1][0]):
				s += str(sentence[1])
			else:
				s += "\n" + "Person " + str(sentence[0]+1) + ": "
				s += str(sentence[1])

		#Write transcript to file
		transcription.write(s)
		transcription.close()
		return phrase


if __name__ == "__main__":
	t = Transcribe(["Recording.wav"])
	t.transcription()
