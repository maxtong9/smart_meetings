#Socket Connection as well as Python access to S3
import socketserver
import json
from transcription_analyzer import TranscriptionAnalyzer
from s3_access.s3_access import download_file_from_S3, upload_file_to_S3

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client

        self.data = self.request.recv(1024)
        print(self.data.decode())
        amount = int(self.data.decode()[0])
        meeting_name = self.data.decode("utf-8")[1:len(self.data.decode())]
        TA = TranscriptionAnalyzer(meeting_name)

        #Receive files one by one
        self.data = self.request.recv(1024)
        info_string = self.data.decode("utf-8")
        info_list = info_string.split('|')
        for i in range(1, amount + 1):
            key = info_list[i].split(';')[0]
            filename = info_list[i].split(';')[1]
            print("Received file: ", filename)
            download_file_from_S3("smartmeetingsbelieving", filename, key)
            TA.loadAudio(filename.split('.')[0] + str(i), "./tmp/" + filename)

        TA.run()
        upload_file_to_S3("smartmeetingsbelieving", "./tmp/" + meeting_name + ".json", meeting_name + ".json")
        key = meeting_name + ".json"
        self.request.sendall(str.encode(key))

if __name__ == "__main__":
    # HOST, PORT = "localhost", 9999 # COMMENT THIS OUT FOR DOCKER
    HOST, PORT = "0.0.0.0", 9999 # UNCOMMENT THIS FOR DOCKER

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
