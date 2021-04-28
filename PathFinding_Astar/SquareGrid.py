from setup import *

#Class SquareGrid dùng để tạo chướng ngại vật, tạo các node cần thiết cho chương trình
# program map : 00 10 20 30 40
#               01 11 21 31 41
#               02 12 22 32 42
#               03 13 23 33 43

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        # Duyệt các node lân cận node hiện tại : 00 => 01 10 0-1 -10 11 -11 1-1 -1-1
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]
        self.connections += [vec(1, 1), vec(-1, 1), vec(1, -1), vec(-1, -1)]

    # Loại các node ngoài tầm vực map như 0-1  -10 -11 1-1 -1-1
    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    # Kiểm tra xem node input có phải là chướng ngại vật ko
    def passable(self, node):
        return node not in self.walls

    # Neighbors là các node lân cận trong tầm vực map và ko phải wall
    def find_neighbors(self, node):
        neighbors = [node + connection for connection in self.connections]
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors

    # Hàm định lượng giữa 2 node. Quãng đường thằng = 1, chéo = sqrt(2), làm tròn các giá trị bằng cách x10.
    def cost(self, from_node, to_node):
        if (vec(to_node) - vec(from_node)).length_squared() == 1:
            # Chi phí khi đi theo đường thẳng
            return  10
        else:
            # Chi phí khi đi theo đường chéo
            return  14

    # Vẽ walls
    def draw(self):
        for wall in self.walls:
            rect = pg.Rect(wall * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, LIGHTGRAY, rect)