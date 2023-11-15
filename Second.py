import pygame
import sys

def Fliesenleger():
    
    if not camera.camera.colliderect(ground.rect):
            first_ground = grounds[0]
            all_sprites.remove(first_ground)
            first_ground.kill()
            last_ground = grounds[-1]
            last_posx = last_ground.posx

            new_ground = Floor(last_posx + 100)
            grounds.append(new_ground)
            all_sprites.add(new_ground)
        
        

            
class Floor(pygame.sprite.Sprite):
    def __init__(self, posx):
        super().__init__()
        self.image = pygame.Surface((100, 10))
        self.image.fill((0, 153, 153))
        self.posx = posx
        self.rect = self.image.get_rect(topleft=(self.posx, 700))
        


                

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.Radius = 30
        self.image = pygame.Surface((self.Radius * 2, self.Radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (128, 255, 0), (self.Radius, self.Radius), self.Radius)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)
        self.speed = 10
        self.direction = pygame.Vector2(0.2, 0)
        self.is_jumping = False
        self.kineticEnergy = 100

    def update_image(self):
        self.image = pygame.Surface((self.Radius * 2, self.Radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (128, 255, 0), (self.Radius, self.Radius), self.Radius)
        self.rect = self.image.get_rect(center=self.pos)


    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.Radius += 10

        elif keys[pygame.K_a]:
            self.Radius -= 10

    def movement(self):
        if not self.is_jumping:
            self.direction.y = 1

        if self.is_jumping:
            if self.kineticEnergy > 0:
                self.direction.y = -1
                self.kineticEnergy -= 2
            else:
                self.is_jumping = False
                self.direction.y = 1

    def floor_collision(self, grounds):
        for Boden in grounds:
            if self.rect.colliderect(Boden.rect):
                self.pos.y = 699 - self.Radius
                self.direction.y *= -1
                self.is_jumping = True
                self.kineticEnergy = 100

    def update(self, grounds):
        self.input()
        self.Radius = max(10, min(self.Radius, 1280 // 2, 720 // 2))
        self.floor_collision(grounds)
        self.movement()
        self.pos += self.direction * self.speed
        self.update_image()
        
class Camera:
    def __init__(self, width, height, view_width, view_height):
        self.camera = pygame.Rect(0, 0, view_width, view_height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.pos.x + int(self.camera.width / 2)
        y = -target.pos.y + int(self.camera.height / 2)


        self.camera = pygame.Rect(x, y, self.camera.width, self.camera.height)


background = pygame.image.load('background.png')
camera = Camera(1280, 720, 900, 1024)
screen = pygame.display.set_mode((1024, 1024))
clock = pygame.time.Clock()
pygame.init()
all_sprites = pygame.sprite.Group()

grounds = []
for k in range(0, 700, 100):
    ground = Floor(0 + k)
    grounds.append(ground)
    all_sprites.add(ground)

player = Player((200, 60))
#all_sprites.add(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    Fliesenleger()
    player.update(grounds)
    camera.update(player)
    all_sprites.update()
    #print(camera.camera.topleft)
    background_rect = background.get_rect(topleft=(camera.camera.topleft[0],camera.camera.topleft[1]+grounds[-1].posx))
    screen.blit(background, background_rect)
    #screen.blit(background, (0, 0))
    #  screen.fill("#0e69ab")

    screen.blit(player.image, camera.apply(player))
    
    for Boden in grounds:
        screen.blit(Boden.image, camera.apply(Boden))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
