import sys
import pygame
import pygame_menu
import subprocess
import webbrowser
python_interpreter = 'python'
script_path = 'main_tkinter.py'



pygame.init()
pygame.mixer.Channel(0).play(pygame.mixer.Sound('music/y2mate.com - Tetris Theme SlowedReverb Tetris.mp3'))
pygame.mixer.Channel(0).set_volume(0.3)
surface = pygame.display.set_mode((700, 600))


def start_the_game():
    pygame.mixer.Channel(0).stop()
    subprocess.call([python_interpreter, script_path])
    pygame.quit()
    sys.exit()
    pass


def start_the_game2():
    pygame.mixer.Channel(0).stop()
    subprocess.call([python_interpreter, '2_mode.py'])
    pygame.quit()
    sys.exit()
    pass
url = "https://sites.google.com/fizmat.kz/tetris/команда-разработчиков?authuser=0"


def open_web():
    webbrowser.open(url)
    pass


menu = pygame_menu.Menu('Hello world!', 700, 600,
                       theme=pygame_menu.themes.THEME_DARK)
menu.add.button('Tetris', start_the_game, font_size=60)
menu.add.button('Pentris', start_the_game2, font_size=60)
menu.add.button('Genius', open_web, font_size=60)

menu.add.button('Quit', pygame_menu.events.EXIT, font_size=60)
menu.mainloop(surface)