import socket
import threading
import time

def read_users_from_file(filename):
    users = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or ':' not in line: continue
            username, password = line.split(':', 1)
            users.append((username, password))
    return users

def simulate_client(username, password):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 12345))
        
        # Read "Enter username: "
        s.recv(1024)
        s.sendall(username.encode())
        
        # Read "Enter password: "
        s.recv(1024)
        s.sendall(password.encode())
        
        # Read welcome message
        response = s.recv(1024).decode(errors='ignore')
        if "Authentication failed" in response:
            print(f"[{username}] Auth failed.")
            s.close()
            return
            
        # Hold the connection open for 15 seconds!
        # This guarantees everyone is connected AT THE EXACT SAME TIME.
        time.sleep(15)
        
        # Send exit command
        s.sendall(b"/exit\n")
        s.close()
        print(f"User {username} held connection and exited cleanly.")
    except Exception as e:
        print(f"[{username}] Error: {e}")

def main():
    users = read_users_from_file("users.txt")[:1000]
    num_users = len(users)
    print(f"Starting TRUE stress test with {num_users} simultaneous connections...")
    
    threads = []
    
    for username, password in users:
        thread = threading.Thread(target=simulate_client, args=(username, password))
        threads.append(thread)
        thread.start()
        # Slight stagger to not overwhelm the OS socket accept queue
        time.sleep(0.01)
        
    for thread in threads:
        thread.join()
        
    print("True stress test completed!")

if __name__ == "__main__":
    main()
