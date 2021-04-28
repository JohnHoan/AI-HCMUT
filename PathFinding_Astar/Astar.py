from setup import  *

#Khởi tạo 1 hàng đợi ưu tiên để phục vụ giải thuật A*
class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))

    def get(self):
        return heapq.heappop(self.nodes)[1]

    def empty(self):
        return len(self.nodes) == 0


def vec2int(v):
    return (int(v.x), int(v.y))

#Hàm h(x) định lượng từ node hiện tại tới đích, x10 giá trị để làm tròn.
def heuristic(a, b):
    return (abs(a.x - b.x) + abs(a.y - b.y)) * 10


#Giải thuật A*
def a_star_search(graph, start, end):
    frontier = PriorityQueue()
    frontier.put(vec2int(start), 0)
    # Lưu trữ đường đi
    path = {}
    # Lưu trữ định lượng quãng đường
    cost = {}
    path[vec2int(start)] = None
    cost[vec2int(start)] = 0 

    while not frontier.empty():
        # Duyệt các node theo mức độ ưu tiên
        current = frontier.get()
        if current == end:
            break
        # Duyệt từng node kế tiếp trong danh sách node hàng xóm của node hiện tại
        for next in graph.find_neighbors(vec(current)):
            next = vec2int(next)
            # Định lượng g(x): start -> next, nếu next chưa đc định lượng hoặc
            # có định lượng mới tốt hơn thì thêm vào hàng đợi ưu tiên
            next_cost = cost[current] + graph.cost(current, next) 
            if next not in cost or next_cost < cost[next]:
                cost[next] = next_cost
                # f(x) = g(x) + h(x)
                priority = next_cost + heuristic(end, vec(next))
                frontier.put(next, priority)
                path[next] = vec(current) - vec(next)
    return path, cost
