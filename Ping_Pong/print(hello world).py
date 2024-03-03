import pygame
from pygame.locals import *

background_color = (200, 255, 255)
window_width = 600
window_height = 500
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Pong Game')
window.fill(background_color)

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_image, sprite_x, sprite_y, sprite_width, sprite_height, sprite_speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(sprite_image), (sprite_width, sprite_height))
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y
        self.speed = sprite_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_left(self):
        keys = pygame.key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < window_height - 80:
            self.rect.y += self.speed

    def update_right(self):
        keys = pygame.key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < window_height - 80:
            self.rect.y += self.speed

pygame.font.init()
font = pygame.font.Font(None, 35)

loseOne = font.render('Player one lose', True, (180, 0, 0))
loseTwo = font.render('Player two lose', True, (180, 0, 0))

racketOne = Player('racket.png', 30, 200, 50, 150, 4)
racketTwo = Player('racket.png', 520, 200, 50, 150, 4)

ball = GameSprite('tennis_ball.png', 200, 200, 50, 50, 4)

speed_x = 3
speed_y = 3

score_player_one = 0
score_player_two = 0
rounds_to_win = 5

fps = 60
clock = pygame.time.Clock()
game = True
finish = False

def reset_game():
    racketOne.rect.y = 200
    racketTwo.rect.y = 200
    ball.rect.x = window_width // 2 - 25
    ball.rect.y = window_height // 2 - 25

while game:
    for e in pygame.event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.fill(background_color)
        racketOne.update_left()
        racketTwo.update_right()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if ball.rect.y > window_height - 50 or ball.rect.y < 0:
            speed_y *= -1
        if ball.rect.x < 0:
            score_player_two += 1
            if score_player_two >= rounds_to_win:
                finish = True
            else:
                reset_game()
        if ball.rect.x > window_width:
            score_player_one += 1
            if score_player_one >= rounds_to_win:
                finish = True
            else:
                reset_game()
        if pygame.sprite.collide_rect(racketOne, ball) or pygame.sprite.collide_rect(racketTwo, ball):
            speed_x *= -1
            speed_y *= 1

        racketOne.reset()
        racketTwo.reset()
        ball.reset()

        # Display scores
        score_text = font.render(f"Player 1: {score_player_one}  Player 2: {score_player_two}", True, (0, 0, 0))
        window.blit(score_text, (220, 10))

    pygame.display.update()
    clock.tick(fps)
