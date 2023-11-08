import pygame, sys

class Floor(pygame.sprite.Sprite):
    def __init__(self,group,posx):
        super().__init__(group)
        self.posx = posx
        
    def update(self):
        self.rect = pygame.draw.rect(screen, (0, 153, 153), (self.posx, 700, 100, 10))
        
        
class Player(pygame.sprite.Sprite):
    def __init__(self,group,pos):
        super().__init__(group)
        self.Radius = 30
        self.pos = pos
        self.speed = 10
        self.direction = pygame.math.Vector2(0.2,0)
        self.is_jumping = False
        self.kineticEnergy = 100


    def draw(self,camera):
        self.rect = pygame.draw.circle(screen, (128,255,0), self.pos- camera.offset, self.Radius)

    def input(self):
            
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.Radius += 10
            
        elif keys[pygame.K_a]:
            self.Radius -= 10

    def movement(self):
        if self.is_jumping == False:
            self.direction.y = 1

        if self.is_jumping == True:
            
            if self.kineticEnergy > 0:
                self.direction.y = -1
                self.kineticEnergy -= 2
            else:
                self.is_jumping = False
                self.direction.y = 1
                
        #print(self.is_jumping)    
            
    def FloorCollision(self):
        for Boden in Ground:
            if self.rect.colliderect(Boden.rect):
                #print("Test")
                self.pos[1] = 699-self.Radius
                self.direction.y *= -1
                self.is_jumping = True
                self.kineticEnergy = 100
        

    def update(self,camera):
            #self.movement()
            self.draw(camera)
            self.input()
            self.Radius = max(10, min(self.Radius, 1280//2,720//2))
            self.FloorCollision()
            self.movement()
            self.pos+= self.direction * self.speed
            #self.draw()
            
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.pos.x + int(self.width / 2)
        y = -target.pos.y + int(self.height / 2)

        # Keep the camera within the bounds of the level
        x = min(0, x)
        x = max(-(self.width - 1280), x)
        y = max(-(720 - self.height), y)
        y = min(0, y)

        self.camera = pygame.Rect(x, y, self.width, self.height)
        self.offset = pygame.Vector2(-x, -y)
        
background = pygame.image.load('Background.png')
camera = Camera(1280, 720)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.init()
all_sprites = pygame.sprite.Group()


Ground = []
for k in range(100,700,100):
    Ground.append(Floor(all_sprites,0+k))
Player = Player(all_sprites,(200,60))
running = True

while running: 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    #screen.fill("#0e69ab")
    Player.update(camera)
    camera.update(player)

    screen.blit(background, (0, 0))

    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))


    pygame.display.update()
    clock.tick(60)
