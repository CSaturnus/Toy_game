import pygame
import numpy
import random
import math

pygame.init()

HEIGHT, WIDTH = 1000, 1300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Toy Maker")

clock = pygame.time.Clock() 
FPS = 120

WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (34, 139, 34)
GREY = (142, 142, 142)
FLOOR_COLOUR = (108,130,128)
LIST_COLOUR = (225,233,183)
Wall_COLOUR = (128,0,0)
YELLOW_STAIN = 	(248,248,186)

TOY_SHEET = pygame.image.load('assets/sprite/Pixel_guy.png')
TOY_SHEET_SMALL = pygame.image.load('assets/sprite/Pixel_guy_small.png')
TRASH_BIN_LID = pygame.image.load('assets/sprite/Trash_Bin_lid.png')
TRASH_BIN_BODY = pygame.image.load('assets/sprite/Trash_Bin_body.png')
CRATE_FRONT = pygame.image.load('assets/sprite/Wood_panel_front.png')
CRATE_BACK = pygame.image.load('assets/sprite/Wood_panel_back.png')
CRATE_SIDE = pygame.image.load('assets/sprite/Wood_panel_side.png')
CRATE_SIDE_BACK = pygame.image.load('assets/sprite/Wood_panel_side_back.png')

def get_sprite(sheet, x, y, width, height):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    return sprite

class Floor_wall:
    def __init__(self, screen, posx = 0, posy = 310):
        self.screen = screen
        self.posx = posx
        self.posy = posy

        self.floor_rect = pygame.Rect((self.posx, self.posy, WIDTH, HEIGHT))
        self.list_rect = pygame.Rect((self.posx, self.posy - 20, WIDTH, 20))
        self.wall_rect = pygame.Rect((0, 0, WIDTH, 290))
    
    def display(self):
        pygame.draw.rect(self.screen, FLOOR_COLOUR, self.floor_rect)
        pygame.draw.rect(self.screen, LIST_COLOUR, self.list_rect)
        pygame.draw.rect(self.screen, Wall_COLOUR, self.wall_rect)



class Toy:
    def __init__(self, screen, posx, posy, colour, broken, speed = -1):
        self.screen = screen
        self.posx = posx
        self.posy = posy
        self.colour = colour
        self.speed = speed
        self.angle = 0
        self.angle_fall_speed = 0
        self.broken = broken # False = 0, True = 1
        self.grabbed = False
        self.falling = False
        self.acceleration_fall = 0.02
        self.garbage = False
        self.score = True

        self.image = get_sprite(TOY_SHEET, 47 * colour, 50 * broken, 47, 50)
        self.width, self.height = self.image.get_size()
        self.toy_rect = pygame.Rect((self.posx, self.posy, self.width, self.height))

    def move(self, mouse_pos):
        if self.grabbed:
            self.posx = mouse_pos[0] - self.width//2
            self.posy = mouse_pos[1] - self.height//2
        else:    
            self.posx += self.speed
        if self.falling:
            self.angle_fall_speed += self.acceleration_fall
            if self.angle_fall_speed > 2:
                self.angle_fall_speed = 2
            self.angle += self.angle_fall_speed
            self.posy += self.angle_fall_speed

    def display(self):
        self.toy_rect = pygame.Rect((self.posx, self.posy, self.width, self.height))
        if self.falling:
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            rotated_rect = rotated_image.get_rect(center=self.toy_rect.center)
            self.screen.blit(rotated_image, rotated_rect.topleft)
        else:
            self.screen.blit(self.image, self.toy_rect)
        
