import pickle
import time

# Load đồ thị
file_path = r"graph_with_attributes.pkl"
with open(file_path, "rb") as file:
    graph = pickle.load(file)

def iddfs_search(graph, starting_node, end_node, max_depth):
    def iddfs(node, path, depth):
        nonlocal node_count

        if node == end_node:
            return path, len(path), time.time() - start_time

        if depth > 0:
            node_count += 1
            neighbors = set(graph.neighbors(node))

            for neighbor in neighbors:
                if neighbor not in path:
                    result = iddfs(neighbor, path + [neighbor], depth - 1)
                    if result[0] is not None:
                        return result

        return None, None, None

    node_count = 0
    start_time = time.time()
    for depth in range(1, max_depth + 1):
        result = iddfs(starting_node, [starting_node], depth)
        if result[0] is not None:
            return result + (node_count,)

    return None, None, None, node_count


if __name__ == "__main__":
    max_depth = 10  # Giới hạn độ sâu tối đa

    starting_node = input("starting article: ")
    end_node = input("ending article: ")
    path, path_length, runtime, node_count = iddfs_search(
        graph, starting_node, end_node, max_depth)

    if path:
        print("A path exists")
        print("Path:", path)
        print("Path length:", path_length)
        print("Runtime:", runtime)
    else:
        print("No path exists")

    print("Number of nodes visited:", node_count)
