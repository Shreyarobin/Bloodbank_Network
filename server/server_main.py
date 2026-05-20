import socket
import ssl
import os
import struct
import threading
import time
import json
import re

CONTROL_PORT = 8443
DATA_PORT = 9001
UPLOAD_DIR = "received_files"
BUFFER_SIZE = 4096

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def sanitize_filename(name):
    return re.sub(r'\W+', '_', name)

def handle_control(conn, addr):
    print(f"[CONTROL] Connection from {addr}")
    try:
        data = conn.recv(1024).decode()
        print(f"[CONTROL] Received: {data}")

        if data.startswith("REQUEST_BLOOD"):
            parts = data.strip().split(":")
            if len(parts) == 3:
                blood_type = parts[1].strip()
                city = parts[2].strip()
                print(f"[CONTROL] Blood request for {blood_type} in {city}")
                conn.send("✅ Blood request received and please upload details.".encode('utf-8'))  # ✅ Fixed
            else:
                conn.send("❌ Invalid blood request format.".encode('utf-8'))  # ✅ Fixed
        else:
            conn.send("UNKNOWN".encode('utf-8'))  # ✅ Fixed

    except Exception as e:
        print(f"[CONTROL] Error: {e}")
        conn.send("❌ Server error occurred.".encode('utf-8'))  # ✅ Fixed
    finally:
        conn.close()

def handle_data_transfer(client_socket):
    try:
        metadata = client_socket.recv(1024).decode()
        filename, filesize = metadata.split(":")
        filename = sanitize_filename(filename)
        filesize = int(filesize)

        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, 'wb') as f:
            bytes_received = 0
            while bytes_received < filesize:
                chunk = client_socket.recv(BUFFER_SIZE)
                if not chunk:
                    break
                f.write(chunk)
                bytes_received += len(chunk)

        print(f"[DATA] Received file: {filename}")
    except Exception as e:
        print(f"[DATA] Error: {e}")
    finally:
        client_socket.close()

def start_control_server(ssl_context):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', CONTROL_PORT))
    sock.listen(5)
    print(f"[CONTROL] Listening securely on port {CONTROL_PORT}")

    while True:
        client_sock, addr = sock.accept()
        connstream = ssl_context.wrap_socket(client_sock, server_side=True)
        threading.Thread(target=handle_control, args=(connstream, addr), daemon=True).start()

def start_data_server():
    data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_sock.bind(('', DATA_PORT))
    data_sock.listen(5)
    print(f"[DATA] Listening on port {DATA_PORT}")

    while True:
        client_socket, addr = data_sock.accept()
        threading.Thread(target=handle_data_transfer, args=(client_socket,), daemon=True).start()

def setup_ssl_context():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    return context

def main():
    print("[SERVER] Secure FTP-like server starting...")
    ssl_ctx = setup_ssl_context()
    threading.Thread(target=start_control_server, args=(ssl_ctx,), daemon=True).start()
    threading.Thread(target=start_data_server, daemon=True).start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
