import pygame
import numpy
import random
import math
import sys
import asyncio

pygame.init()
pygame.mixer.init()

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
NEON_ORANGE = (255, 157, 0)
DARK_NEON_ORANGE = (123, 46, 0)

TOY_SHEET = pygame.image.load('assets/sprite/Pixel_guy.png')
TOY_SHEET_SMALL = pygame.image.load('assets/sprite/Pixel_guy_small.png')
TRASH_BIN_LID = pygame.image.load('assets/sprite/Trash_Bin_lid.png')
TRASH_BIN_BODY = pygame.image.load('assets/sprite/Trash_Bin_body.png')
CRATE_FRONT = pygame.image.load('assets/sprite/Wood_panel_front.png')
CRATE_BACK = pygame.image.load('assets/sprite/Wood_panel_back.png')
CRATE_SIDE = pygame.image.load('assets/sprite/Wood_panel_side.png')
CRATE_SIDE_BACK = pygame.image.load('assets/sprite/Wood_panel_side_back.png')

Score_font = pygame.font.Font('assets/fonts/impact.ttf', 40)
Back_font = pygame.font.Font('assets/fonts/impact.ttf', 50)
Title_font = pygame.font.Font('assets/fonts/impact.ttf', 200)
Start_font = pygame.font.Font('assets/fonts/impact.ttf', 100)
Final_score_font = pygame.font.Font('assets/fonts/impact.ttf', 75)

VOLUME_CONTROLL = 0.2

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
        self.toy_rect = pygame.Rect((self.posx, self.posy, self.width + 15, self.height))
        self.toy_rect_fall = pygame.Rect((self.posx, self.posy, self.width + 10, self.height))

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
        self.toy_rect = pygame.Rect((self.posx, self.posy, self.width + 15, self.height))
        self.toy_rect_fall = pygame.Rect((self.posx, self.posy, self.width, self.height))
        if self.falling:
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            rotated_rect = rotated_image.get_rect(center=self.toy_rect_fall.center)
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
    def __init__(self, screen, posy = 100, posx = 200, radius = 70, width = 5, angle = 0, fps = FPS):
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

        self.angle_initial_small = -90
        self.angle_small = 0
        self.angle_radians_small = math.radians(self.angle_small)
        self.time_counter_small = 0

        self.speed_spawn_list = [1.5, 1.25, 1, 0.75, 0.5]
        self.speed_spawn_list_counter = 0
        self.speed_spawn = self.speed_spawn_list[self.speed_spawn_list_counter]

        self.finish = False

    def clock_update(self):
        self.time_counter += 1
        if self.time_counter > self.fps * 30:
            self.time_counter = 0
            self.speed_spawn_list_counter += 1
            if self.speed_spawn_list_counter > 4:
                self.speed_spawn_list_counter = 4
                self.finish = True
            self.speed_spawn = self.speed_spawn_list[self.speed_spawn_list_counter]
            self.angle = 0

        print(self.angle)

        self.angle += 360 / (self.fps * 30)
        self.angle_radians = math.radians(self.angle_initial + self.angle)

        self.angle_small += 360 / (self.fps * 30 * 5)
        self.angle_radians_small = math.radians(self.angle_initial + self.angle_small)

    def display(self):
        pygame.draw.circle(self.screen, YELLOW_STAIN, (self.posx, self.posy), self.radius)
        pygame.draw.circle(self.screen, BLACK, (self.posx, self.posy), self.radius, width=self.width)

        hand_x = self.posx + math.cos(self.angle_radians) * (self.radius - 10)
        hand_y = self.posy + math.sin(self.angle_radians) * (self.radius - 10)

        hand_x_small = self.posx + math.cos(self.angle_radians_small) * (self.radius - 30)
        hand_y_small = self.posy + math.sin(self.angle_radians_small) * (self.radius - 30)

        pygame.draw.line(self.screen, BLACK, (self.posx, self.posy), (hand_x, hand_y), 3)

        pygame.draw.line(self.screen, BLACK, (self.posx, self.posy), (hand_x_small, hand_y_small), 5)

        pygame.draw.circle(self.screen, BLACK, (self.posx, self.posy), 5)

