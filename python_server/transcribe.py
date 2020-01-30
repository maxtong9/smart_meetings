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
	def __init__(self, input_audio, nameList):
		self.audio = input_audio
		self.nameList = nameList
		self.phrase = None

	def transcription(self):
		''' Returns transcription of the inputed audio files '''
		authenticator = IAMAuthenticator(WATSON_API_KEY)
		speech_to_text = SpeechToTextV1(authenticator=authenticator)
		speech_to_text.set_service_url(SERVICE_URL)

		results = []
		#Iterating through all inputted files
		for item in self.audio:
			file_type = "audio/flac"
			if ".wav" in item:
				file_type = "audio/wav"
			elif ".mpeg" in item:
				file_type = "audio/mpeg"
			elif ".mp3" in item:
				file_type = "audio/mp3"
			file = open(item, "rb")
			#API CAlL
			response = speech_to_text.recognize(file, content_type=file_type, smart_formatting=True, timestamps=True, inactivity_timeout=90)
			results.append(response.get_result());

		phrase = []
		t_string = ""
		t_start = 0
		temp = []

		# Obtain the timestamps of each word to include periods.
		for speaker, item in enumerate(results):
			temp = []
			for r_index, i in enumerate(item['results']):
				for j in i['alternatives']:
					for index, word in enumerate(j['timestamps']):
						#Take into account seperation in transcript from Watson IBM
						if index == 0:
							if temp:
								if (word[1])-(temp[1][2]) < 0.45:
									t_string += " " + str(word[0])
								else:
									t_string += ". "
									phrase.append([self.nameList[speaker], t_string, t_start, temp[1][2]])
									t_string = ""
									t_start = word[1]
									t_string += str(word[0])
									temp = []
								continue
							if t_string:
								t_string += ". "
								phrase.append([self.nameList[speaker], t_string, t_start, j['timestamps'][index-1][2]])
								t_string = ""
								t_start = word[1]
								t_string += str(word[0])
								continue
							t_string += word[0]
							t_start = word[1]
						# The amount of time to determine when a period is placed is decided here.
						elif (word[1])-(j['timestamps'][index-1][2]) < 0.45:
							t_string += " " + str(word[0])
							if index == len(j['timestamps'])-1:
								if (len(results) == 1) or (r_index == len(item['results'])-1):
									t_string += ". "
									phrase.append([self.nameList[speaker], t_string, t_start, word[2]])
									t_string = ""
								else:
									temp = [index, word, self.nameList[speaker]];
						else:
							t_string += ". "
							phrase.append([self.nameList[speaker], t_string, t_start, j['timestamps'][index-1][2]])
							t_string = ""
							t_start = word[1]
							t_string += str(word[0])

		if temp:
			t_string += ". "
			phrase.append([temp[2], t_string, t_start, temp[1][2]])

		#Sort the phrases from all the audio transcriptions in chronological order
		phrase.sort(key = lambda x: x[2])
		self.phrase = phrase
		return phrase

	def text(self):
		''' Returns json format of transcript '''
		data = {}
		s = ""
		#Format output
		for index, sentence in enumerate(self.phrase):
			if index == 0:
				s = "Person " + str(sentence[0]+1) + ": "
				s += str(sentence[1])
			elif (sentence[0] == self.phrase[index-1][0]):
				s += str(sentence[1])
			else:
				s += "\n" + "Person " + str(sentence[0]+1) + ": "
				s += str(sentence[1])

		data['text'] = s
		with open('transcription.json', 'w') as outfile:
			json.dump(data, outfile)

	def overlap(self):
		s_time = 0
		e_time = 0
		name = ''
		overlap = {}
		for index, comp in enumerate(self.phrase):
			if index == 0:
				name = comp[0]
				s_time = comp[2]
				e_time = comp[3]
			else:
				if name != comp[0]:
					if comp[2] > s_time and comp[2] < e_time:
						if comp[0] not in overlap:
							overlap[comp[0]] = 1
						else:
							overlap[comp[0]] += 1
					s_time = comp[2]
					e_time = comp[3]
					name = comp[0]
		interruption = []
		for i in overlap:
			# interruption.append([i[:-1], overlap[i]])
			interruption.append([i, overlap[i]])

		return interruption



# if __name__ == "__main__":
# 	t = Transcribe(["Recording.wav"])
# 	t.transcription()
