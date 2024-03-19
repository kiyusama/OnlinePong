import socket
import pygame
import threading
import json

def receive_data(s, game_state):
    while True:
        data = s.recv(1024)
        if data:
            try:
                state = json.loads(data.decode())
                game_state['pos1p'] = state['pos1p']
                game_state['pos2p'] = state['pos2p']
                game_state['ball_x'] = state['ball_x']
                game_state['ball_y'] = state['ball_y']
            except ValueError as e:
                print(f"Error processing received data: {e}")
            except KeyError as e:
                print(f"Key error in received data: {e}")

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Client-2P")
    font = pygame.font.Font(None, 36)

    game_state = {'pos1p': 100, 'pos2p': 100}

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('pi5.local', 65432))

    threading.Thread(target=receive_data, args=(s, game_state), daemon=True).start()

    running = True
    while running:
        screen.fill((0, 0, 0))  # 背景を黒で塗りつぶし
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            s.sendall('UP_2P'.encode())
        elif keys[pygame.K_DOWN]:
            s.sendall('DOWN_2P'.encode())

        pygame.draw.line(screen, (255, 255, 255), (100, game_state['pos1p'] - 30), (100, game_state['pos1p'] + 30), 10)
        pygame.draw.line(screen, (255, 255, 255), (540, game_state['pos2p'] - 30), (540, game_state['pos2p'] + 30), 10)

        pygame.draw.circle(screen, (255, 255, 255), (game_state['ball_x'], game_state['ball_y']), 10)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
    s.close()

if __name__ == "__main__":
    main()
