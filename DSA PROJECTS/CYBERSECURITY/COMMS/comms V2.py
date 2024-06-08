from cryptography.fernet import Fernet
import socket
import threading

# Read the key from the file
def load_key():
    with open('secret.key', 'rb') as key_file:
        return key_file.read()

key = load_key()
cipher_suite = Fernet(key)

# Shared variables for IP and port
host = '127.0.0.1'
port1 = 5000
port2 = 5001

# Function to handle receiving messages
def receive_messages(conn, cipher_suite):
    while True:
        try:
            encrypted_data = conn.recv(1024)
            if not encrypted_data:
                break
            decrypted_message = cipher_suite.decrypt(encrypted_data).decode()
            print(f"Received: {decrypted_message}")
        except Exception as e:
            print(f"Error: {e}")
            break

# Function to handle sending messages
def send_messages(conn, cipher_suite):
    while True:
        message = input("You: ")
        encrypted_message = cipher_suite.encrypt(message.encode())
        conn.send(encrypted_message)

# Server function to accept connections
def server_program(port):
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    print(f"Connection from: {address}")

    threading.Thread(target=receive_messages, args=(conn, cipher_suite)).start()
    send_messages(conn, cipher_suite)

# Client function to connect to a server
def client_program(port):
    client_socket = socket.socket()
    client_socket.connect((host, port))

    threading.Thread(target=receive_messages, args=(client_socket, cipher_suite)).start()
    send_messages(client_socket, cipher_suite)

if __name__ == "__main__":
    choice = input("Run as user1 or user2 (1/2): ").lower()
    if choice == '1':
        threading.Thread(target=server_program, args=(port1,)).start()
        client_program(port2)
    elif choice == '2':
        threading.Thread(target=server_program, args=(port2,)).start()
        client_program(port1)
