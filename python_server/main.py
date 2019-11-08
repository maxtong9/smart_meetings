#Socket Connection as well as Python access to S3
import socketserver
import json
from transcription_analyzer import TranscriptionAnalyzer
from s3_access.s3_access import download_file_from_S3, upload_file_to_S3

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)

        download_file_from_S3("smartmeetingsbelieving", "Recording.wav", self.data.decode("utf-8"))
        TA = TranscriptionAnalyzer()
        TA.loadAudio("Jackson", "./tmp/Recording.wav")
        TA.run()
        upload_file_to_S3("smartmeetingsbelieving", "./tmp/results.json", "results.json")
        toSend = b'results.json'
        self.request.sendall(toSend)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
