import socket
import threading
import sys
import os

HOST = '127.0.0.1'
PORT = 55555


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                os._exit(0)
            print(message)
        except ConnectionAbortedError:
            os._exit(0)
        except ConnectionResetError:
            os._exit(0)
        except Exception:
            os._exit(0)


def write_messages(client_socket, nickname):
    while True:
        try:
            message = input('')
            client_socket.send(message.encode('utf-8'))
        except EOFError:
            break
        except KeyboardInterrupt:
            break
        except Exception:
            break


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    nickname = input("Choose your nickname: ").strip()
    if not nickname:
        sys.exit(1)

    try:
        client.connect((HOST, PORT))
        client.send(nickname.encode('utf-8'))

        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.daemon = True
        receive_thread.start()

        write_messages(client, nickname)

    except ConnectionRefusedError:
        pass
    except socket.gaierror:
        pass
    except Exception:
        pass
    finally:
        client.close()
        sys.exit(0)


if __name__ == "__main__":
    start_client()
