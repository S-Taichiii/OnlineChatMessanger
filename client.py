import socket
import sys
from protocol import TCPR


class validator:
    @staticmethod
    def check_room_name(room_name):
        pass

    @staticmethod
    def check_user_name(user_name):
        pass

    @staticmethod
    def check_password(password):
        pass


class TcpClient:
    def __init__(self) -> None:
        self.socket : socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address: str = "0.0.0.0"
        self.server_port: int = 8000
        self.buffer: int = 32


