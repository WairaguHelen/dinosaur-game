import pygame
import os
import random

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 1100
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Super Dino")

# Load images
RUNNING = [
    pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))
]

JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

DUCKING = [
    pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))
]

SMALL_CACTUS = [
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))
]

LARGE_CACTUS = [
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))
]

BIRD = [
    pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))
]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

# Game loop
class Dinosaur:
    x_pos = 80
    y_pos = 310
    y_pos_duck = 340
    jump_velocity = 8
    dino_duck_time = 0
    dino_duck_time_limit = 20
    dino_duck_timer = 0


    def __init__(self):
        self.duck_img = DUCKING
        self.jump_img = JUMPING
        self.run_img = RUNNING

        self.dino_duck = False
        self.dino_jump = False
        self.dino_run = True
        
        self.step_index = 0
        self.jump_velocity = self.jump_velocity
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos
    
    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        
        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_jump = True
            self.dino_duck = False
            self.dino_run = False
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos
        self.step_index += 1
    
    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_velocity * 5
            self.jump_velocity -= 0.8
        if self.jump_velocity < -8:
            self.dino_jump = False
            self.jump_velocity = 8

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos_duck
        self.step_index += 1

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud:
    def __init__(self):
        self.x = screen_width + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.x -= game_speed
    
    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = screen_width + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

class Obstacles:
    def __init__(self, image, type):
        #self.x = screen_width + random.randint(800, 1000)
        #self.y = random.randint(200, 350)
        self.image = image
        #self.width = self.image.get_width()
        self.type = type
        self.rect = self.image[self.type].get_rect()
        #self.rect.x = 1100
        self.rect.x = screen_width
    
    def update(self):
        self.rect.x -= game_speed

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)

class smallCactus(Obstacles):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 330

class largeCactus(Obstacles):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacles):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice([200, 250, 300])  
        self.index = 0 

    def update(self):
        self.rect.x -= game_speed  
        self.rect.y += random.randint(-10, 10) 
        self.index += 1  
        if self.index >= 10: 
            self.index = 0  

    def draw(self, screen):
        screen.blit(self.image[self.index // 5], self.rect) 

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.SysFont('Arial', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        
        text = font.render(f"Score: {points}", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (800, 50)
        screen.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        screen.blit(BG, (x_pos_bg, y_pos_bg))
        screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed 

    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(screen)
        player.update(userInput)

        background()
        score()

        if len(obstacles) == 0:
            rand_choice = random.randint(0, 4)
            if rand_choice in [0, 1]:
                obstacles.append(smallCactus(SMALL_CACTUS))
            elif rand_choice in [2, 3]:
                obstacles.append(largeCactus(LARGE_CACTUS))
            else:
               obstacles.append(Bird(BIRD))
        
        #if player.dino_rect.y < -50 or player.dino_rect.y > screen_height - player.dino_rect.height:
        #    run = False
         #   print("Game Over!")
          #  print(f"Your score: {points}")

        
        for obstacle in obstacles[:]:
            obstacle.draw(screen)
            obstacle.update()
            if obstacle.rect.x < -obstacle.rect.width:
                obstacles.remove(obstacle)
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(1000)
                death_count += 1
                menu(death_count)

        cloud.draw(screen)
        cloud.update()

        pygame.display.update()

def menu(death_count):
    global points
    run = True
    while run:
        screen.fill((255, 255, 255))
        font = pygame.font.SysFont('Arial', 20)

        if death_count == 0:
            text = font.render("Welcome to Super Dino. Press any key to start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render(f"Game Over! Press any key to restart", True, (0, 0, 0))
            score = font.render(f"Your score: {points}", True, (0, 0, 0))
            scoreRect = score.get_rect()
            #scoreRect.center = (800, 50)
            scoreRect.center = (screen_width // 2, screen_height // 2 + 50)
            screen.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (screen_width // 2, screen_height // 2)
        screen.blit(text, textRect)
        screen.blit(RUNNING[0], (screen_width // 2 - 20, screen_height // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
               # run = False
                main()

menu(death_count=0)
           