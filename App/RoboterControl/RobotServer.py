import socket, time, random
from datetime import datetime
import RobotInfo
import re

def parse_joint_string(data):
    match = re.search(r"Joints:([-0-9.;]+)#", data)
    if match:
        joint_values = match.group(1).split(';')
        return [float(value) for value in joint_values]
    else:
        raise ValueError("Invalid joint string format")


def print_with_time(message):
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"[{current_time}] {message}")


def handle_client(client_socket,a1,a2,a3,a4,a5,a6):
    counter = 0
    try:

        # Step 1: Listen for the current position
        data = client_socket.recv(1024).decode('utf-8')
        print_with_time(f"Received current position: {data}")
        # Step 2: Send a move command to the client using Simple Parser format
        move_command = f"Ping:{a1};{a2};{a3};{a4};{a5};{a6}#"
    
        if counter % 2 != 0:
            move_command = f"Ping:0.0;0.0;0.0;0.0;0.0;0.0#"
        print_with_time(f"Sending move command: {move_command}\nCounter: {counter}")
        counter += 1
        
        #pos.A1;pos.A2;pos.A3;pos.A4;pos.A5;pos.A6
        x = client_socket.sendall(move_command.encode('utf-8'))

        print(x)
        time.sleep(5)
        # Step 3: Receive the new position confirmation from the client
        data = client_socket.recv(1024).decode('utf-8')

        print_with_time(f"Received confirmation: {data}")
        joints = parse_joint_string(data)
        result = RobotInfo.checkRangeOfMotion(joints[0], joints[1], joints[2], joints[3], joints[4], joints[5])
        print_with_time(f"Result: {result}")

    except socket.error as e:
        print_with_time(f"Socket error: {e}")
    except Exception as e:
        print_with_time(f"Unexpected error: {e}")
    finally:
        client_socket.close()
    


def start_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)
    print_with_time(f"Server listening on {ip}:{port}")

    try:
        client_socket, addr = server_socket.accept()
        print_with_time(f"Connection from {addr}")
        time.sleep(0.5)  # Delay to limit requests and sendings to 1 per 0.5 seconds
        return client_socket
    except Exception as e:
        print_with_time(f"Error accepting connection: {e}")


if __name__ == "__main__":
    robotId = 1
    port = 12345
    client_socket = start_server('0.0.0.0', port)

    while True:
        #read db


        # hand over the joint values
        handle_client(client_socket,1.0,1.0,1.0,1.0,1.0,1.0)
