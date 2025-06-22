Multi-User Chat Application

> Real-time Multi-User Chat (Socket & Threading)
A foundational real-time chat application demonstrating direct network communication using Python's socket module and concurrent client handling via threading.
It features a server that broadcasts messages, supports custom nicknames, and includes basic moderation commands.

> Features
Instant message exchange between multiple clients.
Server handles concurrent connections.
Clients use unique nicknames.
Messages broadcast to all participants.
Basic admin commands (e.g., /kick).

> Technologies
Python 3.x
socket module (Network communication)
threading module (Concurrency)

>  Getting Started
Clone the repository (ensure server.py and client.py are present).
Create and activate a virtual environment (as above).
No external dependencies required.
Open two (or more) separate terminal windows.
In the first terminal, run the server:
python server.py

In the second (and subsequent) terminals, run the client:
python client.py

Enter a nickname when prompted.
