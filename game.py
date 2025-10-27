import pygame
import random
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 800
PLAYER_SIZE = 50
METEOR_SIZE = 50
FPS = 60

WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 150, 255)
BLACK = (10, 10, 20)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Space Dodger (Web Edition)")

clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 70))
        self.speed = 7

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((METEOR_SIZE, METEOR_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), -50))
        self.speed = random.randint(4, 9)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


def draw_text(text, size, color, x, y):
    font_obj = pygame.font.SysFont("consolas", size)
    text_surface = font_obj.render(text, True, color)
    screen.blit(text_surface, (x, y))


def main():
    player = Player()
    all_sprites = pygame.sprite.Group(player)
    meteors = pygame.sprite.Group()

    score = 0
    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, 700)

    running = True
    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == spawn_event:
                meteor = Meteor()
                all_sprites.add(meteor)
                meteors.add(meteor)

        all_sprites.update(keys)

        if pygame.sprite.spritecollideany(player, meteors):
            running = False

        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_text(f"Score: {score}", 24, WHITE, 10, 10)
        pygame.display.flip()

        score += 1

    # Game over
    screen.fill(BLACK)
    draw_text("GAME OVER", 60, RED, WIDTH // 2 - 160, HEIGHT // 2 - 40)
    draw_text(f"Final Score: {score}", 40, WHITE, WIDTH // 2 - 130, HEIGHT // 2 + 30)
    pygame.display.flip()
    pygame.time.wait(2500)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
