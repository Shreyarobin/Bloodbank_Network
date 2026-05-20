# Blood Donation Alert System

A secure socket-based Blood Donation Alert System built using Python that enables real-time donor-recipient communication with SSL encryption, multicast networking, congestion control, and GUI-based management.

---

## Features

- Secure SSL/TLS based communication
- Real-time blood donation alerts
- Multicast socket communication
- TTL-based routing simulation
- Congestion control using Token Bucket/Leaky Bucket
- SQLite integrated donor database
- Tkinter GUI for client interaction
- Intrusion detection and spam monitoring
- Multi-client and multi-server support
- Custom control and data communication protocol

---

## Tech Stack

- Python
- Socket Programming
- SSL/TLS
- Tkinter
- SQLite
- Multithreading
- Networking Concepts

---

## Project Structure

```bash
bloodbank_network/
│
├── server/
│   ├── server_main.py
│   ├── ssl_handler.py
│
├── client/
│   ├── client_main.py
│   ├── ssl_handler.py
│
├── utils/
│   ├── ids_module.py
│   ├── port_scanner.py
│
├── database/
│   ├── donors.db
│
├── certificates/
│   ├── server.crt
│   ├── server.key
│
└── README.md
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/bloodbank_network.git
cd bloodbank_network
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is unavailable:

```bash
pip install pyopenssl
```

---

# How to Run the Project

## Step 1 — Start the Server

Open a terminal inside the project folder:

```bash
cd server
python server_main.py
```

### Example Output

```bash
[SERVER] SSL Server Started
[SERVER] Waiting for clients...
```

---

## Step 2 — Start the Client

Open another terminal:

```bash
cd client
python client_main.py
```

### Example Output

```bash
[CLIENT] Connected securely to server
[CLIENT] GUI Started
```

---

# Example Workflow

## Donor Registration

1. Open the client GUI
2. Enter:
   - Name
   - Blood Group
   - Location
3. Click **Register**

---

## Blood Request Example

```text
Blood Group: O+
Location: Bangalore
Units Needed: 2
```

The system securely multicasts alerts to matching donors.

---

# Networking Concepts Used

- TCP Socket Programming
- SSL/TLS Encryption
- Multicasting
- Congestion Control
- Routing Simulation
- Intrusion Detection
- Reliable Data Transfer

---

# Future Enhancements

- Mobile application support
- GPS-based donor tracking
- Cloud deployment
- AI-based donor prediction
- Emergency priority routing

---

# Contributors

- Shreya Robin

---

# License

This project is developed for educational and academic purposes.
