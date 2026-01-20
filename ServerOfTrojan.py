import socket
import ssl
import sqlite3
import random
from wordfreq import top_n_list

def Server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(server_socket)
    ssl_sock.bind(('0.0.0.0', 8080))
    ssl_sock.listen()
    while True:
        client_socket, client_address = ssl_sock.accept()
        print("Accepted connection from:", client_address)
        Handle_client(client_socket)

def Handle_client(client_socket):
    secret = generate_secret()
    make_connection_database(secret)
    client_socket.send(secret.encode())
    file = input("Enter file path (target's file path to encode): ")
    client_socket.send(file.encode())

def generate_secret(num_words=3):
    words = top_n_list("en", 50000)
    return "-".join(random.choice(words) for _ in range(num_words))

def make_connection_database(secret):
    conn = sqlite3.connect('secret.db')
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS secrets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        secret TEXT NOT NULL
    )
    """)
    c.execute("INSERT INTO secrets (secret) VALUES (?)", (secret,))
    conn.commit()
    print("Secret generated and saved:")
    print(secret)
    conn.close()

if __name__ == '__main__':
    Server()
