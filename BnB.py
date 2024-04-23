import os

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
        while j < n and totweight + items[j][1].weight <= W:
            totweight += items[j][1].weight
            profit_bound += items[j][1].value
            j += 1
        if j < n:
            profit_bound += (W - totweight) * items[j][1].value / items[j][1].weight
        return profit_bound

def knapsack_branch_bound(items, W):
    items = sorted(enumerate(items), key=lambda x: x[1].value/x[1].weight, reverse=True)
    #items.sort(key=lambda x: x.value/x.weight, reverse=True)
    n = len(items)
    Q = []



    Q.append(Node(-1, 0, 0, float('inf'), [0] * n))
    maxProfit = 0
    bestCombination = None
    
    while Q:
        v = Q.pop(0)
        if v.level == -1:
            u_level = 0
        else:
            u_level = v.level + 1
        
        if u_level == n:
            continue


        u = Node(u_level, v.value + items[u_level][1].value, v.weight + items[u_level][1].weight, 0, v.contains.copy())
        u.contains[items[u_level][0]] = 1
        if u.weight <= W and u.value > maxProfit:
            maxProfit = u.value
            bestCombination = u.contains

        u.bound = bound(u, n, W, items)
        if u.bound > maxProfit:
            Q.append(u)


        u = Node(u_level, v.value, v.weight, 0, v.contains.copy())
        u.bound = bound(u, n, W, items)
        if u.bound > maxProfit:
            Q.append(u)


    includes = [0] * n
    for i, include in enumerate(bestCombination):
        includes[i] = include

    return maxProfit, includes




def read_input_file(file_path):
    with open(file_path, 'r') as file:
        n, W = map(int, file.readline().split())
        items = []
        for _ in range(n):
            value, weight = map(int, file.readline().split())
            items.append(Item(value, weight))
    return items, W

def write_output_file(output_path, max_profit, included_items):
    with open(output_path, 'w') as file:
        file.writelines(f"{item}\n" for item in included_items)

def process_files_in_directory(directory, file_pattern, num_files):
    for i in range(1, num_files + 1):
        file_name = os.path.join(directory, file_pattern.format(i))
        if os.path.isfile(file_name):
            items, W = read_input_file(file_name)
            max_profit, included_items = knapsack_branch_bound(items, W)
            output_file_name = f"{file_name}_output.txt"
            write_output_file(output_file_name, max_profit, included_items)
            print(f"Processed {file_name}: Maximum value in knapsack = {max_profit}")
        else:
            print(f"File {file_name} does not exist.")

# The directory where your test files are located
test_directory = 'data/test'  # Replace this with the actual path to your test directory

# File pattern to match your files
file_pattern = "KP_s_{:02d}"  # Adjust the padding as needed based on the file names

# Number of files to process
num_files = 8  # Update this to match the number of files you have

# Process the files
process_files_in_directory(test_directory, file_pattern, num_files)