class Score:
    def __init__(self, screen, posy = 50, posx = 400, width = 400, height = 100):
        self.screen = screen
        self.posx = posx
        self.posy = posy
        self.score_keeper = 0
        self.width = width
        self.height = height

        self.score_board_rect = pygame.Rect(WIDTH//2 - self.width//2, posy, self.width, self.height)
        self.score_board_rect_inner = pygame.Rect(WIDTH//2 - self.width//2 + 20, posy + 20, self.width - 40, self.height - 40)

    def display(self):

        score_text = f" ${self.score_keeper:013}"
        score_surface = Score_font.render(score_text, True, DARK_NEON_ORANGE)
        score_rect = score_surface.get_rect(center=(WIDTH // 2, self.posy + self.height//2))

        pygame.draw.rect(self.screen, GREY, self.score_board_rect)
        pygame.draw.rect(self.screen, NEON_ORANGE, self.score_board_rect_inner)

        self.screen.blit(score_surface, score_rect)
        pygame.draw.rect(self.screen, BLACK, self.score_board_rect, width=5)

async def Final_score(score = 0):
    
    running = True
    toy_list = []

    Colour_Start = [90, 90, 90]
    Colour_Start_2 = [90, 90, 90]

    score_text = f"Final score: {score}"
    score_text_surface = Final_score_font.render(score_text, True, BLACK)
    score_rect = score_text_surface.get_rect(center=(WIDTH // 2, HEIGHT//2))

    exit_text = "Back to Main Menu"
    Exit_surface = Back_font.render(exit_text, True, BLACK)
    Exit_rect = Exit_surface.get_rect(center=(WIDTH - 200, HEIGHT-50))

    Play_again_text = "Play Again"
    Play_again_text_surface = Back_font.render(Play_again_text, True, Colour_Start_2)
    Play_again_rect = Play_again_text_surface.get_rect(center=(120, HEIGHT-50))

    image_toy = get_sprite(TOY_SHEET, 0, 0, 188, 50)
    final_image_rect = (WIDTH//2 - 94, HEIGHT//2 - 100, 188, 50)

    pygame.mixer.music.stop()

    while running:

        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        if Exit_rect.collidepoint(mouse_pos):
            Colour_Start = [0, 0, 0]
        else:
            Colour_Start = [90, 90, 90]

        if Play_again_rect.collidepoint(mouse_pos):
            Colour_Start_2 = [0, 0, 0]
        else:
            Colour_Start_2 = [90, 90, 90]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if Exit_rect.collidepoint(mouse_pos):
                    return False
                if Play_again_rect.collidepoint(mouse_pos):
                    return True

        screen.blit(score_text_surface, score_rect)

        Exit_surface = Back_font.render(exit_text, True, Colour_Start)
        screen.blit(Exit_surface, Exit_rect)

        Play_again_text_surface = Back_font.render(Play_again_text, True, Colour_Start_2)
        screen.blit(Play_again_text_surface, Play_again_rect)

        screen.blit(image_toy, final_image_rect)

        clock.tick(FPS)
        pygame.display.update()
        await asyncio.sleep(0)

async def Gameplay():

    running = True

    spac_conv_srt = 300
    spac_conv = 175

    conveyor_list = [Conveyor(screen, spac_conv_srt, colour=0) ,Conveyor(screen, spac_conv_srt + spac_conv, colour=1) ,Conveyor(screen, spac_conv_srt + spac_conv*2, colour=2), Conveyor(screen, spac_conv_srt + spac_conv*3, colour=3)]
    toy_list = []
    trash_bin = Trash_bin(screen)
    floor_wall = Floor_wall(screen)
    clock_wall = Clock(screen)
    score_counter = Score(screen)

    time_to_spawn = FPS * clock_wall.speed_spawn
    time_spawn = 0
    grab = False

    play_again = 0

    pygame.mixer.music.stop()
    pygame.mixer.music.load('assets/musik/main_game.ogg')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(VOLUME_CONTROLL)

    while running:

        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()

        clock_wall.clock_update()

        time_to_spawn = FPS * clock_wall.speed_spawn

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
                pygame.quit()
                sys.exit()
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
                    score_counter.score_keeper += 100
                toy_list.remove(toy)

        for toy in toy_list:
            for conveyor in conveyor_list:
                if toy.toy_rect.colliderect(conveyor.fall_wall_rect) and toy.grabbed == False:
                    toy.falling = True
                    if toy.colour == conveyor.colour and toy.score == True and toy.broken == 0:
                        score_counter.score_keeper += 50
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

        score_counter.display()

        for toy in toy_list:
            if toy.grabbed:
                toy.display()

        if clock_wall.finish == True:
            play_again = await Final_score(score_counter.score_keeper)
            return play_again



        clock.tick(FPS)
        pygame.display.update()
        await asyncio.sleep(0)

async def main():
    
    global VOLUME_CONTROLL

    running = True
    toy_list = []

    time_to_spawn = FPS/14
    time_countdown = 0
    
    Colour_Start = [255, 255, 255]
    Colour_title = [0, 0 ,0]
    Colour_Music = [90, 90, 90]
    
    musiconoff = True

    Title_text = "Toy Factory"
    Title_surface = Title_font.render(Title_text, True, Colour_title)
    Title_rect = Title_surface.get_rect(center=(WIDTH // 2, 200))

    Title_START = "START"
    Title_surface_START = Start_font.render(Title_START, True, Colour_Start)
    Title_rect_START = Title_surface_START.get_rect(center=(WIDTH // 2, 500))

    Music_text = "Music: "
    Music_surface = Back_font.render(Music_text, True, Colour_Music)
    Music_rect = Music_surface.get_rect(center=(WIDTH - 175, HEIGHT-50))

    play_again = False

    pygame.mixer.music.stop()

    while running:

        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        
        time_countdown += 1

        global VOLUME_CONTROLL
        if musiconoff == True:
            Music_text_type = "On"
            VOLUME_CONTROLL = 0.2
        else:
            Music_text_type = "Off"
            VOLUME_CONTROLL = 0
        
        Music_text_type_surface = Back_font.render(Music_text_type, True, Colour_Music)
        Music_text_type_rect = Music_text_type_surface.get_rect(center=(WIDTH - 75, HEIGHT-50))
        Music_surface = Back_font.render(Music_text, True, Colour_Music)
        Music_rect = Music_surface.get_rect(center=(WIDTH - 175, HEIGHT-50))

        if time_countdown > time_to_spawn:
            time_countdown = 0
            toy_list.append(Toy(screen, random.randint(0, WIDTH), -200, random.randint(0, 3), 0, 0))

        if Title_rect_START.collidepoint(mouse_pos):
            Colour_Start = [0, 0, 0]
        else:
            Colour_Start = [90, 90, 90]

        if Music_text_type_rect.collidepoint(mouse_pos) or Music_rect.collidepoint(mouse_pos):
            Colour_Music = [0, 0, 0]
        else:
            Colour_Music = [90, 90, 90]

        if Title_rect.collidepoint(mouse_pos):
            if Colour_title[0] < 255 and Colour_title[1] == 0 and Colour_title[2] == 0:
                Colour_title[0] += 1
            if Colour_title[0] == 255 and Colour_title[1] < 255 and Colour_title[2] == 0:
                Colour_title[1] += 1
            if Colour_title[0] > 0 and Colour_title[1] == 255 and Colour_title[2] == 0:
                Colour_title[0] -= 1
            if Colour_title[0] == 0 and Colour_title[1] == 255 and Colour_title[2] < 255:
                Colour_title[2] += 1
            if Colour_title[0] == 0 and Colour_title[1] > 0 and Colour_title[2] == 255:
                Colour_title[1] -= 1
            if Colour_title[0] == 0 and Colour_title[1] == 0 and Colour_title[2] > 0:
                Colour_title[2] -= 1

        else:
            Colour_title = [0, 0, 0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if Title_rect_START.collidepoint(mouse_pos):
                    play_again = await Gameplay()
                    while play_again == True:
                        play_again = await Gameplay()
                if Music_text_type_rect.collidepoint(mouse_pos) or Music_rect.collidepoint(mouse_pos):
                    if musiconoff == True:
                        musiconoff = False
                    else:
                        musiconoff = True
        
        for toyr in toy_list[:]:
            if toyr.posy > HEIGHT + 50:
                toy_list.remove(toyr)

        for toy in toy_list:
            toy.falling = True
            toy.move(mouse_pos)
            toy.display()
            
        Title_surface = Title_font.render(Title_text, True, Colour_title)
        Title_rect = Title_surface.get_rect(center=(WIDTH // 2, 200))

        Title_surface_START = Start_font.render(Title_START, True, Colour_Start)
        Title_rect_START = Title_surface_START.get_rect(center=(WIDTH // 2, 500))

        screen.blit(Title_surface, Title_rect)
        screen.blit(Title_surface_START, Title_rect_START)   
        screen.blit(Music_surface, Music_rect)
        screen.blit(Music_text_type_surface, Music_text_type_rect)

        clock.tick(FPS)
        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())
pygame.quit()
