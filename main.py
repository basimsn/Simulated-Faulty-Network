import socket
import io
import time
import typing
import struct
import homework
import homework.logging

def send(sock: socket.socket, data: bytes):
    # Initialize variables
    sequence_num = 0
    packet_timeout = 0.1
    packet_num = 1
    cycle = 1

    avg_timeout = 0
    last_timeout = 0

    logger = homework.logging.get_logger("hw-tcp-sender")

    #-4 because of sequence number bytes
    offsets = range(0, len(data), homework.MAX_PACKET - 4)

    for chunk in [data[i:i + homework.MAX_PACKET - 4] for i in offsets]:
        # Calculate sequence number for the packet
        sequence_num = packet_num * (homework.MAX_PACKET - 4)
        packet_num += 1

        # Add the sequence number to the chunk and pack it
        chunk = struct.pack('I', sequence_num) + chunk

        # Send the chunk over the socket
        sock.send(chunk)
        start = time.time()

        # Log the pause duration
        logger.info("Pausing for %f seconds", round(packet_timeout, 2))

        # Adjust packet timeout based on packet number
        if packet_num == 2:
            packet_timeout = 0.2
        else:
            packet_timeout = (abs(last_timeout - avg_timeout) * 4) + avg_timeout

        # Set socket timeout
        sock.settimeout(packet_timeout)

        # Wait for acknowledgment
        while True:
            try:
                data = sock.recv(4)
                temp_sequence_num = struct.unpack("I", data[:4])[0]
                if temp_sequence_num == sequence_num:
                    last_timeout = time.time() - start
                    avg_timeout = (((cycle - 1) * avg_timeout) + last_timeout) / cycle
                    cycle += 1
                    break
            except socket.timeout:
                # Adjust packet timeout in case of timeout
                packet_timeout = avg_timeout + (abs(last_timeout - avg_timeout) * 4)
                sock.send(chunk)
                start = time.time()
                if packet_num == 2:
                    packet_timeout = 0.2
                time.sleep(packet_timeout)


def recv(sock: socket.socket, dest: io.BufferedIOBase) -> int:
    # Get logger object for logging
    logger = homework.logging.get_logger("hw-tcp-receiver")

    # Initialize variables
    num_bytes = 0
    expected_seq_num = 0

    # Receive data until there is no more data
    while True:
        data = sock.recv(homework.MAX_PACKET)
        if not data:
            break
        actual_seq_num = struct.unpack('i', data[:4])[0]
        data = data[4:]
        if data == b'':
            break
        logger.info("Received %d bytes", len(data))
        if actual_seq_num > expected_seq_num:
            # Write data to the destination
            expected_seq_num = actual_seq_num
            dest.write(data)
            num_bytes += len(data)
            dest.flush()
        # Send acknowledgment
        sock.send(struct.pack('i', expected_seq_num))

    # Return the number of bytes written to the destination
    return num_bytes