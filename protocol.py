class TcpProtocol:
    @staticmethod
    def set_header(room_name_size: int,
                   operation: int,
                   state: int,
                   room_name: str,
                   user_name: str,
                   password: str) -> bytes:
        room_name = TcpProtocol.fill_space(room_name, room_name.encode('utf-8'), 8)
        user_name = TcpProtocol.fill_space(user_name, user_name.encode('utf-8'), 10)
        password = TcpProtocol.fill_space(password, password.encode('utf-8'), 11)

        return room_name_size.to_bytes(1, "big") + operation.to_bytes(1, "big") + state.to_bytes(1, "big") + room_name.encode("utf-8") + user_name.encode("utg-8") + password.encode("utf-8")

    @staticmethod
    def fill_space(res: str, str_byte: bytes, num: int):
        return res.ljust(num, " ") if len(str_byte) < num else res

    @staticmethod
    def get_room_name_length(header) -> int:
        return header[0]

    @staticmethod
    def get_operation(header) -> int:
        return header[1]
    
    @staticmethod
    def get_state(header) -> int:
        return header[2]

    @staticmethod
    def get_room_name(header) -> str:
        return header[3: 11].decode("utf-8").replace(" ", "")

    @staticmethod
    def get_user_name(header) -> str:
        return header[11: 21].decode("utf-8").replace(" ", "")

    @staticmethod
    def get_password(header) -> str:
        return header[21:].decode("utf-8").replace(" ", "")

if __name__ == '__main__':
    print()
