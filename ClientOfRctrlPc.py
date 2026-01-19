import socket
import cv2

HOST = '127.0.0.1'
PORT = 65432

def send_command(action, params=None):
    command = f"{action},{params}" if params else action
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(command.encode('utf-8'))
        if action in ['screenshot', 'list_dir', 'camera']:
            data = s.recv(4096)
            if action == 'screenshot':
                with open('received_screenshot.png', 'wb') as f:
                    f.write(data)
                img = Image.open('received_screenshot.png')
                img.show()
            elif action == 'list_dir':
                files = data.decode('utf-8')
                print(files)
            elif action == 'camera':
                nparr = np.frombuffer(data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                cv2.imshow('Camera', img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        s.close()

if __name__ == "__main__":
    while True:
        command = input("Enter command (screenshot, move_mouse, click, type, list_dir, camera): ")
        if command == 'move_mouse':
            x = int(input("Enter x: "))
            y = int(input("Enter y: "))
            send_command('move_mouse', f"{x},{y}")
        elif command == 'type':
            text = input("Enter text: ")
            send_command('type', text)
        elif command == 'list_dir':
            path = input("Enter directory path: ")
            send_command('list_dir', path)
        else:
            send_command(command)
