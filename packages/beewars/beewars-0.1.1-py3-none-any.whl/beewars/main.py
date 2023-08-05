import pygame
from pygame.locals import *
import numpy as np

def run():
    pass

board = np.zeros((297))
board[:] = -1
boardp = np.zeros((297))
boardp[:] = -1

TENT = 1 #Cost: 4, Adds 2 (/\)
HUT = 2 #Cost: 10, Adds 5 
CASTLE = 3 #Cost: 40, Adds 10
KNIFE = 10 #Cost: 4, Subtracts 2
SNIPER = 11 #Cost 10, Subtracts 5
RPG = 12 #Cost 100, Subtracts 50
GRENADE = 13 #Cost 40, Subtracts 10
RAD = 40

FILENAMES = {1:"tent.png", 2:"hut.png", 3:"castle.png",
        10:"knife.png", 11:"sniper.png", 12:"rpg.png", 13:"grenade.png"}



disp = pygame.display.set_mode((840 + 200, 480))
disp.fill((255,255,255))


HEX = pygame.image.load("sym/hex.png")
HEX = pygame.transform.scale(HEX, (40, 40))

PLAYERS = []
COLORS = [(0,0,0), (255,0,0), (0,255,0), (0,0,255)]

CLICKS = 297 * [[[0,0], [0,0]]]

i = 0
for key in FILENAMES:
    try:
        im = pygame.image.load("sym/hex.png")
        img = pygame.image.load("sym/"+FILENAMES[key])
        im = pygame.transform.scale(im, (40,40))
        disp.blit(im, (850, i*40+20))
        disp.blit(img, (850, i*40+20))
        i+=1
    except:
        pass

def draw():
    row = 0
    col = 0
    global board, disp
    for i in range(len(board)):
        if (row==14 and col%2==0) or (row==13 and col%2==1):
            row = 0
            col += 1
        val = 20 if col%2==0 else 50
        lav = 0 if val==50 else 20
        disp.blit(HEX, (row*60+val, col*20+20))
        CLICKS[i] = [[row*60+val, col*20+20], [row*60+val+40, col*20+20+40]] 
        if board[i]>=0:
            filename = "sym/"+FILENAMES[board[i]]
            im = pygame.image.load(filename)
            nm = pygame.surface.Surface((40,40))
            nm.set_colorkey((100,100,102))
            for x in range(im.get_width()):
                for y in range(im.get_height()):
                    r,g,b,a = im.get_at((x,y))
                    if a>127:
                        nm.set_at((x,y), COLORS[int(boardp[i])])
                    else:
                        nm.set_at((x,y), (100,100,102))
            disp.blit(nm, (row*60+val, col*20+20))
        row += 1
    pygame.display.update()

def draw_scores():
    global board, disp
    pygame.font.init()
    fontname = "assets/digital-7.mono.ttf"
    f = pygame.font.Font(fontname, 48)
    white = f.render("8888", True, (255,255,255))
    for i in range(NPLAYERS):
        t = f.render(str(PLAYERS[i]), False, COLORS[i])
        disp.blit(white, (900, i*40+20))
        disp.blit(t, (900, i*40+20))
    pygame.display.update()

def calculate_scores():
    global PLAYERS, board, boardp
    ADDS = {1:2, 2:5, 3:10, 10:-2, 11:-5, 12:-50, 13:-10}
    for i in range(len(board)):
        j = board[i]
        if j>=0:
            a = ADDS[j]
            p = int(boardp[i])
            PLAYERS[p] += a




NPLAYERS = int(input("Players? [1,2,3,4]"))
PLAYERS = NPLAYERS * [85]

draw()
draw_scores()
TURN = 0

f = True
while f:
    for event in pygame.event.get():
        if event.type==QUIT:
            f = False
            break
        if event.type==MOUSEBUTTONDOWN:
            x,y = event.pos
            if event.button==1:
                if -2 in board:
                    i = board.argmin()
                    if 850<=x<890:
                        if 20<=y<60:
                            board[i] = 1
                            PLAYERS[TURN] -= 4
                        if 60<=y<100:
                            board[i] = 2
                            PLAYERS[TURN] -= 10
                        if 100<=y<=140:
                            board[i] = 3
                            PLAYERS[TURN] -= 40
                        if 140<=y<180:
                            board[i] = 10
                            PLAYERS[TURN] -= 4
                        if 180<=y<220:
                            board[i] = 11
                            PLAYERS[TURN] -= 10
                        if 220<=y<260:
                            board[i] = 12
                            PLAYERS[TURN] -= 100
                        if 260<=y<300:
                            board[i] = 13
                            PLAYERS[TURN] -= 40
                        if 20<=y<300:
                            TURN += 1
                            TURN = TURN % NPLAYERS
                            calculate_scores()
                    continue
                for j in range(len(CLICKS)):
                    i = CLICKS[j]
                    if x>=i[0][0] and y>=i[0][1] and x<i[1][0] and y<i[1][1]:
                        boardp[j]=TURN
                        board[j] = -2
    draw()
    draw_scores()
