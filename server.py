import socket

class UdpServer:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.buffer = 4096
        self.server_address = '0.0.0.0'
        self.server_port = 9001
        self.clients = {}

        print('stratig up on {}'.format(self.server_port))

        self.socket.bind((self.server_address, self.server_port))

    def connect(self):
        while True:
            try:
                print("\nwating to receive message")
                data, client_address = self.socket.recvfrom(self.buffer)

                if client_address not in self.clients.keys():
                    self.clients[client_address] = True
                    print('New Client connected: {}'.format(client_address))
                
                print("Received data: {}".format(data.decode('utf-8')))

                self.send(data)

            except Exception as e:
                print("Error: " + e)

    def send(self, data):
        for addr in self.clients.keys():
            self.socket.sendto(data, addr)
    
        


if __name__ == "__main__":
    udp_server = UdpServer()
    udp_server.connect()