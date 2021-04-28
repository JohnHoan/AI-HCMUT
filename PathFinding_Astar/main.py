from setup import *
from Astar import *
from SquareGrid import *

# Vẽ lưới ô caro cho background
def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (0, y), (WIDTH, y))

# Vẽ icon start và goal =  tọa độ nhân cho đơn vị ô, sau đó căn giữa
def draw_icons():
    start_center = (goal.x * TILESIZE + TILESIZE / 2, goal.y * TILESIZE + TILESIZE / 2)
    screen.blit(home_img, home_img.get_rect(center=start_center))
    goal_center = (start.x * TILESIZE + TILESIZE / 2, start.y * TILESIZE + TILESIZE / 2)
    screen.blit(cross_img, cross_img.get_rect(center=goal_center))


# Gọi đường dẫn tới các images cần thiết cho program và lưu vào các biến
icon_dir = path.join(path.dirname(__file__), '../PATHFINDING')
home_img = pg.image.load(path.join(icon_dir, 'home1.png')).convert_alpha()
home_img = pg.transform.scale(home_img, (50, 50))
home_img.fill(GREEN, special_flags=pg.BLEND_RGBA_MULT)
cross_img = pg.image.load(path.join(icon_dir, 'cross.png')).convert_alpha()
cross_img = pg.transform.scale(cross_img, (50, 50))
cross_img.fill(RED, special_flags=pg.BLEND_RGBA_MULT)
foot = pg.image.load(path.join(icon_dir, 'images.png')).convert_alpha()
foot = pg.transform.scale(foot, (40, 40))


# Khởi tạo map
g = SquareGrid(GRIDWIDTH, GRIDHEIGHT)


# Khởi tạo vật cản/wall
walls = [(10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (16, 7), (7, 7), (6, 7), (5, 7), (5, 5), (5, 6), (1, 6), (2, 6), (3, 6), (5, 10), (5, 11), (5, 12), (5, 9), (5, 8), (12, 8), (12, 9), (12, 10), (12, 11), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10), (17, 7), (18, 7), (21, 7), (21, 6), (21, 5), (21, 4), (21, 3), (22, 5), (23, 5), (24, 5), (25, 5), (18, 10), (20, 10), (19, 10), (21, 10), (22, 10), (23, 10), (14, 4), (14, 5), (14, 6), (14, 0), (14, 1), (9, 2), (9, 1), (7, 3), (8, 3), (10, 3), (9, 3), (11, 3), (2, 5), (2, 4), (2, 3), (2, 2), (2, 0), (2, 1), (0, 11), (1, 11), (2, 11), (21, 2), (20, 11), (20, 12), (23, 13), (23, 14), (24, 10), (25, 10), (6, 12), (7, 12), (10, 12), (11, 12), (12, 12), (5, 3), (6, 3), (5, 4)]
for wall in walls:
    g.walls.append(vec(wall))


# Thiết lập tọa độ mục tiêu và giải thuật
goal = vec(14, 8)
start = vec(0, 0)
search_type = a_star_search
path, c = search_type(g, goal, start)


# Vòng lặp chạy game trên từng khung thời gian :30fps
running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # Thêm và xóa wall tùy ý, sau đó gọi lại giải thuật cho map mới
        if event.type == pg.MOUSEBUTTONDOWN:
            mpos = vec(pg.mouse.get_pos()) // TILESIZE
            if event.button == 1:
                if mpos in g.walls:
                    g.walls.remove(mpos)
                else:
                    g.walls.append(mpos)
            path, c = search_type(g, goal, start)

    # Phủ nền
    screen.fill(DARKGRAY)
    
    # Vẽ các node đc khám phá trong quá trình tìm đường
    for node in path:
        x, y = node
        rect = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
        pg.draw.rect(screen, MEDGRAY, rect)
    
    draw_grid()
    g.draw()

    # vẽ đường đi từ start -> goal
    current = start 
    while current != goal:
        # vẽ path, cách thức vẽ từng node path như đã nói bên trên
        img = foot
        x = current.x * TILESIZE + TILESIZE / 2
        y = current.y * TILESIZE + TILESIZE / 2
        r = img.get_rect(center=(x, y))
        if  current != start:
            screen.blit(img, r)
        # gọi node kế tiếp
        current = current + path[vec2int(current)]
    draw_icons()
    pg.display.flip()
