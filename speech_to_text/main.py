from transcribe import *

def main():
	T = Transcribe("audio-file.flac")
	T.transcription()

if __name__ == "__main__":
	main()