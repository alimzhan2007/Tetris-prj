from tkinter import *
from tkinter import messagebox
from random import choice, randrange
from copy import deepcopy
import time
import pygame
import pyglet

W, H = 13, 25
TILE = 35
GAME_RES = W * TILE, H * TILE
RES = 750, 940

music_list = ['music/y2mate.com - Tetris  Theme A Acapella.mp3',
              'music/y2mate.com - ППК  Воскрешение Robots Outro.mp3',
              'music/y2mate.com - Зодиак  Зодиак 1980 HQ  Хорошее качество.mp3',
              'music/groza.mp3',
              'music/tsoy.mp3']
music_order = 0
music_flag = False

pygame.mixer.init()
pyglet.font.add_file('tetris.ttf')


def play_bg(name):
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(name))
    pygame.mixer.Channel(0).set_volume(0.3)


def play(name):
    pygame.mixer.Channel(1).play(pygame.mixer.Sound(name))


def on_closing():
    global app_running
    if messagebox.askokcancel("Выход из приложения", "Хотите выйти из приложения?"):
        app_running = False
        #tk.destroy()


tk = Tk()
app_running = True
tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.title("Pentris")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
#tk.iconbitmap("bomb-3175208_640.ico")

sc = Canvas(tk, width=RES[0], height=RES[1], bg="red", highlightthickness=0)
sc.pack()

def get_record():
    try:
        with open('record2') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record2', 'w') as f:
            f.write('0')
        return "0"


def set_record(record, score):
    rec = max(int(record), score)
    with open('record2', 'w') as f:
        f.write(str(rec))


game_sc = Canvas(tk, width=W*TILE+1, height=H*TILE+1, bg="yellow", highlightthickness=0)
game_sc.place(x=20, y=30, anchor=NW)

img_obj1 = PhotoImage(file="img2/bg.png")
sc.create_image(0, 0, anchor=NW, image=img_obj1)

img_obj2 = PhotoImage(file="img2/bg2.png")
game_sc.create_image(0, 0, anchor=NW, image=img_obj2)

grid = [game_sc.create_rectangle(x * TILE, y * TILE, x * TILE+TILE, y * TILE+TILE) for x in range(W) for y in range(H)]

figures_pos = [[(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)],
                [(0, 0), (-1, 1), (-1, 0), (0, -1), (1, -1)],
                [(0, 0), (-1, 0), (-2, 0), (1, 0), (2, 0)],
                [(0, 0), (1, 0), (1, 1), (0, 1), (-1, 0)],
                [(0, 0), (0, 1), (1, 0), (-1, 0), (1, -1)],
                [(0, 0), (1, 0), (-1, 0), (1, 1), (-1, 1)],
                [(0, 0), (1, 0), (1, 1), (0, -1), (0, -2)],
                [(0, 0), (1, 0), (1, 1), (-1, 0), (-1, -1)],
                [(-1, 0), (0, 0), (1, 0), (-2, 0), (-2, -1)],
                [(-1, 0), (0, 0), (1, 0), (-2, 0), (0, -1)],
                [(0, -1), (0, 0), (0, 1), (1, -1), (2, -1)],
                [(0, 0), (0, -1), (1, -1), (-1, -1), (0, 1)]]

# figures_pos = [[(0, 0), (-1, 0), (-2, 0), (1, 0), (2, 0)],
#                 [(0, 0), (1, 0), (-1, 0), (1, 1), (-1, 1)]]


