import pygame
import random
import sys
from abc import ABC, abstractmethod

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255,255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Treasure Collector - Enhanced")
clock = pygame.time.Clock()

class GameObject(ABC):
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        """Update logika atau posisi objek."""
        pass

    def draw(self, surface):
        """Gambar objek pada layar."""
        pass

class Player(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self, surface):

        top_point = (self.rect.centerx, self.rect.top)
        left_point = (self.rect.left, self.rect.bottom)
        right_point = (self.rect.right, self.rect.bottom)
        pygame.draw.polygon(surface, self.color, [top_point, left_point, right_point])
  
class Coin(GameObject):
    def __init__(self, x, y, radius, color):
        super().__init__(x, y, radius * 2, radius * 2, color)
        self.radius = radius

    def update(self):
        pass

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.rect.centerx, self.rect.centery), self.radius)


class Trap(GameObject):
    def __init__(self, x, y, width, height, color, speed):
        super().__init__(x, y, width, height, color)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.y = -self.height
            self.rect.x = random.randint(0, WIDTH - self.width)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


def main():
    player = Player(WIDTH // 2, HEIGHT - 60, 50, 50, BLUE)
    coins = [Coin(random.randint(0, WIDTH - 30), random.randint(0, HEIGHT - 30), 15, YELLOW)]
    traps = [Trap(random.randint(0, WIDTH - 40), random.randint(-600, -40), 40, 40, RED, random.randint(3, 6))]

    score = 0
    level = 1
    koin_untuk_level_naik = 10
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.update(keys)

        for trap in traps:
            trap.update()

        for coin in coins[:]:
            if player.rect.colliderect(coin.rect):
                coins.remove(coin)
                score += 1
                coins.append(Coin(random.randint(0, WIDTH - 30), random.randint(0, HEIGHT - 30), 15, YELLOW))

        for trap in traps:
            if player.rect.colliderect(trap.rect):
                print(f"Game Over! Your Score: {score}")
                running = False

        if score >= level * koin_untuk_level_naik:
            level += 1
            traps.append(Trap(random.randint(0, WIDTH - 40), random.randint(-600, -40), 40, 40, RED, random.randint(3, 6)))

        player.draw(screen)
        for coin in coins:
            coin.draw(screen)
        for trap in traps:
            trap.draw(screen)

        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()



        

