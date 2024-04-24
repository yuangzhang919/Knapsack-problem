import os
import subprocess
import time

small_scale_folder = './data/small_scale'
small_scale_solution_folder = './data/small_scale_solution'
large_scale_folder = './data/large_scale'
large_scale_solution_folder = './data/large_scale_solution'
output_folder = './output/approximation_outputs'

os.makedirs(output_folder, exist_ok=True)

small_scale_range = range(1, 11)
large_scale_range = range(1, 22)

def read_optimal_solution(file_path):
    try:
        with open(file_path, 'r') as file:
            optimal_value = float(file.readline().strip())
        return optimal_value
    except FileNotFoundError:
        print(f"Optimal solution file not found: {file_path}")
        return None

def run_approximation(instance_path, output_path):
    command = f"python approximation.py --file {instance_path} --output {output_path}"
    start_time = time.time()
    subprocess.run(command, shell=True)
    end_time = time.time()
    running_time = end_time - start_time
    
    with open(output_path, 'r') as file:
        lines = file.readlines()
        approximation_value = float(lines[0].strip())
    
    return running_time, approximation_value


for i in small_scale_range:
    instance_file = f"small_{i}"
    instance_path = os.path.join(small_scale_folder, instance_file)
    output_file = f"{instance_file}_approx.sol"
    output_path = os.path.join(output_folder, output_file)
    
    optimal_solution_file = f"small_{i}"
    optimal_solution_path = os.path.join(small_scale_solution_folder, optimal_solution_file)
    optimal_value = read_optimal_solution(optimal_solution_path)
    
    running_time, approximation_value = run_approximation(instance_path, output_path)
    
    if optimal_value is not None:
        rel_err = (optimal_value - approximation_value) / optimal_value
        print(f"Relative Error: {rel_err:.4f}")
    else:
        print("Relative Error: N/A")
    
    print(f"Instance: {instance_file}")
    print(f"Running Time: {running_time:.2f} seconds")
    print(f"Approximation Value: {approximation_value:.2f}")
    print(f"Optimal Value: {optimal_value:.2f}")
    print()

for i in large_scale_range:
    instance_file = f"large_{i}"
    instance_path = os.path.join(large_scale_folder, instance_file)
    output_file = f"{instance_file}_approx.sol"
    output_path = os.path.join(output_folder, output_file)
    
    optimal_solution_file = f"large_{i}"
    optimal_solution_path = os.path.join(large_scale_solution_folder, optimal_solution_file)
    optimal_value = read_optimal_solution(optimal_solution_path)
    
    running_time, approximation_value = run_approximation(instance_path, output_path)
    
    if optimal_value is not None:
        rel_err = (optimal_value - approximation_value) / optimal_value
        print(f"Relative Error: {rel_err:.4f}")
    else:
        print("Relative Error: N/A")
    
    print(f"Instance: {instance_file}")
    print(f"Approximation Value: {approximation_value:.2f}") 
    print(f"Optimal Value: {optimal_value:.2f}")
    print()