class Conveyor:
    def __init__(self, screen, posy, colour, posx = 0, width = 960, height = 100):
        self.screen = screen
        self.posx = posx 
        self.posy = posy
        self.width = width
        self.height = height
        self.colour = colour

        self.conveyor_rect = pygame.Rect((WIDTH-self.width , self.posy + 30, self.width, self.height - 20))
        self.conveyor_rect_under_back = pygame.Rect((WIDTH-self.width - 70, self.posy + 30, self.width, 80))
        self.conveyor_rect_under = pygame.Rect((WIDTH-self.width , self.posy + 30 + self.height - 20, self.width, 80))

        self.fall_wall_rect = pygame.Rect((WIDTH-self.width - 70, self.posy, 30, self.height))
        
        self.fall_remover = pygame.Rect((0, self.posy + 150, 270, self.height - 80))

        self.crate_front = pygame.Rect((30, self.posy + 103, 320, 40))
        self.crate_back = pygame.Rect((0, self.posy + 73, 320, 40))
        self.crate_side = pygame.Rect((0,self.posy + 73, 30, 100))
        self.crate_side_back = pygame.Rect((289, self.posy + 73, 30, 100))

        self.toy_image = get_sprite(TOY_SHEET, 47 * colour, 50 * 0, 47, 50)
        self.toy_width_small, self.toy_width_height = self.toy_image.get_size()
        self.toy_small_rect = pygame.Rect((150, self.posy + 115, self.toy_width_small, self.toy_width_height))

    def display(self):

#        pygame.draw.rect(self.screen, GREEN, self.fall_wall_rect)
#        pygame.draw.rect(self.screen, GREEN, self.fall_remover)

        pygame.draw.rect(self.screen, GREY, self.conveyor_rect_under_back)
        pygame.draw.rect(self.screen, BLACK, self.conveyor_rect)
        pygame.draw.polygon(self.screen, BLACK, ((WIDTH-self.width - 70, self.posy + 30), (WIDTH-self.width , self.posy + 30), (WIDTH-self.width , self.posy + self.height + 8)))

        pygame.draw.polygon(self.screen, BLACK, ((WIDTH-self.width - 70, self.posy + 30), (WIDTH-self.width - 70, self.posy + 40),  (WIDTH-self.width , self.posy + self.height + 18),(WIDTH-self.width , self.posy + self.height + 8)))

        pygame.draw.rect(self.screen, GREY, self.conveyor_rect_under)

        self.screen.blit(CRATE_BACK, self.crate_back)

    def display_crate(self):
        self.screen.blit(CRATE_FRONT, self.crate_front)
        self.screen.blit(CRATE_SIDE, self.crate_side)
        self.screen.blit(self.toy_image, self.toy_small_rect)

    def display_crate_back(self):
        self.screen.blit(CRATE_SIDE_BACK, self.crate_side_back)

class Trash_bin:
    def __init__(self, screen, posy = 100, posx = WIDTH - 300, width = 200, height = 100):
        self.screen = screen
        self.posx = posx
        self.posy = posy 
        self.width = width
        self.height = height

        self.trash_bin_lid_rect = pygame.Rect((self.posx, self.posy, self.width, self.height))
        self.delete_rect = pygame.Rect((self.posx, self.posy + 160, self.width, self.height - 50))

        self.trash_bin_body_rect = pygame.Rect((self.posx - 5, self.posy + 100, self.width, self.height))

    def display_lid(self):

        pygame.draw.rect(self.screen, BLACK, self.delete_rect)
        pygame.draw.rect(self.screen, GREEN, self.trash_bin_lid_rect)
        self.screen.blit(TRASH_BIN_LID, self.trash_bin_lid_rect)
    
    def display_body(self):
        
        self.screen.blit(TRASH_BIN_BODY, self.trash_bin_body_rect)

class Clock:
    def __init__(self, screen, posy = 100, posx = 200, radius = 70, width = 5, angle = -90, fps = FPS):
        self.screen = screen
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.width = width
        self.fps = fps

        self.angle_initial = -90
        self.angle = 0
        self.angle_radians = math.radians(angle)
        self.time_counter = 0

        self.speed_spawn = [2, 1.75, 1.5, 1.25, 1]

    def clock_update(self):
        self.time_counter += 1
        if self.time_counter > self.fps * 60:  # Reset every minute
            self.time_counter = 0
            self.angle = 0

        print(self.angle)

        self.angle += 360 / (self.fps * 60)  # Increment angle smoothly
        self.angle_radians = math.radians(self.angle_initial + self.angle)

    def display(self):
        pygame.draw.circle(self.screen, YELLOW_STAIN, (self.posx, self.posy), self.radius)
        pygame.draw.circle(self.screen, BLACK, (self.posx, self.posy), self.radius, width=self.width)  # Black border

        # Calculate hand position
        hand_x = self.posx + math.cos(self.angle_radians) * (self.radius - 10)
        hand_y = self.posy + math.sin(self.angle_radians) * (self.radius - 10)

        pygame.draw.line(self.screen, BLACK, (self.posx, self.posy), (hand_x, hand_y), 5)  # Clock hand

        pygame.draw.circle(self.screen, BLACK, (self.posx, self.posy), 5)

