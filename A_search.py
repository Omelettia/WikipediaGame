import pickle
from heapdict import heapdict
import time

# Load mô hình đã luyện từ file
with open("trained_model.pkl", "rb") as file:
    model = pickle.load(file)

# Load vectorizer từ file
with open("vectorizer.pkl", "rb") as file:
    vectorizer = pickle.load(file)

# Load đồ thị
file_path = r"graph_with_attributes.pkl"
with open(file_path, "rb") as file:
    graph = pickle.load(file)

def astar(graph, start, goal):
    # Cache để lưu các giá trị heuristic đã tính; hạn chế tính lại nhiều lần
    heuristic_cache = {}
    # Dùng Priority queue để sắp xếp các node; từ đó tìm node có priority thấp nhất
    open_nodes = heapdict()
    open_nodes[start] = 0

    # Từ điển để chứa các path lengths ngắn nhất từ node nguồn
    path_lengths = {node: float("inf") for node in graph.nodes}
    path_lengths[start] = 0

    # Từ điển để chứa node trước trong đường đi
    previous_nodes = {node: None for node in graph.nodes}

    # Đếm số node đã thăm
    visited_nodes = 0

    # Xác định thời gian bắt đầu chạy
    start_time = time.time()

    while open_nodes:
        current_node, _ = open_nodes.popitem()
        visited_nodes += 1

        if current_node == goal:
            # Tạo đường đi từ node nguồn tới đích khi tìm ra đường đi
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = previous_nodes[current_node]
            path.reverse()
            # Tính thời gian chạy
            runtime = time.time() - start_time
            return path, visited_nodes, runtime, len(path)
        neighbors = set(graph.neighbors(current_node)) #Dùng set để tránh các link bị duplicate
        for neighbor in neighbors:
            path_length = path_lengths[current_node] + 1

            if path_length < path_lengths[neighbor]:
                path_lengths[neighbor] = path_length
                previous_nodes[neighbor] = current_node
                # Kiểm tra trực tiếp neighbor có phải là goal không
                if neighbor == goal:
                  heuristic_value = 1
                else:
                # Kiểm tra xem goal có nằm trong neighbor của neighbor không
                  neighbor_neighbors = set(graph.neighbors(neighbor))
                  if goal in neighbor_neighbors:
                      heuristic_value = 2
                  else:
                      #Tính hàm heuristic và trừ đi 1 để có ước lượng chấp nhận được
                      heuristic_value = heuristic(neighbor, goal, heuristic_cache) - 1
                      if heuristic_value < 3:
                      #Đẩy lên trên các giá trị heuristic mà kết quả không chính xác và bị lệch xuống
                          heuristic_value = 3
                priority = path_length + heuristic_value
                heuristic_cache[neighbor] = heuristic_value
                if neighbor in open_nodes:
                    del open_nodes[
                        neighbor]  # Loại bỏ node neighbor để update priority của nó nếu nó có trong open_nodes
                open_nodes[neighbor] = priority

    # Nếu không có đường đi
    return None, visited_nodes, None, None

def heuristic(source, target, cache):
    # Kiểm tra xem giá trị heuristic đã được tính chưa
    cached_value = cache.get(source)
    if cached_value is not None:
        return cached_value
    # Lấy các attributes của node nguồn
    source_attributes = graph.nodes[source]

    # Sắp xếp các attributes thành định dạng đúng
    formatted_attributes = [
        source,
        target,
        source_attributes.get("Word Count"),
        source_attributes.get("Link Count"),
        source_attributes.get("Bag of Words"),
    ]

    # Xử lý các giá trị thiếu trong attributes
    formatted_attributes = ["" if attr is None else attr for attr in formatted_attributes]

    # Tokenize và vectorize formatted attributes dựa trên vectorizer đã load
    formatted_attributes_vectorized = vectorizer.transform([formatted_attributes[4]])

    # Dự đoán path length dựa trên mô hình
    path_length = model.predict(formatted_attributes_vectorized)[0]
    cache[source] = path_length
    # Lưu kết quả vào cache
    return path_length

if __name__ == "__main__":
    # Nhập bài đăng đầu và đích
    starting_node = input("Enter the starting node: ")
    end_node = input("Enter the goal node: ")

    # Kiểm tra xem chúng có trong đồ thị không
    if graph.has_node(starting_node) and graph.has_node(end_node):
        # Tìm đường đi dùng A*
        path, node_count, runtime, path_length = astar(graph, starting_node, end_node)

        if path:
            print("Path:", path)
            print("Number of nodes visited:", node_count)
            print("Path length:", path_length)
            print("Runtime:", runtime)
        else:
            print("No path found.")
    else:
        print("Starting node or goal node not found in the graph.")
