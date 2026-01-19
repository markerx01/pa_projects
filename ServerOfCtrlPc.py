import socket
import threading
import pyautogui
from PIL import ImageGrab
import cv2

HOST = '0.0.0.0'
PORT = 65432

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        command = data.decode('utf-8')
        if command == 'screenshot':
            screenshot = ImageGrab.grab()
            screenshot.save('snapshot.png')
            with open('snapshot.png', 'rb') as f:
                screenshot_data = f.read()
            conn.sendall(screenshot_data)
        elif command.startswith('move_mouse'):
            x, y = map(int, command.split(',')[1:])
            pyautogui.moveTo(x, y)
        elif command == 'click':
            pyautogui.click()
        elif command.startswith('type'):
            text = command.split(',')[1]
            pyautogui.typewrite(text)
        elif command.startswith('list_dir'):
            path = command.split(',')[1]
            files = ' '.join(['file1', 'file2', 'file3'])
            conn.sendall(files.encode('utf-8'))
        elif command == 'camera':
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                _, buffer = cv2.imencode('.jpg', frame)
                conn.sendall(buffer.tobytes())
            cap.release()
        else:
            conn.sendall(b'Unknown command')
    conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