def main():

    running = True

    spac_conv_srt = 300
    spac_conv = 175

    conveyor_list = [Conveyor(screen, spac_conv_srt, colour=0) ,Conveyor(screen, spac_conv_srt + spac_conv, colour=1) ,Conveyor(screen, spac_conv_srt + spac_conv*2, colour=2), Conveyor(screen, spac_conv_srt + spac_conv*3, colour=3)]
    toy_list = []
    trash_bin = Trash_bin(screen)
    floor_wall = Floor_wall(screen)
    clock_wall = Clock(screen)


    time_to_spawn = FPS * clock_wall.speed_spawn[0]
    time_spawn = 0
    grab = False

    score = 0

    while running:

        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()

        clock_wall.clock_update()

        time_spawn += 1
        if time_spawn >= time_to_spawn:
            if random.randint(1, 20) == 1:
                toy_list.append(Toy(screen, WIDTH, random.randint(0, 3)*spac_conv + spac_conv_srt + random.randint(0, 52), random.randint(0, 3), 1))
            else:
                toy_list.append(Toy(screen, WIDTH, random.randint(0, 3)*spac_conv + spac_conv_srt + random.randint(0, 52), random.randint(0, 3), 0))
            time_spawn = 0
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                debouncer = False
                for i, toy in enumerate(toy_list):
                    if toy.toy_rect.collidepoint(mouse_pos) and grab == False and debouncer == False and toy.falling == False:
                        grab = True
                        toy.grabbed = True
                        debouncer = True
                        toy_list.insert(0, toy_list.pop(i))
                    for conveyor in conveyor_list:
                        if conveyor.conveyor_rect.collidepoint(mouse_pos) and grab == True and debouncer == False and toy.grabbed == True:
                            toy.grabbed = False
                            grab = False
                            debouncer = True
                            if int(mouse_pos[1] - toy.height//2) < int(conveyor.posy):
                                toy.posy += toy.height//2
                            elif int(mouse_pos[1] + toy.height//2) > int(conveyor.posy + conveyor.height):
                                toy.posy -= toy.height//2
                    if trash_bin.trash_bin_lid_rect.collidepoint(mouse_pos) and grab == True and debouncer == False and toy.grabbed == True:
                        toy.grabbed = False
                        toy.falling = True
                        toy.speed = 0
                        grab = False
                        toy.garbage = True
                        if int(mouse_pos[0] - toy.width//2) < int(trash_bin.posx):
                            toy.posx += toy.width//2 + 4
                        elif int(mouse_pos[0] + toy.width//2) > int(trash_bin.posx + trash_bin.width):
                            toy.posx -= toy.width//2 + 4
                        
        floor_wall.display()

        trash_bin.display_lid()

        trash_bin.display_body()

        for conveyor in conveyor_list:
            conveyor.display()
            conveyor.display_crate_back()
        
        for toy in toy_list:
            for conveyor in conveyor_list:
                if toy.toy_rect.colliderect(conveyor.fall_remover) and toy.falling == True:
                    toy_list.remove(toy)
                    break
            if toy.toy_rect.colliderect(trash_bin.delete_rect) and toy.falling == True:
                if toy.broken == 1:
                    score += 10
                toy_list.remove(toy)

        for toy in toy_list:
            for conveyor in conveyor_list:
                if toy.toy_rect.colliderect(conveyor.fall_wall_rect) and toy.grabbed == False:
                    toy.falling = True
                    if toy.colour == conveyor.colour and toy.score == True and toy.broken == 0:
                        score += 10
                        toy.score = False

            toy.move(mouse_pos)
            toy.display()
            if toy.falling == True and toy.garbage == True:
                trash_bin.display_body()

        for crate in conveyor_list:
            crate.display_crate()

        if grab == False:
            trash_bin.display_body()

        clock_wall.display()

        clock.tick(FPS)
        pygame.display.update()

main()
pygame.quit()
