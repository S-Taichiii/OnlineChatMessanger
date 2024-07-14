from typing import Tuple

class TCPR:
    @staticmethod
    def set_header(room_name_size: int,
                   operation: int,
                   state: int,
                   user_name_size: int,
                   room_name: str,
                   user_name: str,
                   password: str) -> bytes:

        return room_name_size.to_bytes(1, "big") + operation.to_bytes(1, "big") + state.to_bytes(1, "big") + user_name_size.to_bytes(1, "big") + room_name.encode("utf-8") + user_name.encode("utg-8") + password.encode("utf-8")


    @staticmethod
    def get_operation(header) -> int:
        return header[1]
    
    @staticmethod
    def get_state(header) -> int:
        return header[2]

    @staticmethod
    def get_user_name_length(header) -> int:
        return header[3]

    @staticmethod
    def get_payload(header) -> Tuple[str, str, str]:
        room_name_size = header[0]
        room_name_end_index: int = 4 + room_name_size
        user_name_end_index: int = room_name_end_index + TCPR.get_user_name_length(header)

        return header[4: room_name_end_index], header[room_name_end_index, user_name_end_index], header[user_name_end_index:]
        

