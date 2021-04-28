# Các setup cần thiết để tạo chương trình hoạt động
import pygame as pg
from os import path
import heapq
vec = pg.math.Vector2

TILESIZE = 48  # kích thước ô đơn vị của map 48x48
GRIDWIDTH = 28
GRIDHEIGHT = 15
WIDTH = TILESIZE * GRIDWIDTH  # Chiều rộng
HEIGHT = TILESIZE * GRIDHEIGHT # Chiều cao
FPS = 30 # Tốc độ load khung hình

# Setup color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGRAY = (40, 40, 40)
MEDGRAY = (75, 75, 75)
LIGHTGRAY = (140, 140, 140)

# Khởi tọa pygame
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

font_name = pg.font.match_font('hack')