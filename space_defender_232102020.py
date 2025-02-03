import pygame
import random
import sys

pygame.init()
pygame.mixer.init()  # Inisialisasi pygame mixer untuk efek suara

WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (0, 255 ,255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Defender")
clock = pygame.time.Clock()

# Memuat gambar latar belakang dan menyesuaikan ukuran dengan layar
background_image = pygame.image.load("gambar2.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Memuat efek suara tembakan
shoot_sound = pygame.mixer.Sound("laser-bolt-89300.wav") 

class GameObject:
    def __init__(self, x, y, width, height, color, image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Jika diberikan path gambar, gambar akan dimuat dan disesuaikan ukurannya
        if image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        else:
            self.image = None

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

class Player(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color, "pesawat.png")  # Menggunakan gambar "pesawat.png" untuk player
        self.speed = 7  
        self.lives = 100  

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:  # Bergerak ke kiri
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:  # Bergerak ke kanan
            self.rect.x += self.speed

    # Menembakkan peluru
    def shoot(self):
        bullets = [
            Bullet(self.rect.centerx - 15, self.rect.top, 5, 10, GREEN),
            Bullet(self.rect.centerx, self.rect.top, 5, 10, GREEN),
            Bullet(self.rect.centerx + 15, self.rect.top, 5, 10, GREEN)
        ]
        shoot_sound.play()  # Memainkan suara tembakan
        return bullets

class Bullet(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.speed = -10  # Kecepatan peluru (negatif agar bergerak ke atas)

    # Menggerakkan peluru
    def move(self):
        self.rect.y += self.speed

class Meteor(GameObject):
    def __init__(self, x, y, width, height, color, speed, image_path, can_shoot=False):
        super().__init__(x, y, width, height, color, image_path)
        self.speed = speed  
        self.can_shoot = can_shoot 
        self.last_shot_time = 0  

    def fall(self):
        self.rect.y += self.speed

    def shoot(self):
        if self.can_shoot:
            return MeteorBullet(self.rect.centerx, self.rect.bottom, 5, 10, RED, 5)
        return None

class MeteorBullet(GameObject):
    def __init__(self, x, y, width, height, color, speed):
        super().__init__(x, y, width, height, color)
        self.speed = speed  # Kecepatan peluru meteor

    def move(self):
        self.rect.y += self.speed

# Fungsi untuk membuat meteor secara acak
def create_random_meteor():
    meteor_types = [
        {"width": 40, "height": 40, "speed": random.randint(3, 5), "image": "ufo.png", "can_shoot": False},  # Meteor kecil
        {"width": 80, "height": 80, "speed": random.randint(2, 4), "image": "ufo2.png", "can_shoot": True}  # Meteor besar
    ]
    chosen_type = random.choice(meteor_types)  # Memilih tipe meteor secara acak
    return Meteor(
        random.randint(0, WIDTH - chosen_type["width"]),  # Posisi horizontal meteor secara acak
        0,  # Memulai dari atas layar
        chosen_type["width"],
        chosen_type["height"],
        RED,
        chosen_type["speed"],
        chosen_type["image"],
        chosen_type["can_shoot"]
    )

def main():
    player = Player(WIDTH // 2, HEIGHT - 80, 80, 80, BLUE)  # Inisialisasi player

    meteors = [] 
    bullets = []  
    meteor_bullets = []  

    score = 0  
    running = True  
    last_shot_time = 0 
    shoot_cooldown = 50  

    while running:
        screen.blit(background_image, (0, 0))  # Menampilkan gambar latar belakang

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed() 
        player.move(keys) 

        # Player menembak dengan cooldown
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and current_time - last_shot_time > shoot_cooldown:
            bullets.extend(player.shoot())  
            last_shot_time = current_time  

        # Spawn meteor secara acak
        if random.randint(1, 50) == 1:
            meteors.append(create_random_meteor())  

        # Meteor menembakkan peluru
        for meteor in meteors[:]:
            if meteor.can_shoot and current_time - meteor.last_shot_time > 2000:
                meteor_bullet = meteor.shoot()  # Biarkan meteor menembak
                if meteor_bullet:
                    meteor_bullets.append(meteor_bullet)  # Tambahkan peluru meteor ke daftar
                meteor.last_shot_time = current_time  # Memperbarui waktu tembakan meteor

        # Meteor jatuh dan memeriksa apakah sudah keluar layar
        for meteor in meteors[:]:
            meteor.fall()
            if meteor.rect.top > HEIGHT:
                meteors.remove(meteor)  
                player.lives -= 1  
                if player.lives == 0:
                    print(f"Game Over! Skor Anda: {score}")
                    running = False  

        # Menggerakkan peluru meteor
        for meteor_bullet in meteor_bullets[:]:
            meteor_bullet.move()
            if meteor_bullet.rect.top > HEIGHT:
                meteor_bullets.remove(meteor_bullet)  

        for bullet in bullets[:]:
            bullet.move()
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)  # Hapus peluru jika keluar layar

        # Memeriksa tabrakan antara peluru player dan meteor
        for bullet in bullets[:]:
            for meteor in meteors[:]:
                if bullet.rect.colliderect(meteor.rect):  # Jika peluru mengenai meteor
                    bullets.remove(bullet)  
                    meteors.remove(meteor) 
                    score += 1  
                    break

        # Memeriksa tabrakan antara peluru meteor dan player
        for meteor_bullet in meteor_bullets[:]:
            if meteor_bullet.rect.colliderect(player.rect):  # Jika peluru meteor mengenai player
                meteor_bullets.remove(meteor_bullet)  
                player.lives -= 5  # Kurangi nyawa player
                if player.lives <= 0: 
                    print(f"Game Over! Skor Anda: {score}")
                    running = False

        player.draw(screen)
        for meteor in meteors:
            meteor.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for meteor_bullet in meteor_bullets:
            meteor_bullet.draw(screen)

        # Menampilkan skor dan nyawa pada layar
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Skor: {score}", True, WHITE)
        lives_text = font.render(f"Nyawa: {player.lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        pygame.display.flip() 
        clock.tick(FPS) 

if __name__ == "__main__":
    main()
