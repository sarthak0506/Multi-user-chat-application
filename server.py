import socket
import threading
import sys
import os

HOST = '0.0.0.0'
PORT = 55555

clients = []
nicknames = []
admin_nicknames = ["admin", "moderator"]
client_lock = threading.Lock()


def broadcast(message, _client=None):
    with client_lock:
        for client in clients:
            if client != _client:
                try:
                    client.send(message)
                except socket.error:
                    remove_client(client)


def remove_client(client_socket):
    with client_lock:
        if client_socket in clients:
            index = clients.index(client_socket)
            nickname = nicknames[index]
            clients.remove(client_socket)
            nicknames.remove(nickname)
            client_socket.close()
            broadcast(f"{nickname} left the chat.".encode('utf-8'))


def handle_client(client_socket, address):
    nickname = None
    try:
        nickname = client_socket.recv(1024).decode('utf-8')

        with client_lock:
            if nickname in nicknames:
                client_socket.send("Nickname already taken. Please try again with a different name.".encode('utf-8'))
                client_socket.close()
                return
            nicknames.append(nickname)
            clients.append(client_socket)

        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        client_socket.send("Connected to the chat server!".encode('utf-8'))

        while True:
            try:
                message = client_socket.recv(1024)
                if not message:
                    break

                decoded_message = message.decode('utf-8')

                if decoded_message.startswith('/'):
                    parts = decoded_message.split(' ', 1)
                    command = parts[0].strip().lower()

                    if command == '/kick':
                        if nickname in admin_nicknames:
                            if len(parts) > 1:
                                target_nickname = parts[1].strip()
                                if target_nickname in nicknames:
                                    target_index = nicknames.index(target_nickname)
                                    target_client = clients[target_index]
                                    target_client.send("You have been kicked from the server!".encode('utf-8'))
                                    remove_client(target_client)
                                    broadcast(f"{target_nickname} was kicked by {nickname}.".encode('utf-8'))
                                else:
                                    client_socket.send("User not found.".encode('utf-8'))
                            else:
                                client_socket.send("Usage: /kick <nickname>".encode('utf-8'))
                        else:
                            client_socket.send("You don't have permission to use this command.".encode('utf-8'))
                    else:
                        client_socket.send(f"Unknown command: {command}".encode('utf-8'))
                else:
                    broadcast(f"[{nickname}] {decoded_message}".encode('utf-8'), _client=client_socket)

            except ConnectionResetError:
                break
            except UnicodeDecodeError:
                client_socket.send("Server: Error decoding your message.".encode('utf-8'))
            except Exception:
                break
    finally:
        if nickname:
            remove_client(client_socket)
        else:
            client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        server.listen()

        while True:
            client_socket, address = server.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, address))
            thread.start()
    except socket.error:
        sys.exit(1)
    except KeyboardInterrupt:
        pass
    finally:
        with client_lock:
            for client in clients:
                client.close()
        server.close()


if __name__ == "__main__":
    start_server()