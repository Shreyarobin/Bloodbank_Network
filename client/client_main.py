import socket
import ssl
import os
import json
import struct
import threading
import re

CONTROL_SERVER = '127.0.0.1'
CONTROL_PORT = 8443
DATA_PORT = 9001
BUFFER_SIZE = 4096

UPLOAD_DIR = "received_files"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def sanitize_filename(name):
    return re.sub(r'\W+', '_', name)

def send_control_message(blood_type, city):
    try:
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations(cafile='server_cert.pem')
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=CONTROL_SERVER) as conn:
            conn.connect((CONTROL_SERVER, CONTROL_PORT))
            message = f"REQUEST_BLOOD:{blood_type}:{city}"
            conn.send(message.encode())
            response = conn.recv(1024).decode()
            print(f"[CONTROL] Server Response: {response}")
    except Exception as e:
        print(f"[CONTROL] Error: {e}")

def send_data_file(filename):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((CONTROL_SERVER, DATA_PORT))

        filesize = os.path.getsize(filename)
        metadata = f"{os.path.basename(filename)}:{filesize}"
        sock.send(metadata.encode())

        with open(filename, 'rb') as f:
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                sock.send(data)

        sock.close()
        print(f"[DATA] File '{filename}' sent successfully.")
    except Exception as e:
        print(f"[DATA] Error sending file: {e}")

def send_blood_request():
    print("\nEnter patient details for blood request")
    name = input("Patient Name: ").strip()
    hospital = input("Hospital Name: ").strip()
    city = input("City: ").strip()
    contact = input("Contact Number: ").strip()
    blood_type = input("Blood Group (A+/O-/etc): ").strip().upper()

    if not all([name, hospital, city, contact, blood_type]):
        print("[INPUT] Please fill all the fields.")
        return

    data = {
        "patient_name": name,
        "hospital_name": hospital,
        "city": city,
        "contact": contact,
        "blood_type": blood_type
    }

    filename = f"{sanitize_filename(name)}_request.json"
    with open(filename, "w") as f:
        json.dump(data, f)

    print("[INFO] Sending request and data securely to the server...")
    threading.Thread(target=send_control_message, args=(blood_type, city), daemon=True).start()
    threading.Thread(target=send_data_file, args=(filename,), daemon=True).start()

def upload_patient_file():
    # Correct indentation
    filepath = input("Enter full path of patient report to upload (PDF/JPG): ").strip()

    print(f"[DEBUG] Checking file path: {filepath}")
    
    if not os.path.isfile(filepath):
        print("[ERROR] File does not exist.")
        return

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((CONTROL_SERVER, DATA_PORT))

        filesize = os.path.getsize(filepath)
        filename = os.path.basename(filepath)
        metadata = f"{filename}:{filesize}"
        sock.send(metadata.encode())

        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(BUFFER_SIZE)
                if not chunk:
                    break
                sock.send(chunk)

        print(f"[DATA] File '{filename}' uploaded successfully.")
        sock.close()
    except Exception as e:
        print(f"[UPLOAD] Error uploading file: {e}")

def main():
    print("""
========= Blood Bank FTP Client =========
Options:
1. SEND_REQUEST       - Submit blood request (JSON)
2. UPLOAD_REPORT      - Upload patient report (PDF/JPG)
3. EXIT               - Exit the application
=========================================
    """)
    while True:
        cmd = input("Enter command: ").strip().upper()

        if cmd == "SEND_REQUEST":
            send_blood_request()
        elif cmd == "UPLOAD_REPORT":
            upload_patient_file()
        elif cmd == "EXIT":
            print("[EXIT] Closing application.")
            break
        else:
            print("[ERROR] Unknown command. Please try again.")

if __name__ == "__main__":
    main()
