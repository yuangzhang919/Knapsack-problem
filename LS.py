import random
import math
import time
import argparse
import os

# Simulated Annealing Algorithm
def simulated_annealing(values, weights, capacity, initial_temp, final_temp, alpha, cutoff_time, random_seed):
    # Initialize the knapsack
    n = len(values)
    current_solution = [random.choice([0, 1]) for _ in range(n)]
    current_value = sum(v for i, v in enumerate(values) if current_solution[i] == 1)
    current_weight = sum(w for i, w in enumerate(weights) if current_solution[i] == 1)

    # Ensure capacity isn't exceeded
    while current_weight > capacity:
        idx = random.choice([i for i, s in enumerate(current_solution) if s == 1])
        current_solution[idx] = 0
        current_value -= values[idx]
        current_weight -= weights[idx]

    best_solution = current_solution[:]
    best_value = current_value

    # Track improved solutions with timestamps and quality
    solution_trace = []
    start_time = time.time()  # Initialize once, before the loop
    print("Start time:", start_time)
    solution_trace.append((0.00, best_value))  # Initial trace entry

    temperature = initial_temp  # Start with the initial temperature



    # Simulated Annealing loop
    while temperature > final_temp and (time.time() - start_time) < cutoff_time:
        idx = random.randint(0, n - 1)  # Randomly select neighboring solution
        new_solution = current_solution[:]
        new_solution[idx] = 1 - current_solution[idx]  # Flip the selection state

        new_value = current_value + (values[idx] if new_solution[idx] == 1 else -values[idx])
        new_weight = current_weight + (weights[idx] if new_solution[idx] == 1 else -weights[idx])

        # If new weight exceeds capacity, skip this solution
        if new_weight > capacity:
            continue

        # Calculate acceptance probability
        delta = new_value - current_value
        acceptance_probability = math.exp(delta / temperature) if delta < 0 else 1.0

        # Accept or reject based on probability
        if random.random() < acceptance_probability:
            current_solution = new_solution
            current_value = new_value
            current_weight = current_weight + (weights[idx] if new_solution[idx] == 1 else -weights[idx])

            # Correctly update trace only when a new best solution is found
            timestamp = time.time() - start_time
            if current_value > best_value:
                best_solution = current_solution[:]
                best_value = current_value
                solution_trace.append((timestamp, best_value))


        # Lower temperature
        temperature *= alpha  # Gradually reduce temperature
    print("Trace updated with timestamp:", timestamp, "and quality:", best_value)  # Check trace updates
    return best_solution, best_value, solution_trace

# Hill Climbing Algorithm with Correct Initialization and Trace Updates
def hill_climbing(values, weights, capacity, cutoff_time, random_seed):
    random.seed(random_seed)  # Set the random seed for reproducibility

    # Initialize the knapsack
    n = len(values)
    current_solution = [random.choice([0, 1]) for _ in range(n)]  # Random initial solution
    current_value = sum(v for i, v in enumerate(values) if current_solution[i] == 1)
    current_weight = sum(w for i, w in enumerate(weights) if current_solution[i] == 1)

    # Ensure the initial solution doesn't exceed capacity
    while current_weight > capacity:
        idx = random.choice([i for i, s in enumerate(current_solution) if s == 1])
        current_solution[idx] = 0
        current_value -= values[idx]
        current_weight -= weights[idx]

    best_solution = current_solution[:]
    best_value = current_value  # Best initial value

    # Correct initialization and trace updates
    solution_trace = []
    start_time = time.time()  # Initialize before the loop begins
    solution_trace.append((0.0, best_value))  # Initial trace entry with best value
    print(f"Initial best value: {best_value}, Initial timestamp: {start_time}")
    
    # Hill Climbing loop
    loop_count = 0
    while (time.time() - start_time) < cutoff_time:
        current_time = time.time()  # Track current time
        elapsed_time = current_time - start_time  # Calculate elapsed time
        loop_count += 1


        best_neighbor_solution = None
        best_neighbor_value = -1

        # Explore neighboring solutions
        for idx in range(n):
            # Consider both inclusion and exclusion
            for state in [0, 1]:
                if current_solution[idx] == state:
                    continue  # Skip if there's no change

                new_solution = current_solution[:]
                new_solution[idx] = state  # Flip the state

                new_value = sum(v for i, v in enumerate(values) if new_solution[i] == 1)
                new_weight = sum(w for i, w in enumerate(weights) if new_solution[i] == 1)

                # Skip if the new solution exceeds capacity
                if new_weight > capacity:
                    continue  # Ensure capacity constraint

                if new_value > best_neighbor_value:
                    best_neighbor_solution = new_solution
                    best_neighbor_value = new_value

        # If no better neighbor is found, break the loop
        if best_neighbor_solution is None or best_neighbor_value <= current_value:
            break  # Exit if no improvement

        # Update trace only when there's a new best solution
        if best_neighbor_solution and best_neighbor_value > best_value:
            best_solution = best_neighbor_solution[:]
            best_value = best_neighbor_value
            timestamp = time.time() - start_time  # Correct elapsed time

            solution_trace.append((timestamp, best_value))  # Proper trace update

        # Avoid redundant trace updates
        if best_neighbor_solution and best_neighbor_value > current_value:
            current_solution = best_neighbor_solution
            current_value = best_neighbor_value

            # Only update trace if there's a significant improvement
            if best_neighbor_value > current_value:
                timestamp = time.time() - start_time  # Accurate timestamp
                solution_trace.append((timestamp, current_value))  # Correct trace update
                
    final_timestamp = time.time() - start_time  # Final elapsed time
    print("Final best value:", best_value, "Final timestamp:", final_timestamp)
    return best_solution, best_value, solution_trace

