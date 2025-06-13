import socket
import threading
import sys

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            # اینجا می‌توانید داده‌ها را پردازش کنید (مثلاً به اینترنت فوروارد کنید)
            print("Received data from client:", data[:100], "...")
            # پاسخ آزمایشی (اختیاری)
            client_socket.send(b"ACK: Data received by server")
    except Exception as e:
        print("Server error:", e)
    finally:
        client_socket.close()

def start_server(port=9090):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"⚡ Server listening on port {port}")

    while True:
        client_sock, addr = server.accept()
        print(f"🔗 New connection from: {addr}")
        threading.Thread(target=handle_client, args=(client_sock,)).start()

if __name__ == "__main__":
    start_server()