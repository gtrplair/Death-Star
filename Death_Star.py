import pygame
import random
import math

vec = pygame.math.Vector2

WIDTH = 600
HEIGHT = 800
FPS = 60

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
TURQUOISE = (67, 198, 219)
ORANGE = (255, 130, 0)
DARK_ORANGE = (255, 90, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Death Star")
clock = pygame.time.Clock()

#Sound initialisation
pygame.mixer.init(44100)
pygame.mixer.music.load('theme.wav')
pygame.mixer.music.play(6)

#Sound effects
effect = pygame.mixer.Sound('xw_blaster.wav') 
tie_blast = pygame.mixer.Sound('tie_blaster.wav')
tie_ex = pygame.mixer.Sound('tie_ex.wav')
wow = pygame.mixer.Sound('wow.wav')
rocket = pygame.mixer.Sound('rocket_launch1.wav')
shock = pygame.mixer.Sound('electriccurrent.wav')
pulse = pygame.mixer.Sound('pulse.wav')

#Player Images
xwleft = pygame.image.load("xwleft.png")
xwright = pygame.image.load("xwright.png")
xwnormal= pygame.image.load("xwnormal.png")
#Player missile image
player_missile = pygame.image.load('playermissile.png')
#Player missile explosion spritesheet
player_missile_ex = pygame.image.load('player_missile_ex.png').convert_alpha()
#Player laser image
player_laser = pygame.image.load('player_singlelaser1.png')  

#Enemy Images
#Block (first enemy)
block_image = pygame.image.load('intercept3.png').convert_alpha()
#Block Weapon
tie_laser = pygame.image.load('tie_laser.png')

#Bomber (second enemy)
#Bomber Images
bomber_image = pygame.image.load('bomber.png').convert_alpha()
#Bomber engine explosion spritesheet
bomberex = pygame.image.load('laserex.png').convert_alpha()
#Bomber engine fire images
puff1 = pygame.image.load('missilesmoke.png').convert()
puff2 = pygame.image.load('missilesmoke2.png').convert()
#Bomber wall impact explosion spritesheet
bomber_trench_explosion = pygame.image.load('bomber_trench_explosion.png').convert_alpha()
#Bomber missile images
missile_white = pygame.image.load('missile_white.png').convert_alpha()
missile_red = pygame.image.load('missile_red.png').convert_alpha()

#Turret
turret_image = pygame.image.load('turret3.png').convert_alpha()
scorch_image = pygame.image.load('scorch.png').convert_alpha() #Image for when Turret is destroyed
#Turret weapon
ion = pygame.image.load('ion2.png').convert_alpha()
#Effect when Turret hits Player spritesheets
electric2 = pygame.image.load('electric2.png')
electric1 = pygame.image.load('electric1.png')
#Turret Explosion spritesheet
turret_ex1 = pygame.image.load('turret_explosion2.png').convert_alpha()

#General explosion spritesheet
blowup = pygame.image.load('blowup.png').convert_alpha()
#General laser impact spritesheet
laserex = pygame.image.load('laserex.png').convert_alpha()

#Background image
trench_run = pygame.image.load('trench_scroll.png').convert()

#font
font_name = pygame.font.match_font('arial')

#Draw text function
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#Draw shield bar function
def draw_shield_bar(surf, x, y, shield_percent):
    if shield_percent < 0:
        shield_percent = 0
    if shield_percent > 100:
        shield_percent = 100
    shield_bar_length = 100
    shield_bar_height = 10
    fill = (shield_percent / 100) * shield_bar_length
    outline_rect = pygame.Rect(x, y, shield_bar_length + 1, shield_bar_height + 1)
    fill_rect = pygame.Rect(x, y, fill, shield_bar_height)
    pygame.draw.rect(surf, TURQUOISE , fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 3)
 

#Draw Health bar function
def draw_health_bar(surf, x, y, health_percent):
    if health_percent < 0:
        health_percent = 0
    health_bar_length = 100
    health_bar_height = 10
    fill = (health_percent / 100) * health_bar_length
    outline_rect = pygame.Rect(x, y, health_bar_length + 1, health_bar_height + 1)
    fill_rect = pygame.Rect(x, y, fill, health_bar_height)
    if health_percent <= 40:
        pygame.draw.rect(surf, RED, fill_rect)
    elif health_percent <= 60:
        pygame.draw.rect(surf, DARK_ORANGE, fill_rect)
    elif health_percent <= 80:
        pygame.draw.rect(surf, ORANGE, fill_rect)  
    else:
        pygame.draw.rect(surf, GREEN, fill_rect)         
    pygame.draw.rect(surf, WHITE, outline_rect, 3)
    
    
#Draw missile bar function
def draw_missile_bar(surf, x, y, missile_percent):
    if missile_percent < 0:
        missile_percent = 0
    if missile_percent > 100:
        missile_percent = 100
    missile_bar_length = 100
    missile_bar_height = 10
    fill = (missile_percent / 100) * missile_bar_length
    outline_rect = pygame.Rect(x, y, missile_bar_length + 1, missile_bar_height + 1)
    fill_rect = pygame.Rect(x, y, fill, missile_bar_height)
    pygame.draw.rect(surf, RED , fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 3)
    

#Background sprite 1
class Level1_Background1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = trench_run
        self.rect = self.image.get_rect()
        self.rect.y = -186
        self.pos = (self.rect.x, self.rect.y)
        self.vel = vec(0, 1)
        self.a = 0
        
    def update(self):
        self.pos += self.vel
        self.rect = self.pos
        #continuous scrolling
        if self.rect.y == 800:
            self.rect.y = -1172
            self.a += 1
            
        #Wave 2 function call
        if self.a == 3:
            Level2()
            self.a = 4
        #Wave 3 function call
        if self.a == 7:
            Level3()
            self.a = 8
               
#Background sprite 2
class Level1_Background2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = trench_run
        self.rect = self.image.get_rect()
        self.rect.y = -1172
        self.pos = (self.rect.x, self.rect.y)
        self.vel = vec(0, 1)
        
    def update(self):
        self.pos += self.vel
        self.rect = self.pos
        if self.rect.y == 800:
            self.rect.y = -1172     
            
#Player class
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = xwnormal
        self.rect = self.image.get_rect()
        self.radius = 24
        self.rect.center = (WIDTH/2,HEIGHT/2)
        self.pos = vec(WIDTH/2,HEIGHT/2)
        self.shoot_delay = 250
        self.shield = 100
        self.health = 100
        self.force = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.missile = 100
        self.collision_damage = 100
        self.laser_damage = 100
        self.rect.center = (WIDTH/2,HEIGHT - 100)
        self.pos = vec(WIDTH/2,HEIGHT - 100)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.friction = -0.2
        self.left_bound = 40
        self.right_bound = 510
        
    def kill(self):
        self.kill()
        
    #Making the player change images when moving
    def tilt(self):

        pressed = pygame.key.get_pressed() 
        if pressed[pygame.K_LEFT] and pressed[pygame.K_RIGHT]:
            self.image = xwnormal

        elif pressed[pygame.K_LEFT]:
            self.image = xwleft

        elif pressed[pygame.K_RIGHT]:
            self.image = xwright

        elif not pressed[pygame.K_RIGHT] and not pressed[pygame.K_LEFT]:
            self.image = xwnormal    
            
    #Shooting player lasers
    def shoot(self):
        now= pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            effect.play()            
            self.last_shot = now
            bulletleft = Bulletleft(self.rect.x + 3, self.rect.y + 25)
            all_sprites.add(bulletleft)
            bullets.add(bulletleft)
            bulletright = Bulletright(self.rect.x + 49, self.rect.y + 25) 
            all_sprites.add(bulletright)
            bullets.add(bulletright)
    
    #Shooting player missile
    def shootmissile(self):

        if self.missile >= 100:
            self.missile = 0
            playermissile = Playermissile(self.rect.centerx, self.rect.centery - 10)
            all_sprites.add(playermissile)
            playermissiles.add(playermissile)
            rocket.play()

    def update(self):
        
        #recharging missile
        player.missile += 0.8
        
        #Player motion
        self.acc = vec(0,0)
        pressed = pygame.key.get_pressed()          
        if pressed[pygame.K_LEFT] and self.rect.x >= self.left_bound:
            self.acc.x = - 1.2
            self.tilt()
        if pressed[pygame.K_RIGHT] and self.rect.x <= self.right_bound:
            self.acc.x = + 1.2
            self.tilt()
        if pressed[pygame.K_UP]and self.rect.y >=20:
            self.acc.y = - 1.2
        if pressed[pygame.K_DOWN] and self.rect.y <=733:
            self.acc.y = + 1.2  
        
        #Player physics to give smoother motion
        self.acc += self.vel * self.friction   
        self.vel += self.acc
        self.pos += self.vel + 0.2 * self.acc
        self.rect.center = self.pos
        
        #calling function to change player image when moving
        if pressed[pygame.K_RIGHT] and pressed[pygame.K_LEFT]:
            self.tilt()
        if not pressed[pygame.K_RIGHT] and not pressed[pygame.K_LEFT]:
            self.tilt()
        if pressed[pygame.K_SPACE]:
            self.shoot()
            
        #The player's shield regenerates unless it has been completely destroyed
        if self.shield <= 0:
            self.shield = 0
        elif self.shield > 100:
            self.shield = 100
        else:
            self.shield += 0.1
        if self.force <= 0:
            self.force += 0.08
        if self.force >= 100:
            self.force = 100
            
        #shooting player missile
        if pressed[pygame.K_v]:
            self.shootmissile()     
            
#Player left laser sprite            
class Bulletleft(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_laser
        self.rect = self.image.get_rect()
        self.radius = 3
        self.rect.bottom = y
        self.rect.centerx = x
        self.pos = (x, y)      
        self.vel = vec(0.3, -22)
        
    def update(self):
        #Impact effect with Block sprite
        hit_list = pygame.sprite.spritecollide(self, block, False, pygame.sprite.collide_circle)
        for bullets in hit_list:

            expl = Laserex(self.rect.left - 10, self.rect.top)
            all_sprites.add(expl)  
        
        #laser movement
        self.pos += self.vel
        self.rect.center = self.pos

        if self.rect.bottom < 0:
            self.kill()        
         
#Player right laser sprite     
class Bulletright(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_laser
        self.rect = self.image.get_rect()
        self.radius = 3
        self.rect.bottom = y
        self.rect.centerx = x        
        self.pos = (x, y)      
        self.vel = vec(-0.3, -22) 
        
    def update(self):
        #Impact effect with Block sprite
        hit_list = pygame.sprite.spritecollide(self, block, False, pygame.sprite.collide_circle)
        for bullets in hit_list:
            expl = Laserex(self.rect.left-16, self.rect.top)
            all_sprites.add(expl) 
            
        #laser movement
        self.pos += self.vel
        self.rect.center = self.pos

        if self.rect.bottom < 0:
            self.kill()        

#First enemy sprite
class Block(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = block_image
        self.rect = self.image.get_rect()
        self.radius = 27
        self.rect.centerx = x
        self.rect.centery = y
        self.shoot_delay = 200
        self.burst_delay = random.randrange(1500, 3000)
        self.last_shot = pygame.time.get_ticks()
        self.last_burst = pygame.time.get_ticks()
        self.health = 6
        self.pos = (self.rect.centerx, self.rect.centery)
        self.vel = vec(0, 1.5)        
        self.acc = vec(0, 0)
        self.shots = random.randrange(1, 2)

    #When Block health goes to 0
    def shot(self):
        expl = Blowup(self.rect.left -37, self.rect.top-37)
        self.kill() 
        all_sprites.add(expl)         
        
    #if Block collides with Player
    def collision(self):
        expl = Blowup(self.rect.left -37, self.rect.top-37)
        self.kill() 
        wow.play()         
        all_sprites.add(expl) 
        if player.shield >= 0:
            player.shield -= 40
            player.collision_damage = player.shield
            if player.shield <= 0:
                player.health += player.collision_damage
                player.collision_damage = 0
                player.health -= 20   
            
    def update(self):
             
        #Block movement
        self.pos += self.vel
        self.rect.center = self.pos                  
        if self.rect.top > HEIGHT+10:
            self.kill()    
            
        #Block collision with player lasers
        hit_list = pygame.sprite.spritecollide(self, bullets, True, pygame.sprite.collide_circle)
        for block in hit_list:
            self.health -= 1
            self.rect.y -= 2
        
            if self.health == 0:
                tie_ex.play()                 
                expl = Blowup(self.rect.left -37, self.rect.top-37)
                self.kill()
                all_sprites.add(expl) 
        
        #calling collision function
        hits = pygame.sprite.spritecollide(self, [player], False, pygame.sprite.collide_circle)
        for hit in hits:
            tie_ex.play()                     
            self.collision()
        
        #repeating lasers
        now = pygame.time.get_ticks()        
        if self.shots > 0:
            if now - self.last_shot > self.shoot_delay and self.rect.y > random.randrange(0, 170):        
                tielaser = Tielaser(self.rect.centerx, self.rect.bottom - 10) 
                all_sprites.add(tielaser)
                lasers.add(tielaser)
                self.shots -= 1
                self.last_shot = now
                
        #reloading lasers
        elif self.shots <= 0:
            reload = pygame.time.get_ticks()
            if reload - self.last_burst > self.burst_delay:
                self.shots = 3
                self.last_burst = reload                
                
#Block lasers
class Tielaser(pygame.sprite.Sprite):

    def __init__(self, x, y):   
        pygame.sprite.Sprite.__init__(self)    
        self.image = tie_laser
        self.rect = self.image.get_rect()
        self.radius = 3
        self.rect.centery = y + 10 
        self.rect.centerx = x     
        tie_blast.play()

        
    def update(self):
        self.rect.y += 12 
        if self.rect.top > 800:
            self.kill()       
            
        #Player damage on collision
        hit_list = pygame.sprite.spritecollide(self, [player], False)
        for tielaser in hit_list:
            if player.shield >= 0:
                player.shield -= 5
                if player.shield <= 0:
                    player.health -= 5
                    
            #spritesheet impact animation
            expl = Laserex(self.rect.centerx - 15, self.rect.centery)
            all_sprites.add(expl)
            self.kill()


#Bomber class (2nd enemy)
class Bomber(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bomber_image
        self.rect = self.image.get_rect()
        self.radius = 30
        pygame.draw.circle(self.image, RED, (self.rect.centerx, self.rect.centery - 25), 3)     
        self.rect.centerx = x
        self.rect.centery = y        
        self.pos = (self.rect.centerx, self.rect.centery)
        self.vel = vec(0, 1.5)
        self.shoot_delay = random.randrange(8000, 12000)
        self.last_shot = pygame.time.get_ticks()
        self.last_burst=pygame.time.get_ticks()
        self.health = 10
        self.death_time = 1
        self.last_smoke = pygame.time.get_ticks()
        self.smoke_delay = 30       
        self.rotate = 1
        self.direction = random.randrange(-10,10)
        self.deathspin = 1  
        self.trench_left = 150 
        self.trench_right = 450
        self.crash = random.randrange(0, 2)

    #shooting missile
    def shoot(self):
        missile = Missile(self.rect.right, self.rect.bottom) 
        all_sprites.add(missile)
        missiles.add(missile) 
  
    #Sprite rotation and engine explosion when health is 0 or below. 
    def shot(self):
        
        #randomly choosing direction and amount of rotation and adding engine explosion
        if self.direction < 0:
            self.image = pygame.transform.rotate(self.image, random.randrange(4, 10))
        else:
            self.image = pygame.transform.rotate(self.image, random.randrange(-10, -4))         
        expl5 = Bomberex(self.rect.left, self.rect.top + 10)
        all_sprites.add(expl5)        

    #Collision with Player
    def collision(self):
        expl = Blowup(self.rect.left -37, self.rect.top-37)
        self.kill() 
        all_sprites.add(expl) 
        wow.play() 
        if player.shield >= 0:
            player.shield -= 40
            player.collision_damage = player.shield
            if player.shield <= 0:
                player.health += player.collision_damage
                player.collision_damage = 0
                player.health -= 20    
                
        
    def update(self):
        
        #Bomber movement
        self.pos += self.vel
        self.rect.center = self.pos
        
        if self.rect.centerx < -10 or self.rect.centerx > 610 or self.rect.centery > 810:
            self.kill()            
 
        #Randomly setting the Bomber to crash into the wall or not. With different levels, this would have remained the same depending on the context.
        if self.crash == 0:
            #left wall collision
            if self.rect.centerx <= self.trench_left:
                t_ex = Bomber_T_Ex(153, self.rect.centery - 20, 270)
                self.kill()
                all_sprites.add(t_ex)
            
            #right wall collision
            if self.rect.centerx >= self.trench_right:
                t_ex = Bomber_T_Ex(375, self.rect.centery - 20, 90)
                self.kill()  
                all_sprites.add(t_ex)

        #If Bomber still has health (before engine explosion), it can collide with the Player and collide with Player lasers.
        if self.health > 0:
            hits = pygame.sprite.spritecollide(self, [player], False, pygame.sprite.collide_circle)
            for hit in hits:            
                self.collision() 
                
            hit_list = pygame.sprite.spritecollide(self, bullets, True, pygame.sprite.collide_circle)
            for bomber in hit_list:

                self.health -= 1
                self.rect.y -= 2
                if self.health == 0:
                    self.shot()
            for bulletleft in hit_list:
                expl = Laserex(bulletleft.rect.left - 10, self.rect.top + 8)
                all_sprites.add(expl)   

        #Firing missiles
        if self.rect.bottom > 10 and self.health > 0:
            now = pygame.time.get_ticks()

            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                missile = Missile(self.rect.centerx, self.rect.bottom - 10) 
                all_sprites.add(missile)
                missiles.add(missile)


        #If health is gone, engine explodes and begins smoking, and collisions become possible with other enemies or the trench "wall". Collisions with Player do not occur.
        if self.health <= 0:
            now = pygame.time.get_ticks()
            if now - self.last_smoke > self.smoke_delay:
                self.last_smoke = now
                bombersmoke2 = BomberSmoke2(self.rect.centerx + 15 , self.rect.bottom + 13) 
                all_sprites.add(bombersmoke2)
                smokes.add(bombersmoke2)                
                bombersmoke = BomberSmoke(self.rect.centerx + 15 , self.rect.bottom + 13) 
                all_sprites.add(bombersmoke)
                smokes.add(bombersmoke)            
            self.deathspin -= 0.1   
            if self.direction < 0:
                self.vel -= vec(0.01, (random.randrange(-2,3)/100)) * self.deathspin
            else:
                self.vel += vec(0.01, (random.randrange(-2,3)/100)) * self.deathspin
                
            enemy_hit = pygame.sprite.spritecollide(self, block, False, pygame.sprite.collide_circle)
            for bomber in enemy_hit:
                expl = Blowup(self.rect.left -37, self.rect.top-37)
                all_sprites.add(expl)
                self.kill()                 
            for self in enemy_hit:
                self.shot() 
                
            turret_hit = pygame.sprite.spritecollide(self, turrets, False, pygame.sprite.collide_circle)
            for turret in turret_hit:
                expl = Blowup(self.rect.left -37, self.rect.top-37)        
                self.shot()
                self.kill()
            for self in turret_hit:
                self.shot()                
                

#Turret class (3rd enemy)
class Turret(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = turret_image
        self.original = self.image
        self.rect = self.image.get_rect()
        self.radius = 35
        self.rect.x = x
        self.rect.y = y     
        self.shoot_delay = 5000
        self.burst_delay =1500
        self.last_shot = pygame.time.get_ticks()
        self.health = 10
        self.pos = vec(self.rect.centerx, self.rect.centery)
        self.rect.center = self.pos
        self.rotate = 0
        self.last_rotate = pygame.time.get_ticks()
        self.rotate_delay = 50
        self.rotate_angle = 0
        self.blast_angle =0
        self.angle = 0
        self.vel= vec(0, 1)

    #Rotating sprite to follow Player
    def rotation(self):
 
        self.rotate_angle = (player.pos - self.pos).angle_to(vec(1,0))
        self.image = self.original
        self.image = pygame.transform.rotozoom(self.image, self.rotate_angle, 1)
        self.blast_angle = (player.pos - self.pos).angle_to(vec(1,0))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.angle = self.rotate_angle              
    
    #When Turret health falls to 0, it is destroyed
    def shot(self):

        self.rect.center = (self.rect.centerx, self.rect.centery)
        a = self.rect.center       
        expl2 = Turret_Ex1(a)
        all_sprites.add(expl2)
        self.image = scorch_image
        self.rect = self.image.get_rect()
        self.rect.center = a
        self.rect.center = (self.rect.centerx + 70, self.rect.centery + 70)
        self.radius = 0.01


    def update(self):
        
        #Turret movement. It moves at the same speed as the background.
        self.pos += self.vel
        self.rect.center = self.pos
        
        #Activating rotation and shooting once Turret is onscreen.
        if self.rect.bottom > 10 and self.health > 0:
            now = pygame.time.get_ticks()
            self.rotate_angle = 0
            new_rotate = pygame.time.get_ticks() 
            
            if new_rotate - self.last_rotate > self.rotate_delay:
                self.last_rotate = new_rotate
                self.rotation()            
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                ion = Ion(self.rect.centerx, self.rect.centery, self.blast_angle)
                all_sprites.add(ion)
                ions.add(ion)

        #Collisions with Player lasers
        if self.rect.top > HEIGHT+10:
            self.kill()
        hit_list = pygame.sprite.spritecollide(self, bullets, True, pygame.sprite.collide_circle)
        for turret in hit_list:
            self.health -= 1
            if self.health == 0:
                self.shot() 
                tie_ex.play()
                
        for bulletleft in hit_list:
            expl = Laserex(bulletleft.rect.left - 10, self.rect.top + 42)
            all_sprites.add(expl)   
            
            
#Turret explosion animation, randomly rotated.
class Turret_Ex1 (pygame.sprite.Sprite):

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        rotate = random.randrange(1, 360)
        self.sheet = turret_ex1
        self.rotate = random.randrange(1,359)

        self.turret_ex1_anim_pos = [
            pygame.Rect(0, 0, 128, 128),
            pygame.Rect(128, 0, 128, 128),
            pygame.Rect(256, 0, 128, 128),
            pygame.Rect(384, 0, 128, 128),
            pygame.Rect(512, 0, 128, 128),
            pygame.Rect(0, 128, 128, 128),
            pygame.Rect(128, 128, 128, 128),
            pygame.Rect(256, 128, 128, 128),
            pygame.Rect(384, 128, 128, 128),
            pygame.Rect(512, 128, 128, 128),       
            pygame.Rect(0, 256, 128, 128),
            pygame.Rect(128, 256, 128, 128),
            pygame.Rect(256, 256, 128, 128),
            pygame.Rect(384, 256, 128, 128),
            pygame.Rect(512, 256, 128, 128),            
            pygame.Rect(0, 384, 128, 128),
            pygame.Rect(128, 384, 128, 128),
            pygame.Rect(256, 384, 128, 128),
            pygame.Rect(384, 384, 128, 128),
            pygame.Rect(512, 384, 128, 128),
            pygame.Rect(640, 384, 128, 128),
            pygame.Rect(0, 512, 128, 128),
            pygame.Rect(128, 512, 128, 128),
            pygame.Rect(256, 512, 128, 128),
            pygame.Rect(384, 512, 128, 128),
            pygame.Rect(512, 512, 128, 128),
            pygame.Rect(640, 512, 128, 128),            
            ]
        self.turret_ex1_anim = []
        for pos in self.turret_ex1_anim_pos:
            img = pygame.Surface((128, 128), pygame.SRCALPHA, 32)
            img.blit(self.sheet, (0, 0), pos)
            self.turret_ex1_anim.append(img)
        self.image = self.turret_ex1_anim[0]

        self.rect = self.image.get_rect()
        self.rect.center = position
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 10
        self.image = pygame.transform.rotate(self.image, self.rotate)
        self.rect.center = position
        tie_ex.play()                 

        
       
    def update(self):
        a = self.rect.center
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.image = self.turret_ex1_anim[self.frame]
            self.image = pygame.transform.rotate(self.image, self.rotate)
            self.rect.center = a
            self.frame += 1
            if self.frame == 27:
                self.kill()
        self.frame_rate = 18
        self.rect.y += 1

            
                
#Explosion animation used by multiple sprites, randomly rotated.
class Blowup (pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        rotate = random.randrange(1, 360)
        self.sheet = blowup
        self.rotate = random.randrange(1,359)
        self.blowup_anim_pos = [
            pygame.Rect(0, 0, 128, 128),
            pygame.Rect(128, 0, 128, 128),
            pygame.Rect(128, 0, 128, 128),
            pygame.Rect(256, 0, 128, 128),
            pygame.Rect(256, 0, 128, 128),
            pygame.Rect(384, 0, 128, 128),
            pygame.Rect(384, 0, 128, 128),
            pygame.Rect(128, 128, 128, 128),
            pygame.Rect(128, 128, 128, 128),
            pygame.Rect(256, 128, 128, 128),
            pygame.Rect(256, 128, 128, 128),
            pygame.Rect(384, 128, 128, 128),
            pygame.Rect(384, 128, 128, 128),
            pygame.Rect(0, 256, 128, 128),
            pygame.Rect(0, 256, 128, 128),
            pygame.Rect(128, 256, 128, 128),
            pygame.Rect(128, 256, 128, 128),
            pygame.Rect(256, 256, 128, 128),
            pygame.Rect(256, 256, 128, 128),
            pygame.Rect(384, 256, 128, 128),
            pygame.Rect(384, 256, 128, 128),
            pygame.Rect(0, 384, 128, 128),
            pygame.Rect(0, 384, 128, 128),
            pygame.Rect(128, 384, 128, 128),
            pygame.Rect(128, 384, 128, 128),
            pygame.Rect(256, 384, 128, 128),
            pygame.Rect(256, 384, 128, 128),
            pygame.Rect(384, 384, 128, 128),
            pygame.Rect(384, 384, 128, 128),
            ]
        self.blowup_anim = []
        for pos in self.blowup_anim_pos:
            img = pygame.Surface((128, 128), pygame.SRCALPHA, 32)
            img.blit(self.sheet, (0, 0), pos)
            self.blowup_anim.append(img)
        self.image = self.blowup_anim[0]
        self.rect = self.image.get_rect()
        self.rect = (x, y)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 20
        self.image = pygame.transform.rotate(self.image, self.rotate)
        self.rect = (x, y)
        tie_ex.play()                 
       
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.image = self.blowup_anim[self.frame]
            self.image = pygame.transform.rotate(self.image, self.rotate)
            self.frame += 1
            if self.frame == 29:
                self.kill()
        self.frame_rate = 30


#Player Missile explosion animation, randomly rotated.
class PlayerMissileEx (pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        rotate = random.randrange(1, 360)
        self.sheet = player_missile_ex
        self.rotate = random.randrange(1,359)
        self.player_missile_ex_anim_pos = [
            pygame.Rect(0, 0, 128, 128),
            pygame.Rect(384, 0, 128, 128),
            pygame.Rect(512, 0, 128, 128),
            pygame.Rect(640, 0, 128, 128), 
            pygame.Rect(0, 128, 128, 128),
            pygame.Rect(128, 128, 128, 128),
            pygame.Rect(256, 128, 128, 128),
            pygame.Rect(640, 128, 128, 128),
            pygame.Rect(768, 128, 128, 128), 
            pygame.Rect(128, 256, 128, 128),
            pygame.Rect(256, 256, 128, 128),
            pygame.Rect(384, 256, 128, 128),
            pygame.Rect(768, 256, 128, 128),  
            pygame.Rect(896, 256, 128, 128),            
            pygame.Rect(128, 384, 128, 128),
            pygame.Rect(256, 384, 128, 128),
            pygame.Rect(512, 384, 128, 128),  
            pygame.Rect(640, 384, 128, 128),
            pygame.Rect(768, 384, 128, 128),
            pygame.Rect(0, 512, 128, 128),
            pygame.Rect(128, 512, 128, 128),
            pygame.Rect(256, 512, 128, 128),
            pygame.Rect(384, 512, 128, 128),
            pygame.Rect(512, 512, 128, 128),  
            pygame.Rect(640, 512, 128, 128), 
            pygame.Rect(768, 512, 128, 128),  
            pygame.Rect(896, 512, 128, 128),
            pygame.Rect(0, 640, 128, 128),
            pygame.Rect(128, 640, 128, 128),
            pygame.Rect(256, 640, 128, 128),
            pygame.Rect(384, 640, 128, 128),
            pygame.Rect(512, 640, 128, 128),  
            pygame.Rect(640, 640, 128, 128), 
            pygame.Rect(768, 640, 128, 128),  
            pygame.Rect(896, 640, 128, 128)              
            ]
        self.player_missile_ex_anim = []
        for pos in self.player_missile_ex_anim_pos:
            img = pygame.Surface((128, 128), pygame.SRCALPHA, 32)
            img.blit(self.sheet, (0, 0), pos)
            self.player_missile_ex_anim.append(img)
        self.image = self.player_missile_ex_anim[0]
        self.rect = (x, y)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 8
        self.image = pygame.transform.rotate(self.image, self.rotate)
        self.rect = (x, y)
        self.image = pygame.transform.scale(self.image, (120,120)) 
        self.pos = self.rect
        tie_ex.play()       
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.image = self.player_missile_ex_anim[self.frame]
            self.image = pygame.transform.rotate(self.image, self.rotate)
            self.rect=self.pos
            self.image = pygame.transform.scale(self.image, (120,120)) 
            self.frame += 1            
            if self.frame == 35:
                self.kill()
        self.frame_rate = 10


#Laser impact animation
class Laserex (pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rotate = random.randrange(1, 360)
        self.sheet = laserex
        self.laserex_anim_pos = [
            pygame.Rect(0, 96, 32, 32),
            pygame.Rect(32, 96, 32, 32),
            pygame.Rect(64, 96, 32, 32),
            pygame.Rect(96, 96, 32, 32),
            pygame.Rect(128, 96, 32, 32),
            pygame.Rect(160, 96, 32, 32),
            pygame.Rect(192, 96, 32, 32),
            pygame.Rect(225, 96, 32, 32)
            ]
        self.laserex_anim = []
        for pos in self.laserex_anim_pos:
            img = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
            img.blit(self.sheet, (0, 0), pos)
            self.laserex_anim.append(img)
        self.image = self.laserex_anim[0]
        self.rect = (x - 10, y - 10)
        self.image = pygame.transform.rotate(self.image, self.rotate)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()   
        self.frame_rate = 20
        self.pos = self.rect
        
    def update(self):

        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now

            self.image = self.laserex_anim[self.frame]
            self.image = pygame.transform.rotate(self.image, self.rotate)
            self.frame += 1

            if self.frame == 8:
                self.kill()
        self.frame_rate = 50
        self.rect = self.pos
        
        
#Bomber trench wall explosion
class Bomber_T_Ex (pygame.sprite.Sprite):

    def __init__(self, x, y, side):
        pygame.sprite.Sprite.__init__(self)
        self.rotate = side
        self.sheet = bomber_trench_explosion
        self.Bomber_T_Ex_anim_pos = [
            pygame.Rect(0, 0, 96, 96),
            pygame.Rect(96, 0, 96, 96),
            pygame.Rect(192, 0, 96, 96),
            pygame.Rect(288, 0, 96, 96),
            pygame.Rect(384, 0, 96, 96),
            pygame.Rect(0, 96, 96, 96),
            pygame.Rect(96, 96, 96, 96),
            pygame.Rect(192, 96, 96, 96),
            pygame.Rect(288, 96, 96, 96),
            pygame.Rect(384, 96, 96, 96),
            pygame.Rect(0, 192, 96, 96),
            pygame.Rect(96, 192, 96, 96),
            pygame.Rect(192, 192, 96, 96),
            pygame.Rect(288, 192, 96, 96),
            pygame.Rect(384, 192, 96, 96)          
            ]
        self.Bomber_T_Ex_anim = []
        for pos in self.Bomber_T_Ex_anim_pos:
            img = pygame.Surface((96, 96), pygame.SRCALPHA, 32)
            img.blit(self.sheet, (0, 0), pos)
            self.Bomber_T_Ex_anim.append(img)
        self.image = self.Bomber_T_Ex_anim[0]
        self.rect = (x - 10, y - 10)
        self.image = pygame.transform.rotate(self.image, self.rotate)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()   
        self.frame_rate = 10
        self.pos = self.rect
        self.vel = vec(0, 1)
        tie_ex.play()                 
        
    def update(self):
        self.pos += self.vel
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now

            self.image = self.Bomber_T_Ex_anim[self.frame]
            self.image = pygame.transform.rotate(self.image, self.rotate)
            self.frame += 1

            if self.frame == 15:
                self.kill()
        self.frame_rate = 30
        self.rect = self.pos
        
        
#Ion impact with Player, electric animation 1
class Electric1 (pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = electric1
        self.electric1_anim_pos = [
            pygame.Rect(0, 0, 60, 60),
            pygame.Rect(60, 0, 60, 60),
            pygame.Rect(120, 0, 60, 60),
            pygame.Rect(180, 0, 60, 60),
            pygame.Rect(240, 0, 60, 60),
            pygame.Rect(0, 60, 60, 60),
            pygame.Rect(60, 60, 60, 60),
            pygame.Rect(120, 60, 60, 60),
            pygame.Rect(180, 0, 60, 60),
            pygame.Rect(240, 0, 60, 60),
            pygame.Rect(0, 60, 60, 60),
            pygame.Rect(60, 60, 60, 60), 
            pygame.Rect(60, 0, 60, 60),
            pygame.Rect(120, 0, 60, 60),
            pygame.Rect(180, 0, 60, 60),
            pygame.Rect(240, 0, 60, 60),            
            ]
        self.electric1_anim = []
        for pos in self.electric1_anim_pos:
            img = pygame.Surface((60, 60), 32)
            img.blit(self.sheet, (0, 0), pos)
            self.electric1_anim.append(img)
        self.image = self.electric1_anim[0]
        img = pygame.Surface.set_colorkey(self.image, BLACK)
        self.rect = (x, y)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()   
        self.frame_rate = 20

    def update(self):
        self.rect = (player.rect.centerx-20, player.rect.centery-30)
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now

            self.image = self.electric1_anim[self.frame]
            img = pygame.Surface.set_colorkey(self.image, BLACK)
            self.frame += 1

            if self.frame == 16:
                self.kill()
        self.frame_rate = 50

#Ion impact with Player, electric animation 2
class Electric2 (pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = electric2
        self.electric2_anim_pos = [
            pygame.Rect(0, 0, 60, 60),
            pygame.Rect(60, 0, 60, 60),
            pygame.Rect(0, 120, 60, 60),
            pygame.Rect(60, 120, 60, 60),
            pygame.Rect(0, 180, 60, 60),
            pygame.Rect(60, 180, 60, 60),
            pygame.Rect(0, 240, 60, 60),
            pygame.Rect(60, 240, 60, 60),
            pygame.Rect(60, 0, 60, 60),
            pygame.Rect(0, 120, 60, 60),
            pygame.Rect(60, 120, 60, 60),
            pygame.Rect(0, 180, 60, 60), 
            pygame.Rect(60, 240, 60, 60),
            pygame.Rect(60, 0, 60, 60),
            pygame.Rect(0, 120, 60, 60),
            pygame.Rect(60, 120, 60, 60),            
            ]
        self.electric2_anim = []
        for pos in self.electric2_anim_pos:
            img = pygame.Surface((60, 60), 32)
            img.blit(self.sheet, (0, 0), pos)
            self.electric2_anim.append(img)
        self.image = self.electric2_anim[0]
        img = pygame.Surface.set_colorkey(self.image, BLACK)
        self.rect = (x, y)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()   
        self.frame_rate = 20

    def update(self):
       
        self.rect = (player.rect.centerx - 35, player.rect.centery-20)
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now

            self.image = self.electric2_anim[self.frame]
            img = pygame.Surface.set_colorkey(self.image, BLACK)
            self.frame += 1

            if self.frame == 16:
                self.kill()
        self.frame_rate = 50
        

#Bomber engine explosion animation
class Bomberex (pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        rotate = random.randrange(1, 360)
        self.sheet = bomberex
        self.sheet.set_colorkey((0,0,0))    
        self.bomberex_anim_pos = [
            pygame.Rect(0, 32, 32, 32),
            pygame.Rect(32, 32, 32, 32),
            pygame.Rect(64, 32, 32, 32),
            pygame.Rect(96, 32, 32, 32),
            pygame.Rect(128, 32, 32, 32),
            pygame.Rect(160, 32, 32, 32),
            pygame.Rect(192, 32, 32, 32),
            pygame.Rect(225, 32, 32, 32)
            ]
        self.bomberex_anim = []
        for pos in self.bomberex_anim_pos:
            img = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
            img.blit(self.sheet, (0, 0), pos)
            self.bomberex_anim.append(img)
        self.image = self.bomberex_anim[0]
        self.image = pygame.transform.scale(self.image, (150, 150)) 
        self.rect = (x, y)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()   
        self.frame_rate = 60

    def update(self):

        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.image = self.bomberex_anim[self.frame]
            self.image = pygame.transform.scale(self.image, (150,150)) 
            self.frame += 1
            if self.frame == 7:
                self.kill()
        self.frame_rate = 60

            
#Bomber missile class   
class Missile(pygame.sprite.Sprite):
    def __init__(self,x,y): 
        pygame.sprite.Sprite.__init__(self)    
        self.image = missile_white
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 6
        self.rect.centery = y + 35  
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = x        
        self.pos = (self.rect.centerx, self.rect.centery)
        self.vel = vec(0,4)
        self.acc = vec(0,0)
        self.friction = -0.013
        self.last_smoke = pygame.time.get_ticks()
        self.smoke_delay = 30     
        self.birth = pygame.time.get_ticks()
        self.death_delay = 10000
        self.enemy_collide = 0

    def update(self):
        
        #Smoke trail is created
        now = pygame.time.get_ticks()
        if now - self.last_smoke > self.smoke_delay:
            self.last_smoke = now
            smoke = Smoke(self.rect.centerx + 28 , self.rect.bottom + 23) 
            all_sprites.add(smoke)
            smokes.add(smoke)          
        
        #Missile explodes after a certain time
        current_age = pygame.time.get_ticks()
        if current_age - self.birth > self.death_delay:
            self.kill()
            expl = Blowup(self.rect.centerx - 85 , self.rect.bottom - 87) 
            all_sprites.add(expl)
             
        #Missile follows player with basic AI
        self.acc = vec(0,0)
        pressed = pygame.key.get_pressed()          
        if self.rect.x > player.rect.x:
            self.acc.x = - 0.07

        elif self.rect.x < player.rect.x:
            self.acc.x = + 0.07

        if self.rect.y > player.rect.y:
            self.acc.y = - 0.07
        elif self.rect.y < player.rect.y:
            self.acc.y = + 0.07 
        
        self.acc += self.vel*self.friction   
        self.vel += self.acc
        self.pos += self.vel + 0.8 * self.acc
        self.rect.center = self.pos
        
        
        #If missile gets close enough to Player, it is activated
        if abs(self.rect.x - player.rect.x) < 70 and abs(self.rect.y - player.rect.y) < 70:
            self.enemy_collide = 1
            self.image = missile_red
            
        #It can then collide with other enemies such as Block and Turret
        if self.enemy_collide == 1:
            
            hit_list5 = pygame.sprite.spritecollide(self, block, False, pygame.sprite.collide_circle)       
            for missiles in hit_list5:
                expl2 = Blowup(self.rect.left-46, self.rect.top-29)
                all_sprites.add(expl2) 
                self.kill()
            for self in hit_list5:
                self.shot()
        
            hit_list3 = pygame.sprite.spritecollide(self, turrets, False, pygame.sprite.collide_circle)
            for missiles in hit_list3:
                expl2 = Blowup(self.rect.left-46, self.rect.top-29)
                all_sprites.add(expl2)
                self.kill()
            for self in hit_list3:
                self.health -= 5
                self.shot()             
                     
        
        #Collision with Player
        hit_list = pygame.sprite.spritecollide(self, [player], False)
        for hit in hit_list:
            self.kill()
            
            wow.play() 
            expl2 = Blowup(self.rect.left-46, self.rect.top-29)
            all_sprites.add(expl2) 
            if player.shield >= 0:
                player.shield -= 20
                player.collision_damage = player.shield
                if player.shield <= 0:
                    player.health += player.collision_damage
                    player.collision_damage = 0
                    player.health -= 20      
                    
        #Collision with Player lasers
        hit_list6 = pygame.sprite.spritecollide(self, bullets, True, pygame.sprite.collide_circle)
        for hit in hit_list6:
            self.kill()
            expl2 = Blowup(self.rect.left - 60, self.rect.top - 60)
            all_sprites.add(expl2) 
            

#Turret laser sprite. 
class Ion(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)    
        self.image = ion
        self.rect = self.image.get_rect()
        self.radius = 15
        self.rect.centery = y 
        self.rect.centerx = x       
        self.pos = (self.rect.centerx, self.rect.centery)
        self.vel = pygame.math.Vector2.normalize(player.pos-self.pos) * 14
        self.rotate_angle = angle #Rotated in the direction of the Player. Rotation angle is passed from Turret when it creates instance of this class.
        self.image = pygame.transform.rotate(self.image, self.rotate_angle)
        self.rect = self.image.get_rect()
        self.pos = self.pos + self.vel * 3
        pulse.play()
        

    def update(self):

        if self.rect.centerx < -10 or self.rect.centerx > 610 or self.rect.centery < -10 or self.rect.centery > 810:
            self.kill()
        self.rect.center = self.pos + self.vel * 2
        self.pos += self.vel
        
        #Impact animation with Player
        hit_list = pygame.sprite.spritecollide(self, [player], False, pygame.sprite.collide_circle)
        for hit in hit_list:
            self.kill()
            elec1 = Electric1(player.rect.centerx-20, player.rect.centery-30)
            all_sprites.add(elec1) 
            elec2 = Electric2(player.rect.centerx - 35, player.rect.centery-20)
            all_sprites.add(elec2)
            player.shield -= 30
            shock.play()


#Player missile class
class Playermissile(pygame.sprite.Sprite):
    def __init__(self,x,y): 
        pygame.sprite.Sprite.__init__(self)    
        self.image = player_missile
        self.rect = self.image.get_rect()
        self.radius = 5
        self.rect.centery = y + 5  
        self.rect.centerx = x        
        self.acceleration = 0.5
        self.last_smoke = pygame.time.get_ticks()
        self.smoke_delay = 1  
        self.pos = self.rect.center
        self.vel = vec(0, -3)
        self.acc = vec(0, -0.005)
        self.friction = 0.001      

    def update(self):
        
        self.acc += self.vel * self.friction   
        self.vel += self.acc
        self.pos += self.vel + 0.01 * self.acc
        self.rect.center = self.pos       
        now = pygame.time.get_ticks()
        
        #Smoke trail creation
        if now - self.last_smoke > self.smoke_delay:
            self.last_smoke = now
            smoke = Smoke(self.rect.centerx + 28 , self.rect.bottom + 13) 
            all_sprites.add(smoke)
            smokes.add(smoke)                
            
        #Collisions with Block, Bomber and Turret
        hit_list = pygame.sprite.spritecollide(self, block, False, pygame.sprite.collide_circle)       
        for playermissiles in hit_list:
            expl = PlayerMissileEx(self.rect.left-50, self.rect.top-65)
            all_sprites.add(expl) 
            self.kill()
        for self in hit_list:
            self.shot()

        hit_list2 = pygame.sprite.spritecollide(self, bomber, False, pygame.sprite.collide_circle)
        for playermissiles in hit_list2:
            expl = PlayerMissileEx(self.rect.left-65, self.rect.top-80)
            all_sprites.add(expl) 
            self.kill()
        for self in hit_list2:
            self.health = 0
            self.shot()     
        if self.rect.bottom < 0:
            self.kill()    
            
        hit_list3 = pygame.sprite.spritecollide(self, turrets, False, pygame.sprite.collide_circle)
        for playermissiles in hit_list3:
            expl = PlayerMissileEx(self.rect.left-65, self.rect.top-80)
            all_sprites.add(expl) 
            self.kill()
        for self in hit_list3:
            self.health -= 5
            self.shot()
        
#Smoke class for missile trails
class Smoke(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)    

        self.image = puff1
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, (10,10))     
        self.image = pygame.transform.rotate(self.image, random.randrange(1,50))
        self.a = 8
        self.c = random.randrange(75,95)
        self.shoot_delay = 500
        self.last_shot = pygame.time.get_ticks()   
        self.rect.centerx = x     
        self.rect.centery = y
      
    def update(self):
        
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.image = pygame.transform.scale(self.image, (self.a,self.a))
            self.a+=3
        self.c -= 2
        self.image.set_alpha(self.c)
        if self.c <= 0:
            self.kill()

#Gray smoke for Bomber engine explosion.
class BomberSmoke(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)    

        self.image = puff1
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, (10,10))     
        self.image = pygame.transform.rotate(self.image, random.randrange(1,50))
        self.a = 13
        self.c = random.randrange(40,70)
        self.shoot_delay = 100
        self.last_shot = pygame.time.get_ticks()
        self.rect.centerx = x     
        self.rect.centery = y
      
    def update(self):
        
        self.pos = self.rect.center
        now = pygame.time.get_ticks()
        #The sprite grows
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.image = pygame.transform.scale(self.image, (self.a, self.a))
            self.rect.centery -= 2
        self.a+=1
        #The transparency increases until the sprite disappears and is killed.
        self.c -= 1
        self.image.set_alpha(self.c)
        if self.c <= 0:
            self.kill()

#Orange smoke for Bomber engine explosion to give the impression of fire
class BomberSmoke2(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = puff2
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, (10,10))     
        self.image = pygame.transform.rotate(self.image, random.randrange(1,50))
        self.a = 13
        self.c = random.randrange(70,95)
        self.shoot_delay = 80
        self.last_shot = pygame.time.get_ticks()
        self.rect.centerx = x     
        self.rect.centery = y
      
    def update(self):
        
        self.pos = self.rect.center
        now = pygame.time.get_ticks()
        #The sprite grows
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.image = pygame.transform.scale(self.image, (self.a, self.a))
            self.rect.centery -= 2
        self.a+=1
        #The transparency increases until the sprite disappears and is killed.
        self.c -= 5
        self.image.set_alpha(self.c)
        if self.c <= 0:
            self.kill()
            

#Sprite groups
background = pygame.sprite.Group()
stars = pygame.sprite.Group()
turrets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tielaser = pygame.sprite.Group()
block = pygame.sprite.Group()
bullets = pygame.sprite.Group()
lasers = pygame.sprite.Group()
bomber = pygame.sprite.Group()
smokes = pygame.sprite.Group()
missiles = pygame.sprite.Group()
ions = pygame.sprite.Group()
playermissiles = pygame.sprite.Group()

d = Level1_Background1()
all_sprites.add(d)
e = Level1_Background2()
all_sprites.add(e)

player = Player()
all_sprites.add(player)


#Functions that create instances of enemies
def Level1():
    for i in range(30):
        c = Block(random.randrange (30, 530), random.randrange(-5000, -50))
        all_sprites.add(c)
        block.add(c)
    for i in range(16):
        b = Bomber(random.randrange(250, 350), random.randrange(-7000, -20))
        all_sprites.add(b)
        bomber.add(b)  
        
def Level2():
    for i in range(20):
        c = Block(random.randrange(30, 530), random.randrange(-7000, -50))
        all_sprites.add(c)
        block.add(c)
    for i in range(13):
        b = Bomber(random.randrange(250, 350), random.randrange(-7000, -20))
        all_sprites.add(b)
        bomber.add(b)    
    
    for i in range(20):
        c = Block(random.randrange(30, 530), random.randrange(-7000, -50))
        all_sprites.add(c)
        block.add(c)
    for i in range(16):
        b = Bomber(random.randrange(250, 350), random.randrange(-7000, -20))
        all_sprites.add(b)
        bomber.add(b)
        
def Level3():
    for i in range(4):
        b = Turret(10, -800 -(900 * i))
        all_sprites.add(b)
        turrets.add(b)   
    for i in range(4):
        b = Turret(470, -400 - (900 * i))
        all_sprites.add(b)
        turrets.add(b)    
    for i in range(20):
        c = Block(random.randrange(30, 530), random.randrange(-7000, -50))
        all_sprites.add(c)
        block.add(c)
    for i in range(13):
        b = Bomber(random.randrange(250, 350), random.randrange(-7000, -20))
        all_sprites.add(b)
        bomber.add(b)
        

#Welcome menu
def menu():
    menu = True
    while menu:
        pygame.display.flip()   
        clock.tick(FPS)
        draw_text(screen, "Press Enter to play", 45, WIDTH/2, HEIGHT/2 - 60)
        draw_text(screen, "Arrow keys to move", 20, WIDTH/2, HEIGHT/2 + 60)
        draw_text(screen, "Spacebar to fire lasers", 20, WIDTH/2, HEIGHT/2 + 90)
        draw_text(screen, "V key to fire rockets", 20, WIDTH/2, HEIGHT/2 + 120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                gameLoop()
                return
                
#Game loop    
def gameLoop():
    running = True
    Level1()
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False      
        if player.health <= 0 and player.shield <= 0:
            running = False   
        all_sprites.update()
        all_sprites.draw(screen)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_health_bar(screen, 5, 20, player.health) 
        draw_missile_bar(screen, 495, 5, player.missile) 
        pygame.display.flip()
    
    pygame.quit()

menu()