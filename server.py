import socket
import struct
import sys
import threading
import random
import uuid
import time
from protocol import TcpProtocol

class User:
    def __init__(self, user_name: str = "", ip_address: str = "", token: str = "",) -> None:
        self.user_name = user_name
        self.ip_address = ip_address
        self.token = token
        self.start_time = sys.float_info.max

    def set_time(self, time) -> None:
        self.start_time = time


class Room:
    def __init__(self, host_token: str = "", room_name: str = "", password: str = "") -> None:
        self.host_token = host_token
        self.password = password
        self.room_name = room_name
        self.members: list[User] = []

    def set_member(self, member: User) -> None:
        self.members.append(member)

class RoomList:
    rooms: list[Room] = []

class TcpServer:
    def __init__(self) -> None:
        self.socket : socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address: str = "0.0.0.0"
        self.server_port: int = 8000
        self.buffer: int = 32
        self.connection = None

        self.room_name_lenth: int = 1
        self.operation: int = 1
        self.state: int = 0
        self.room_name: str = ""
        self.user_name: str = ""
        self.password: str = ""
        self.token: str = ""

        self.room_list = RoomList.rooms

        self.socket.bind((self.server_address, self.server_port))
        self.socket.listen(1)

    def init(self) -> None:
        self.room_name_lenth: int = 1
        self.operation: int = 1
        self.state: int = 0
        self.room_name: str = ""
        self.user_name: str = ""
        self.token: str = ""

    def get_header_info(self, header) -> None:
        self.room_name_length = TcpProtocol.get_room_name_length(header)
        self.operation = TcpProtocol.get_operation(header)
        self.state = TcpProtocol.get_state(header)
        self.room_name = TcpProtocol.get_room_name(header)
        self.user_name = TcpProtocol.get_user_name(header)
        self.password = TcpProtocol.get_password(header)

    def create_room(self, connection) -> None:
        self.state = 1

        connection.send(TcpProtocol.set_header(
            self.room_name_length,
            self.operation,
            self.state,
            self.room_name,
            self.user_name,
            self.password
        ))

        # tokenの発行
        self.token = str(uuid.uuid4())

        # roomを作成
        host_user = User(self.user_name, socket.inet_ntoa(struct.pack('>I', random.randrange(0x7F000001, 0x7FFFFFFE))), self.token)
        
        room = Room(self.token, self.password, self.room_name)
        room.set_member(host_user)
        self.room_list.append(room)

        self.state = 2

        connection.send(TcpProtocol.set_header(
            self.room_name_length,
            self.operation,
            self.state,
            self.room_name,
            self.user_name,
            self.password
        ))

    def join_room(self, connection) -> None:
        self.state = 1

        connection.send(TcpProtocol.set_header(
            self.room_name_length,
            self.operation,
            self.state,
            self.room_name,
            self.user_name,
            self.password
        ))

        # tokenの発行
        self.token = str(uuid.uuid4())
        
        member_user = User(self.user_name, socket.inet_ntoa(struct.pack('>I', random.randrange(0x7F000001, 0x7FFFFFFE))), self.token)

        for room in self.room_list:
            if self.room_name == room.room_name and self.password == room.password:
                room.set_member(member_user)



    def connect(self) -> None:
        try:
            connection, client_addr = self.socket.accept()
            
            while True:
                print("TCP: Connection from {}".format(client_addr))
                self.get_header_info(connection.recv(self.buffer))
        finally:
            self.close()


    def close(self) -> None:
        print("Closing current connection")
        self.socket.close()

