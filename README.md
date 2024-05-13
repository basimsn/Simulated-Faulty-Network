# README: Simulated Faulty Network Communication
This project simulates a faulty network communication system, allowing for the transmission of data between a client and a server over unreliable connections. The system consists of multiple Python scripts that mimic the behavior of sending and receiving data over simulated network connections.

### Overview
The simulated network communication system comprises three main components:

Sender Script: Sends data over the simulated network connection.
Receiver Script: Receives data over the simulated network connection.
Server Script: Sits between the sender and receiver, simulating network behavior such as packet loss and delays.
These scripts interact to demonstrate how data transmission can be affected by network issues like packet loss and delays.

### Setup
To set up the project, follow these steps:

Clone the repository to your local machine.
Ensure you have Python installed (Python 3.6 or later recommended).
Install any required dependencies by running pip install -r requirements.txt.

### Scripts
#### Sender Script
The sender script (sender.py) reads data from a file and sends it over the simulated network connection. It utilizes a custom protocol for packet transmission and handles timeouts and acknowledgments.

#### Receiver Script
The receiver script (receiver.py) listens for data over the simulated network connection and writes it to a specified file. It acknowledges received packets and handles out-of-order packets.

#### Server Script
The server script (server.py) acts as an intermediary between the sender and receiver. It simulates network behavior such as packet loss and delays based on specified parameters.

#### Main Script
The main script (main.py) is used for most of the code dealing with the fault network. It has timeouts and retransmissions of packets.



### Usage
To use the simulated network communication system, follow these steps:

Start the server script with desired parameters (loss, delay, etc.).
Run the sender script, providing the file to send and the server's port.
Run the receiver script, specifying the output file and the server's port.
Additional Notes
Verbose Mode: Each script supports a verbose mode (-v or --verbose) for detailed logging.
Custom Logging: Logging is implemented using the homework.logging module to provide insight into the communication process.

### Contributors
This project was created by Basim Nabulsi.
