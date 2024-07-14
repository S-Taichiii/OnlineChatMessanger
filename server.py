import socket
import struct
import sys
import threading
import random
import uuid
import time
from protocol import TCPR

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
        self.operation: int = 1
        self.state: int = 0
        self.room_name: str = ""
        self.user_name: str = ""
        self.token: str = ""

    def get_header_info(self, header) -> None:
        self.operation = TCPR.get_operation(header)
        self.state = TCPR.get_state(header)
        self.room_name, self.user_name, self.password = TCPR.get_payload(header)

    def create_room(self, connection) -> None:
        self.state = 1

        connection.send(TCPR.set_header(
            len(self.room_name),
            self.operation,
            self.state,
            len(self.user_name),
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

        connection.send(TCPR.set_header(
            len(self.room_name),
            self.operation,
            self.state,
            len(self.user_name),
            self.room_name,
            self.user_name,
            self.password
        ))
        
        connection.send(host_user.ip_address.encode('utf-8'))


    def join_room(self, connection) -> None:
        # status code 
        # 0: success
        # 1: failed not exist room_name
        # 2: failed incorrect password

        send_code: str = "1"

        for room in self.room_list:
            if room.room_name == self.room_name and room.password == self.password:
                send_code = "0"

                # tokenの発行
                self.token = str(uuid.uuid4())

                # join the room
                member_user = User(self.user_name, socket.inet_ntoa(struct.pack('>I', random.randrange(0x7F000001, 0x7FFFFFFE))), self.token)
                room.set_member(member_user)
                connection.send(member_user.ip_address)
            elif self.room_name != room.room_name:
                continue
            elif self.password != room.password:
                send_code = "2"

        connection.send(send_code.encode("utf-8"))

    def connect(self) -> None:
        while True:
            connection, client_addr = self.socket.accept()
            
            try:
                print("[TCP]: Connection from {}".format(client_addr))
                self.get_header_info(connection.recv(self.buffer))
                
                if self.operation == 1:
                    self.create_room(connection)
                elif self.operation == 2:
                    self.join_room(connection)

                self.init()

            except Exception as e:
                print("[TCP]Error: ", str(e))
            finally:
                self.close()


    def close(self) -> None:
        print("[TCP]Closing current connection\n")
        self.socket.close()

