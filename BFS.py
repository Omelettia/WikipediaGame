import pickle
from collections import deque
import time


def bfs_search(graph, starting_node, end_node):
# Sử dụng deque làm fringe để tốc độ nhanh hơn
    fringe = deque()
# Lưu node và đường đi đến node
    fringe.append((starting_node, [starting_node]))
    closed = set()
    fringe_set=set()
# Sử dụng set làm closed, điều này giúp kiểm tra phần tử có trong closed nhanh hơn
    i = 0 # Đếm số trang phải xét để tìm đến đích
    start_time = time.time()

    while fringe:
        i += 1
        node, path = fringe.popleft()
        closed.add(node)
        fringe_set.discard(node)
        if node == end_node:
            end_time = time.time()
            path_length = len(path)
            return path_length, path, end_time - start_time, i

        neighbors = set(graph.neighbors(node))
        for neighbor in neighbors:
            if neighbor not in closed and neighbor not in fringe_set:# Kiểm tra xem node con đã được đến chưa để tránh lặp
                fringe.append((neighbor, path + [neighbor]))
                fringe_set.add(neighbor)

    return None, None, None, i

if __name__ == "__main__":
 # Load đồ thị
 file_path = r"graph_with_attributes.pkl"

 with open(file_path, "rb") as file:
    graph = pickle.load(file)

 # Lấy bài đăng đích và bài đăng nguồn
 starting_node = input("starting article: ")
 end_node = input("ending article: ")

 path_length, path, running_time, node_visited = None,None,None, None
 # Check if the starting and goal nodes exist in the graph
 if graph.has_node(starting_node) and graph.has_node(end_node):
 # Thực hiện BFS
   path_length, path, running_time, node_visited = bfs_search(graph, starting_node, end_node)

 if path_length is not None:
    print("A path exists")
    print("Path:", path)
    print("Path length:", path_length)
    print("Running time:", running_time)
    print("Node_visited", node_visited)
 else:
    print("No path exists")
