import socket
import threading
import time
import json

class GameServer:
    def __init__(self, host, port):
        self.pos1p = 100  # 初期位置
        self.pos2p = 100  # 初期位置
        self.ball_x = 320
        self.ball_y = 240
        self.ball_dx = 2  # ボールの速度
        self.ball_dy = 2
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        print(f"Server started at {host}:{port}")

    def update_ball_position(self):
        # ボールの位置を更新
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # 画面端でのボールの反射などのロジックをここに追加
        if self.ball_x >= 640 or self.ball_x <= 0:
            self.ball_dx *= -1  # 方向を反転
        if self.ball_y >= 480 or self.ball_y <= 0:
            self.ball_dy *= -1

    def broadcast_game_state(self):
        while True:
            self.update_ball_position()  # ボールの位置を更新
            state = {
                'pos1p': self.pos1p,
                'pos2p': self.pos2p,
                'ball_x': self.ball_x,
                'ball_y': self.ball_y
            }
            state_json = json.dumps(state).encode('utf-8')
            for client in self.clients:
                client.sendall(state_json)
            time.sleep(1 / 60)  # 約60fpsで更新

    def handle_client(self, conn, addr):
        self.clients.append(conn)
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break

            command = data.decode()
            if command.startswith('UP_1P'):
                self.pos1p -= 5  # 上に移動
            elif command.startswith('DOWN_1P'):
                self.pos1p += 5  # 下に移動
            elif command.startswith('UP_2P'):
                self.pos2p -= 5  # 上に移動
            elif command.startswith('DOWN_2P'):
                self.pos2p += 5  # 下に移動

        self.clients.remove(conn)
        conn.close()

    def start(self):
        threading.Thread(target=self.broadcast_game_state, daemon=True).start()
        # ボールの更新を別スレッドで実行
        threading.Thread(target=self.update_ball_position, daemon=True).start()
        while True:
            conn, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    game_server = GameServer('pi5.local', 65432)
    game_server.start()
