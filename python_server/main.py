from transcribe import *
# from text_processor import *
def main():
	# Transcribe Audio
	T = Transcribe("example_audio/audio-file.flac")
	T.transcription()
	# Used Audio in Text Processor
	# tp = TextProcessor("Hello, Input")
	# tp.summarize()
if __name__ == "__main__":
	main()