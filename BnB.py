import os
import time
import threading

class Item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

class Node:
    def __init__(self, level, value, weight, bound, contains):
        self.level = level
        self.value = value
        self.weight = weight
        self.bound = bound
        self.contains = contains

def bound(node, n, W, items):
    if node.weight >= W:
        return 0
    else:
        profit_bound = node.value
        j = node.level + 1
        totweight = node.weight
        while j < n and totweight + items[j].weight <= W:
            totweight += items[j].weight
            profit_bound += items[j].value
            j += 1
        if j < n:
            profit_bound += (W - totweight) * items[j].value / items[j].weight
        return profit_bound

def knapsack_branch_bound(items, W, timeout_event):
    items.sort(key=lambda x: x.value/x.weight, reverse=True)
    n = len(items)
    Q = []
    Q.append(Node(-1, 0, 0, float('inf'), []))
    maxProfit = 0
    bestCombination = None
    
    start_time = time.time()

    while Q and not timeout_event.is_set():
        current_time = time.time()
        if current_time - start_time > 30:
            timeout_event.set()
            break

        v = Q.pop(0)
        if v.level == -1:
            u_level = 0
        else:
            u_level = v.level + 1
        
        if u_level == n:
            continue
        u = Node(u_level, v.value + items[u_level].value, v.weight + items[u_level].weight, 0, v.contains + [1])
        if u.weight <= W and u.value > maxProfit:
            maxProfit = u.value
            bestCombination = u.contains
        u.bound = bound(u, n, W, items)
        if u.bound > maxProfit:
            Q.append(u)
        u = Node(u_level, v.value, v.weight, 0, v.contains + [0])
        u.bound = bound(u, n, W, items)
        if u.bound > maxProfit:
            Q.append(u)

    includes = [0] * n
    for i, include in enumerate(bestCombination or []):
        includes[i] = include
    return maxProfit, includes

def process_file(file_name, items, W):
    timeout_event = threading.Event()
    result = [None]  # Use a mutable object to store the result
    knapsack_thread = threading.Thread(target=lambda: result.__setitem__(0, knapsack_branch_bound(items, W, timeout_event)))
    knapsack_thread.start()
    knapsack_thread.join(timeout=1800)
    if knapsack_thread.is_alive():
        timeout_event.set()
        knapsack_thread.join()
        print(f"Timeout reached for {file_name}. Returning best solution found so far.")
    return result[0]

def process_files_in_directory(directory, file_pattern, num_files):
    for i in range(1, num_files + 1):
        file_name = os.path.join(directory, file_pattern.format(i))
        if os.path.isfile(file_name):
            items, W = read_input_file(file_name)
            start_time = time.time()
            max_profit, included_items = process_file(file_name, items, W) or (0, [])
            end_time = time.time()
            running_time = end_time - start_time
            output_file_name = f"{file_name}_output.txt"
            write_output_file(output_file_name, max_profit, included_items)
            print(f"Processed {file_name}: Maximum value = {max_profit}, Running time = {running_time:.2f} seconds")
        else:
            print(f"File {file_name} does not exist.")

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        n, W = map(int, file.readline().split())
        items = []
        for _ in range(n):
            value, weight = map(float, file.readline().split())
            items.append(Item(value, weight))
    return items, W

def write_output_file(output_path, max_profit, included_items):
    with open(output_path, 'w') as file:
        if included_items:
            file.writelines(f"{item}\n" for item in included_items)
        else:
            file.write("No solution found or timeout occurred.\n")

test_directory = 'large_scale'
file_pattern = "large_{:d}"


num_files = 21  


process_files_in_directory(test_directory, file_pattern, num_files)
