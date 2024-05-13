import socket
import threading

class UdpClient:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = '0.0.0.0'
        self.server_port = 9001
        self.buffer = 4096

        # self.socket.bind((self.client_address, self.client_port))

    def send(self):
        try:
            while True:
                message = input("please input message ---> ")
                print()

                self.socket.sendto(message.encode('utf-8'), (self.server_address, self.server_port))
        finally:
            print("closing socket")
            self.socket.close()

    def receive(self):
        while True:
            recv_data, _ = self.socket.recvfrom(self.buffer)
            print("accepted data: {}".format(recv_data.decode('utf-8')))

    def start_chat(self):
        thread_receive = threading.Thread(target=self.receive)
        thread_receive.start()
        self.send()


if __name__ == "__main__":
    udp_client = UdpClient()
    udp_client.start_chat()
            