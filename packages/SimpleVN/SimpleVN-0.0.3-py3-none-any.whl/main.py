import pygame, math, random, sys, re
from pygame.locals import *
from settings import *
from classes import *

# General Settings
WIDTH, HEIGHT = 1080,720
TITLE = "Dating Sim"
FPS = 60
PLAYER_NAME = "DEFAULT"

TEXT_SCROLL_SPEED = 0.005 # in seconds
FADE_SPEED = 0.0001

# Credits
CREDITS = [
    "C R E D I T S",
    "",
    "Lead Programmer - Derek Zhang",
    "Code Assistant - Yi Deng",
    "Script - Stephen Hwang & Khushwant Virdi",
    "Original Art - Juleen Chen",
    "Music - Stephen Hwang",
    "Project Director - Stephen Hwang"
]

path = "../resources/images/"
OPENING = pygame.image.load("{}python.png".format(path))
SPLASH = pygame.image.load("{}splash.png".format(path))
OPENING_BG = pygame.image.load("{}opening.png".format(path))

EXPRESSIONS = []
BACKGROUNDS = []

# Font Definitions
comicsans50 = pygame.font.SysFont("comicsansms", 50)


# Music
MUSIC = [
"../resources/music/intro.mp3",
"../resources/music/bg_music.mp3",
"../resources/music/51_ending.mp3"
]