# Function to save solution to a file
def save_solution(filename, solution, best_value):
    with open(filename, 'w') as f:
        f.write(f"{best_value}\n")  # Total quality of the best solution
        selected_items = [str(idx) for idx, s in enumerate(solution) if s == 1]
        f.write(",".join(selected_items) + "\n")  # List of selected item indices


# Function to save trace to a file
def save_trace(filename, trace):
    with open(filename, 'w') as f:
        for entry in trace:
            f.write(f"{entry[0]:.3f}, {entry[1]}\n")  # Write timestamp and quality


# Function to parse the knapsack input file and handle non-integer values
def parse_knapsack_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        first_line = lines[0].strip().split()
        n = int(first_line[0])  # Ensure the first value is an integer
        capacity = int(first_line[1])  # Ensure the second value is an integer
        values = []
        weights = []

        # Parse the subsequent lines and handle non-integer cases
        for line in lines[1:]:
            try:
                v, w = map(float, line.strip().split())  # Use float to handle non-integer values
                values.append(int(v))  # Convert to integer if needed
                weights.append(int(w))  # Convert to integer if needed
            except ValueError:
                print(f"Invalid data: {line.strip()}")  # Debug non-integer values
                continue  # Skip invalid lines

    return values, weights, capacity  # Return parsed values, weights, and capacity


# Main function to execute the algorithm and save the outputs
def main():
    parser = argparse.ArgumentParser(description="Run a Knapsack Algorithm")
    parser.add_argument("-inst", type=str, required=True, help="Input file name")
    parser.add_argument("-alg", type=str, required=True, choices=["LS1", "LS2"], help="Algorithm to use")
    parser.add_argument("-time", required=True, type=int, help="Cut-off time in seconds")
    parser.add_argument("-seed", required=True, type=int, help="Random seed")
    args = parser.parse_args()

    # Parse the knapsack input file to get values, weights, and capacity
    values, weights, capacity = parse_knapsack_file(args.inst)

    # Execute the selected algorithm
    if args.alg == "LS1":
        # Simulated Annealing function
        # Define Simulated Annealing parameters
        initial_temp = 100
        final_temp = 1
        alpha = 0.99  # Ensure alpha is defined

        best_solution, best_value, solution_trace = simulated_annealing(
            values, weights, capacity, initial_temp, final_temp, alpha, args.time, args.seed)

    elif args.alg == "LS2":
        # Hill Climbing function
        best_solution, best_value, solution_trace = hill_climbing(values, weights, capacity, args.time, args.seed)

    # Save solution and trace files
    solution_filename = f"{args.inst}_{args.alg}_{args.time}_{args.seed}.sol"
    trace_filename = f"{args.inst}_{args.alg}_{args.time}_{args.seed}.trace"

    save_solution(solution_filename, best_solution, best_value)  # Save best solution
    save_trace(trace_filename, solution_trace)  # Save trace with timestamps and quality


if __name__ == "__main__":
    main()
