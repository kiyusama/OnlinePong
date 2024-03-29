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
                game_state['point1p'] = state['point1p']
                game_state['point2p'] = state['point2p']
            except ValueError as e:
                print(f"Error processing received data: {e}")
            except KeyError as e:
                print(f"Key error in received data: {e}")

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Client-1P")
    font = pygame.font.Font(None, 36)

    game_state = {'pos1p': 240, 'pos2p': 240, 'ball_x': 320, 'ball_y': 240, 'point1p': 0, 'point2p': 0}

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
            s.sendall('UP_1P'.encode())
        elif keys[pygame.K_DOWN]:
            s.sendall('DOWN_1P'.encode())

        pygame.draw.line(screen, (255, 255, 255), (100, game_state['pos1p'] - 30), (100, game_state['pos1p'] + 30), 10)
        pygame.draw.line(screen, (255, 255, 255), (540, game_state['pos2p'] - 30), (540, game_state['pos2p'] + 30), 10)
        pygame.draw.circle(screen, (255, 255, 255), (game_state['ball_x'], game_state['ball_y']), 10)
        point1p = font.render(str(game_state['point1p']), True, (255, 255, 255))
        point2p = font.render(str(game_state['point2p']), True, (255, 255, 255))
        screen.blit(point1p, (230, 50))
        screen.blit(point2p, (390, 50))
        if game_state['point1p'] >= 5:
            winner = font.render("1P wins!", True, (255, 255, 255))
            screen.blit(winner, (270, 200))
        elif game_state['point2p'] >= 5:
            winner = font.render("2P wins!", True, (255, 255, 255))
            screen.blit(winner, (270, 200))
            

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
    s.close()

if __name__ == "__main__":
    main()