# Colour Definitions
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN= (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
AQUA = (0,255,255)
GREY = (200,200,200)

# Fancy Functions
def find_space_backwards(string, index):
    for i in range(index,0,-1):
        if string[i] == ' ':
            return i

def check_break():
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
            return True
    return False

def set_player_name(name):
    global PLAYER_NAME
    PLAYER_NAME = name
class Player:
    def __init__(self,name):
        self.name = name
        self.score

class Dialogue:
    def __init__(self, text, responses, image):
        self.t = text
        self.responses = responses
        self.image = image

    def play_text(self,window,bg,overlay,x,y,playerName):
        text_font = pygame.font.SysFont("arial", 25)
        message = text_font.render(self.t, True, WHITE)
        self.t = self.t.replace("PLAYERNAME",playerName)
        if message.get_width() > WIDTH-410:
            #split the message into sections
            index = int(len(self.t)*(WIDTH-410)/(message.get_width()))
            t1 = self.t[:find_space_backwards(self.t,index)]

            if(message.get_width()/(WIDTH-410))>2:
                index2 = int((len(self.t)-index)*(WIDTH-410)/(message.get_width()))
                t2 = self.t[find_space_backwards(self.t,index):find_space_backwards(self.t,index2)].strip()
                t3 = self.t[find_space_backwards(self.t,index2):].strip()
            else:
                t2 = self.t[find_space_backwards(self.t,index):].strip()

            for i in range(len(t1)):
                if check_break():
                    break
                window.blit(bg,(0,0))
                window.blit(self.image,(0,0))
                window.blit(overlay,(200,510))
                self.text(window, t1[:i],"arial", 25, WHITE, x, y)
                time.sleep(TEXT_SCROLL_SPEED)
                pygame.display.update()
            for i in range(len(t2)):
                if check_break():
                    break
                window.blit(bg,(0,0))
                window.blit(self.image,(0,0))
                window.blit(overlay,(200,510))
                self.text(window, t1,"arial",25,WHITE,x,y)
                self.text(window, t2[:i],"arial", 25, WHITE, x, y+30)
                time.sleep(TEXT_SCROLL_SPEED)
                pygame.display.update()
            if(message.get_width()/(WIDTH-400)>2):
                for i in range(len(t3)):
                    if check_break():
                        break
                    window.blit(bg,(0,0))
                    window.blit(self.image,(0,0))
                    window.blit(overlay,(200,510))
                    self.text(window, t1,"arial",25,WHITE,x,y)
                    self.text(window, t2,"arial", 25, WHITE, x, y+30)
                    self.text(window, t3[:i],"arial", 25, WHITE, x, y+60)

                    time.sleep(TEXT_SCROLL_SPEED)
                    pygame.display.update()
        else:
            for i in range(len(self.t)):
                if check_break():
                    break
                window.blit(bg,(0,0))
                window.blit(self.image,(0,0))
                window.blit(overlay,(200,510))
                self.text(window, self.t[:i],"arial", 25, WHITE, x, y)
                time.sleep(TEXT_SCROLL_SPEED)
                pygame.display.update()

    def text(self, window, text, font, size, color, x, y):
        font_style = str(font)
        font_size = size

        text_font = pygame.font.SysFont(font_style, font_size)
        message = text_font.render(text, True, color)
        
        window.blit(message, (x, y))

class Response:
    def __init__(self, text, target,scene_change = False):
        self.text = text
        self.target_id = target
        self.scene_change = scene_change

class Scene:
    def __init__(self,bg):
        self.bg = bg
        self.dialogues = []
        self.current_dialogue = None
        self.fresh = True

    def add_dialogue(self,dial):        
        self.dialogues.append(dial)
        if self.fresh:
            self.current_dialogue = self.dialogues[0]
            self.fresh = False

    def input(self, option):
        ''' option -> response 1, 2, or 3'''
        self.current_dialogue = self.dialogues[self.current_dialogue.responses[option-1].target_id-1]

class Game:
    def __init__(self):
        # initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        pygame.display.init()
        pygame.display.set_caption(TITLE)

        self.window = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()

        self.scenes = []
        self.current_scene = None
        self.next_scene = None

        self.game_state = "splash"

        self.text_anim = True
        
        # Bad Ending
        self.bad_ending = False
        self.fifty_ending = False

        # Fader Animation
        self.fader = pygame.Surface((WIDTH,HEIGHT));self.fader.fill(BLACK)
        self.fading = False
        self.fade_alpha = 0     
        self.fading_out = False

        # Name Typing Shenanigans
        self.temp_name = ""
        self.inkey = None

    def load_scripts(self,ffiles):
        self.scenes = []
        
        # Reading the file
        path = '../resources/script/'
        files = []
        for f in ffiles:
            files.append(open(f, "r"))
        
        for file in files:
            script = file.readlines()
            self.scenes.append(Scene(BACKGROUNDS[int(script[0])-1]))
            for i in range(2,len(script),6):
                dial_text = script[i][:-2]

                try:
                    r1 = Response(script[i+1][:script[i+1].index(' (')], int(script[i+1][script[i+1].index('(')+1:script[i+1].index(')')]),scene_change=(')s' in script[i+1]))
                    r2 = Response(script[i+2][:script[i+2].index(' (')], int(script[i+2][script[i+2].index('(')+1:script[i+2].index(')')]),scene_change=(')s' in script[i+2]))
                    r3 = Response(script[i+3][:script[i+3].index(' (')], int(script[i+3][script[i+3].index('(')+1:script[i+3].index(')')]),scene_change=(')s' in script[i+3]))
                except ValueError:
                    print(files.index(file))

                self.scenes[files.index(file)].add_dialogue(Dialogue(dial_text,[r1,r2,r3],EXPRESSIONS[int(script[i][-2:].strip())-1]))

        self.current_scene = self.scenes[0]
        self.next_scene = None

    def load_backgrounds(self, files):
        for f in files:
            BACKGROUNDS.append(pygame.image.load(f))    

    def load_expressions(self, files):
        for f in files:
            EXPRESSIONS.append(pygame.image.load(f)) 

    def run(self):
        pygame.mixer.music.load(MUSIC[0])
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        # Game Loop
        while 1:
            while self.game_state == "loading":
                for event in pygame.event.get():
                    # check for closing window
                    if event.type == pygame.QUIT:
                        self.close()
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                        self.fade()
                        self.fading_out = True

                self.window.blit(PYTHON_BG,(0,0))

                if self.fading:
                    if self.fading_out:
                        if self.fade_alpha + 15 < 255:
                            self.fade_alpha += 15
                        else:
                            self.game_state = "splash"
                            self.fading_out = False
                            break
                    else:
                        if self.fade_alpha - 15 > 0:
                            self.fade_alpha -= 15
                        else:
                            self.fading = False
                    self.fader.set_alpha(self.fade_alpha)
                    self.window.blit(self.fader,(0,0))

                pygame.display.update()

            while self.game_state == "splash":
                for event in pygame.event.get():
                    # check for closing window
                    if event.type == pygame.QUIT:
                        self.close()
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                        self.fade()
                        self.fading_out = True 

                self.window.blit(SPLASH,(0,0))

                if self.fading:
                    if self.fading_out:
                        if self.fade_alpha + 15 < 255:
                            self.fade_alpha += 15
                        else:
                            self.game_state = "name_select"
                            break
                    else:
                        if self.fade_alpha - 15 > 0:
                            self.fade_alpha -= 15
                        else:
                            self.fading = False
                    self.fader.set_alpha(self.fade_alpha)
                    self.window.blit(self.fader,(0,0))

                pygame.display.update()

            while self.game_state == "name_select":
                for event in pygame.event.get():
                    # check for closing window
                    if event.type == pygame.QUIT:
                        self.close()
                    if event.type == pygame.KEYDOWN:
                        self.inkey = event.key
                        if event.key == K_RETURN and not self.temp_name.strip() == "":
                            PLAYER_NAME = self.temp_name
                            self.fade()

                    if self.inkey != None:
                        if self.inkey == K_BACKSPACE:
                            self.temp_name = self.temp_name[:-1]
                        elif self.inkey == K_ESCAPE:
                            self.temp_name = ""
                        elif self.inkey <= 122 and self.inkey >= 97 and len(self.temp_name) < 20:
                            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                                self.temp_name+=(chr(self.inkey-32))
                            else:
                                self.temp_name+=(chr(self.inkey))
                        self.inkey = None

                self.window.blit(OPENING_BG,(0,0))

                self.text(self.temp_name,"Consolas",30,WHITE,0,0,align="fullcenter")
                if self.temp_name.strip() == "":
                    self.text("N A M E", "Consolas",30,(180,180,180),0,0,align="fullcenter")

                if self.fading:
                    if not self.temp_name == "":
                        if self.fade_alpha + 15 < 255:
                            self.fade_alpha += 15
                        else:
                            self.game_state = "speaking"
                            pygame.mixer.music.load(MUSIC[1])
                            pygame.mixer.music.set_volume(0.2)
                            pygame.mixer.music.play(-1)
                            break
                    else:
                        if self.fade_alpha - 15 > 0:
                            self.fade_alpha -= 15
                        else:
                            self.fading = False
                    self.fader.set_alpha(self.fade_alpha)
                    self.window.blit(self.fader,(0,0))

                pygame.display.update()

            while self.game_state == "speaking":
                for event in pygame.event.get():
                    # check for closing window
                    if event.type == pygame.QUIT:
                        self.close()
                    if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP) and not self.fading:
                        if self.current_scene.current_dialogue.responses[0].text == "END":
                            self.fade_alpha = 0
                            self.fade()
                            if self.current_scene.current_dialogue.responses[0].target_id == 100:
                                self.fifty_ending = True
                            elif self.current_scene.current_dialogue.responses[0].target_id == 200:
                                self.bad_ending = True
                        else:
                            if self.current_scene.current_dialogue.responses[0].text == "SKIP":
                                self.game_state = "speaking"
                                self.current_scene.input(1)
                                self.text_anim = True
                            else:
                                self.game_state = "replying"

                if self.game_state != "speaking":
                    break

                self.window.blit(self.current_scene.bg,(0,0))

                # Draw Character
                self.window.blit(self.current_scene.current_dialogue.image,(0,0))

                overlay = pygame.Surface((680,150));overlay.set_alpha(128);overlay.fill(BLACK)
                self.window.blit(overlay,(200,510))

                if not self.fading:
                    if self.text_anim:
                        self.current_scene.current_dialogue.play_text(self.window,self.current_scene.bg,overlay,210,520,PLAYER_NAME)
                        self.text_anim = False
                    else:
                        tt = self.current_scene.current_dialogue.t
                        text_font = pygame.font.SysFont("arial", 25)
                        message = text_font.render(tt, True, WHITE)

                        if message.get_width() > WIDTH-410:
                            #split the message into sections 
                            index = int(len(tt)*(WIDTH-410)/(message.get_width()))
                            t1 = tt[:find_space_backwards(tt,index)]
                            t2 = tt[find_space_backwards(tt,index):]
                            self.text(t1,"arial",25,WHITE,210,520)
                            self.text(t2.strip(),"arial",25,WHITE,210,550)
                        else:
                            self.text(tt,"arial",25,WHITE,210,520)

                if self.fading:
                    if self.current_scene.current_dialogue.responses[0].text == "END":
                        if self.fade_alpha + 5 < 255:
                            self.fade_alpha += 5
                        else:
                            self.fading = False
                            self.game_state = "endscreen"
                            if self.fifty_ending:
                                pygame.mixer.music.load(MUSIC[2])
                                pygame.mixer.music.play()
                            else:
                                pygame.mixer.music.load(MUSIC[0])
                                pygame.mixer.music.set_volume(0.2)
                                pygame.mixer.music.play(-1)
                            break
                    else:
                        if self.fade_alpha - 15 > 0:
                            self.fade_alpha -= 15
                        else:
                            self.fading = False
                    self.fader.set_alpha(self.fade_alpha)
                    self.window.blit(self.fader,(0,0))

                pygame.display.update()
                self.clock.tick(FPS)

            while self.game_state == "replying":
                for event in pygame.event.get():
                    # check for closing window
                    if event.type == pygame.QUIT:
                        self.close()
                    if event.type == pygame.MOUSEBUTTONUP:
                        # Check for button clicks
                        if mx >= 200 and mx <= WIDTH-200:
                            if my > 510 and my < 660:
                                if my > 510 and my < 560 and self.current_scene.current_dialogue.responses[0].text != "EMPTY":
                                    if self.current_scene.current_dialogue.responses[0].scene_change:
                                        self.next_scene = self.scenes[self.current_scene.current_dialogue.responses[0].target_id-1]
                                        self.fade()
                                    else:
                                        self.current_scene.input(1)
                                elif my > 560 and my < 610 and self.current_scene.current_dialogue.responses[1].text != "EMPTY":
                                    if self.current_scene.current_dialogue.responses[1].scene_change:
                                        self.fade()
                                        self.next_scene = self.scenes[self.current_scene.current_dialogue.responses[1].target_id-1]
                                    else:
                                        self.current_scene.input(2)
                                elif my > 610 and my < 660 and self.current_scene.current_dialogue.responses[2].text != "EMPTY":
                                    if self.current_scene.current_dialogue.responses[2].scene_change:
                                        self.fade()
                                        self.next_scene = self.scenes[self.current_scene.current_dialogue.responses[2].target_id-1]
                                    else:
                                        self.current_scene.input(3)
                                else:
                                    break
                                self.text_anim = True
                                if not self.fading:
                                    self.game_state = "speaking"

                if self.game_state != "replying":
                    break

                # Clear screen
                self.window.blit(self.current_scene.bg,(0,0))

                # Draw Character
                self.window.blit(self.current_scene.current_dialogue.image,(0,0))

                # Grab mouse position
                mx,my = pygame.mouse.get_pos()

                # Declaring the faded overlay and selector
                overlay = pygame.Surface((680,150));overlay.set_alpha(128);overlay.fill(BLACK)
                selector = pygame.Surface((680,50));selector.set_alpha(128);selector.fill(BLACK)

                # Overlay Render
                self.window.blit(overlay,(200,510))

                # Selector Render
                if mx >= 200 and mx <= WIDTH-200:
                    if my > 510 and my < 560 and self.current_scene.current_dialogue.responses[0].text != "EMPTY":
                        self.window.blit(selector,(200,510))
                    elif my > 560 and my < 610 and self.current_scene.current_dialogue.responses[1].text != "EMPTY":
                        self.window.blit(selector,(200,560))
                    elif my > 610 and my < 660 and self.current_scene.current_dialogue.responses[2].text != "EMPTY":
                        self.window.blit(selector,(200,610))

                # Actual Replies
                for i in range(3): 
                    t = self.current_scene.current_dialogue.responses[i].text.replace("PLAYERNAME",PLAYER_NAME)
                    if t == "[next scene]":
                        self.text(t, "arial", 25, WHITE, -99, 518+50*i,align="center")
                    elif not t == "EMPTY":
                        self.text(t, "arial", 25, WHITE, 210, 518+50*i)

                if self.fading:
                    if self.fade_alpha + 15 < 255:
                        self.fade_alpha += 15
                    else:
                        self.game_state = "speaking"
                        self.current_scene = self.next_scene
                        break
                    self.fader.set_alpha(self.fade_alpha)
                    self.window.blit(self.fader,(0,0))

                pygame.display.update()
                self.clock.tick(FPS)

            while self.game_state == "endscreen":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.close()
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                        self.fade()

                if self.fifty_ending:
                    self.window.blit(BACKGROUNDS[-1],(0,0))
                else:
                    self.window.fill(BLACK)
                    if(self.bad_ending):
                        self.text("E N D ?", "Arial", 30, WHITE, 0,0,align="fullcenter")
                    else:
                        self.text("F I N", "Arial", 30, WHITE, 0,0,align="fullcenter")

                if self.fading:
                    if self.fade_alpha + 15 < 255:
                        self.fade_alpha += 15
                    else:
                        self.game_state = "credits"
                        if self.fifty_ending:
                            pygame.mixer.music.load(MUSIC[0])
                            pygame.mixer.music.play(-1)
                        self.fading = False
                        self.fade_alpha = 0
                        break
                    self.fader.set_alpha(self.fade_alpha)
                    self.window.blit(self.fader,(0,0))
                pygame.display.update()

            while self.game_state == "credits":
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.close()
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                        self.fade()

                self.window.fill(BLACK)
                for line in CREDITS:
                    self.text(line, "Arial", 30, WHITE, 0,200+40*CREDITS.index(line),align="center")

                if self.fading:
                    if self.fade_alpha + 15 < 255:
                        self.fade_alpha += 15
                    else:
                        self.game_state = "splash"
                        self.load_game()
                        self.temp_name = ""
                        self.fading_out = False
                        break
                pygame.display.update()

    def text(self,text, font, size, color, x, y, align="free"):
        font_style = str(font)
        font_size = size

        text_font = pygame.font.SysFont(font_style, font_size)

        message = text_font.render(text, True, color)
        if(align == "center"):
            self.window.blit(message, (WIDTH/2-message.get_width()//2, y))
        elif(align == "fullcenter"):
            self.window.blit(message, (WIDTH/2-message.get_width()//2, HEIGHT/2-message.get_height()//2))
        else:
            self.window.blit(message, (x, y))

    def fade(self):
        self.fading = True

    def close(self):
        pygame.quit()
        sys.exit()

