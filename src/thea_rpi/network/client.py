import socket, struct
from thea_rpi.config import SERVER_IP, PORT


def start_connection() -> socket.socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, PORT))
    print(f"CONNECTED TO {SERVER_IP}")
    return s


def close_connection(s : socket.socket) -> None:
    print("CONNECTION CLOSED")
    s.close()


def send_data(s : socket.socket, data : bytes) -> None:
    try:
        length = len(data)
        header = struct.pack(">I", length)
        
        s.sendall(header + data)
        print("DATA SENT SUCCESSFULLY")

    except Exception as e:
        print(f"ERROR: {e}")


def send_text(s : socket.socket, text : str) -> None:
    message = text.encode()
    send_data(s, message)


if __name__ == "__main__":
    s = start_connection()
    message = "Hello, World!"
    send_text(s, message)
    close_connection(s)
