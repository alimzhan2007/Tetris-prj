import pygame

pygame.mixer.init()

def play_bg(name):
    # pygame.mixer.music.load('y2mate.com - Tetris  Theme A Acapella.mp3')
    # pygame.mixer.music.load('smoke-bomb-6761.mp3')
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(name))


def play(name):
    # pygame.mixer.music.load(name)
    # pygame.mixer.music.load('smoke-bomb-6761.mp3')
    pygame.mixer.Channel(1).play(pygame.mixer.Sound(name))


pygame.mixer.Channel(0).play(pygame.mixer.Sound('music/smoke-bomb-6761.mp3'))
if pygame.mixer.Channel(0).get_busy():
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('music/y2mate.com - Tetris  Theme A Acapella.mp3'))