bonus_pos = [(1, 0), (1, 1), (0, 1), (0, 0), (1, -1)]
bonus = [[x + W // 2, y + 1] for x, y in bonus_pos]
figures = [[[x + W // 2, y + 1] for x, y in fig_pos] for fig_pos in figures_pos]
field = [[0 for i in range(W)] for j in range(H)]

anim_count, anim_speed, anim_limit = 0, 60, 2000

score, lines = 0, 0
bonus_flag = False
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
record = "0"

sc.create_text(520, 30,text="pentris", font=("tetris", 35),fill="red", anchor=NW)
sc.create_text(555, 780,text="score", font=("tetris", 35),fill="white", anchor=NW)
_score = sc.create_text(570, 840,text=str(score), font=("WiGuru 2", 35),fill="white", anchor=NW)
sc.create_text(545, 650,text="record", font=("tetris", 35),fill="white", anchor=NW)
_record = sc.create_text(570, 710,text=record, font=("WiGuru 2", 35),fill="gold", anchor=NW)

get_color = lambda : choice([(220, 20, 60), (255, 255, 0), (0, 255, 255), (0, 255, 0), (255, 0, 255), (25, 25, 112),
                             (255, 255, 255)])
get_color2 = lambda: (randrange(30, 255), randrange(30, 255), randrange(30, 255))

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def check_borders():
    if figure[i][0] < 0 or figure[i][0] > W - 1:
        return False
    elif figure[i][1] > H - 1 or field[figure[i][1]][figure[i][0]]:
        return False
    return True


def check_borders_bomb(i, j):
    if i < 0 or i > W - 1:
        return False
    elif j > H - 1 or j < 0:
        return False
    return True


def move_obj(event):
    global rotate, anim_limit, dx, music_flag
    if event.keysym == 'Up' or event.keysym == 'w':
        rotate = True
        anim_limit = 2000
    elif event.keysym == 'Left' or event.keysym == 'a':
        dx = -1
        anim_limit = 2000
    elif event.keysym == 'Right' or event.keysym == 'd':
        dx = 1
        anim_limit = 2000
    elif event.keysym == 'Down' or event.keysym == 's':
        anim_limit = 0.1
    elif event.keysym == 'z':
        music_flag = True


game_sc.bind_all("<KeyPress-Up>",move_obj)
game_sc.bind_all("<KeyPress-Down>",move_obj)
game_sc.bind_all("<KeyPress-Left>",move_obj)
game_sc.bind_all("<KeyPress-Right>",move_obj)
game_sc.bind_all("<w>",move_obj)
game_sc.bind_all("<s>",move_obj)
game_sc.bind_all("<a>",move_obj)
game_sc.bind_all("<d>",move_obj)
game_sc.bind_all("<z>",move_obj)


play_bg(music_list[music_order])
dx, rotate = 0, False
while app_running:
    if app_running:
        if not pygame.mixer.Channel(0).get_busy() or music_flag:
            if music_order + 1 == len(music_list):
                music_order = 0
            else:
                music_order += 1
            play_bg(music_list[music_order])
            music_flag = False
        record = get_record()
        # move x
        figure_old = deepcopy(figure)
        for i in range(5):
            figure[i][0] += dx
            if not check_borders():
                figure = deepcopy(figure_old)
                break
        # move y
        anim_count += anim_speed
        if anim_count > anim_limit:
            anim_count = 0
            figure_old = deepcopy(figure)
            for i in range(5):
                figure[i][1] += 1
                if not check_borders():
                    if bonus_flag:
                        for i in range(figure_old[0][1] - 4, figure_old[0][1] + 4):
                            for j in range(figure_old[0][0] - 4, figure_old[0][0] + 4):
                                if check_borders_bomb(j, i) and field[i][j]:
                                    field[i][j] = 0
                        play('music/smoke-bomb-6761.mp3')
                        bonus_flag = False
                    else:
                        for i in range(5):
                            field[figure_old[i][1]][figure_old[i][0]] = color
                        play('music/stuk-upavshey-na-pol-derevyashki.mp3')
                        pygame.mixer.Channel(1).set_volume(6.0)
                    figure, color = next_figure, next_color
                    next_figure, next_color = deepcopy(choice(figures)), get_color()
                    anim_limit = 2000
                    break
        # rotate
        center = figure[0]
        figure_old = deepcopy(figure)
        if rotate:
            for i in range(5):
                x = figure[i][1] - center[1]
                y = figure[i][0] - center[0]
                figure[i][0] = center[0] - x
                figure[i][1] = center[1] + y
                if not check_borders():
                    figure = deepcopy(figure_old)
                    break
        # check lines
        line, lines = H - 1, 0
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < W:
                line -= 1
            else:
                anim_speed += 3
                lines += 1
                bonus_flag = True
                figure = deepcopy(bonus)
        # compute score
        score += scores[lines]

        fig = []
        # draw figure
        if bonus_flag:
            for i in range(4):
                figure_rect_x = figure[i][0] * TILE
                figure_rect_y = figure[i][1] * TILE
                fig.append(game_sc.create_rectangle(figure_rect_x, figure_rect_y, figure_rect_x + TILE,
                                                    figure_rect_y + TILE, fill='black'))
            figure_rect_x = figure[4][0] * TILE
            figure_rect_y = figure[4][1] * TILE
            fig.append(game_sc.create_rectangle(figure_rect_x, figure_rect_y, figure_rect_x + TILE,
                                                figure_rect_y + TILE, fill='yellow'))
        else:
            for i in range(5):
                figure_rect_x = figure[i][0] * TILE
                figure_rect_y = figure[i][1] * TILE
                fig.append(game_sc.create_rectangle(figure_rect_x, figure_rect_y, figure_rect_x + TILE,
                                                    figure_rect_y + TILE, fill=rgb_to_hex(color)))

        # draw field
        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect_x, figure_rect_y = x * TILE, y * TILE
                    fig.append(game_sc.create_rectangle(figure_rect_x, figure_rect_y, figure_rect_x + TILE,
                                                        figure_rect_y + TILE, fill=rgb_to_hex(col)))

        fig2 = []
        # draw next figure
        for i in range(5):
            figure_rect_x = next_figure[i][0] * TILE + 400
            figure_rect_y = next_figure[i][1] * TILE + 185
            fig2.append(sc.create_rectangle(figure_rect_x, figure_rect_y, figure_rect_x + TILE, figure_rect_y + TILE,
                                fill=rgb_to_hex(next_color)))
        # draw titles
        sc.itemconfigure(_score, text=str(score))
        sc.itemconfigure(_record, text=record)
        anim_limit = 2000
        # game over
        for i in range(W):
            if field[0][i]:
                set_record(record, score)
                field = [[0 for i in range(W)] for i in range(H)]
                anim_count, anim_speed, anim_limit = 0, 60, 2000
                score = 0
                for item in grid:
                    game_sc.itemconfigure(item, fill=rgb_to_hex(get_color2()))
                    time.sleep(0.001)
                    tk.update_idletasks()
                    tk.update()

                for item in grid:
                    game_sc.itemconfigure(item, fill="")

        dx, rotate = 0, False
        tk.update_idletasks()
        tk.update()
        for id_fig in fig: game_sc.delete(id_fig)
        for id_fig in fig2: sc.delete(id_fig)
    time.sleep(0.0005)

tk.destroy()
#tk.mainloop()