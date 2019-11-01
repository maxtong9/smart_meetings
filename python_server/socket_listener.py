#Socket Connection as well as Python access to S3
import socketserver
from s3_access import download_file_from_S3

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        # print("{} wrote:".format(self.client_address[0]))
        # print(self.data)

        download_file_from_S3("smartmeetingsbelieving", "downloaded.txt", self.data)
        # CALL TEXT_ANALYZER FUNCTIONS HERE
        toSend = b'Some key'
        self.request.sendall(toSend)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
