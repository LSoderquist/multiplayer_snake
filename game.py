import pygame
from network import Network
from helpers import process_player_data

WIDTH = 900
HEIGHT = 900
BG_COLOR = '#000000'
PLAYER_SIZE = 50
TICKS_PER_MOVEMENT = 250
FOOD_COLOR = 'red'
FOOD_RADIUS = PLAYER_SIZE // 2
SCORE_COLOR = 'yellow'

class Player:

    def __init__(self):
        self.x = [100]
        self.y = [100]
        self.vel = 50
        self.dir = 'r'

    def draw(self, window, color):
        for x, y in zip(self.x, self.y): 
            pygame.draw.rect(window, color, (x, y, PLAYER_SIZE, PLAYER_SIZE))

pygame.font.init()

color = input('pick color:')
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
player = Player()
net = Network()
network_players = {}
running = True
seconds = 0
while running:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.dir != 'r': player.dir = 'l'
    if keys[pygame.K_RIGHT] and player.dir != 'l': player.dir = 'r'
    if keys[pygame.K_UP] and player.dir != 'd': player.dir = 'u'
    if keys[pygame.K_DOWN] and player.dir != 'u': player.dir = 'd'
    window.fill(BG_COLOR)

    req = ''
    for x, y in zip(player.x, player.y): req += f'{x} {y} '
    print('pre-send')
    res = net.send(f'{req}{color}').split(',')
    print('post-send')
    print(res)
    network_players = {}
    if res != ['-']:
        foodpos = None
        for data in res:
            if not data: continue
            if data[:4] == 'food': foodpos = list(map(int, data.split(' ')[1:3]))
            else: 
                data = data.split(' ')
                p = data[0]
                network_players[p] = process_player_data(data[1:])

        if foodpos: 
            coordinates = (foodpos[0] + FOOD_RADIUS, foodpos[1] + FOOD_RADIUS)
            pygame.draw.circle(window, FOOD_COLOR, coordinates, FOOD_RADIUS)

        for p in network_players: 
            print(network_players[p][0], network_players[p][1], PLAYER_SIZE, PLAYER_SIZE)
            for x, y in network_players[p][0]:
                pygame.draw.rect(
                    window, 
                    network_players[p][1], 
                    (x, y, PLAYER_SIZE, PLAYER_SIZE)
                )

    ticks = pygame.time.get_ticks()
    is_moving_tick = ticks // TICKS_PER_MOVEMENT > seconds
    if is_moving_tick: 
        if player.dir == 'l': 
            player.x.append(max(player.x[-1] - player.vel, 0))
            player.y.append(player.y[-1])
        elif player.dir == 'r': 
            player.x.append(min(player.x[-1] + player.vel, WIDTH - PLAYER_SIZE))
            player.y.append(player.y[-1])
        elif player.dir == 'u': 
            player.y.append(max(player.y[-1] - player.vel, 0))
            player.x.append(player.x[-1])
        elif player.dir == 'd': 
            player.y.append(min(player.y[-1] + player.vel, HEIGHT - PLAYER_SIZE))
            player.x.append(player.x[-1])

        seconds = ticks // TICKS_PER_MOVEMENT

    if foodpos and player.x[-1] == foodpos[0] and player.y[-1] == foodpos[1]: 
        net.send('food eaten', response=False)
    elif is_moving_tick: 
        player.x.pop(0)
        player.y.pop(0)

    head_coords = (player.x[-1], player.y[-1])
    tail_coords = zip(player.x[:len(player.x)-1], player.y[:len(player.y)-1])
    other_player_coords = [network_players[p][0] for p in network_players]
    snake_collides_with_itself = head_coords in tail_coords
    snake_collides_with_other = any([head_coords in player_coords for player_coords in other_player_coords])
    if snake_collides_with_itself or snake_collides_with_other : player = Player()

    font = pygame.font.SysFont('Impact', 25)
    player_score = font.render(f'{color}: {len(player.x)}', False, SCORE_COLOR)
    window.blit(player_score, (0, 0))
    score_pos = PLAYER_SIZE
    for p in network_players:
        score = font.render(f'{network_players[p][1]}: {len(network_players[p][0])}', False, SCORE_COLOR)
        window.blit(score, (0, score_pos))
        score_pos += PLAYER_SIZE

    player.draw(window, color)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            net.send('quit', response=False)

    clock.tick(60)




