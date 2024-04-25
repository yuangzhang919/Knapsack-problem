"""
Executable File

Works as a sort of "root", where you can call all the algorithms.
All necessary arguments have been defined using arg-parse. To use simply type:
    python3 exec.py --help
This command will print out all required arguments, and how to set and use them.
"""
import approximation
import BnB
import LS

import argparse

def main():
    parser = argparse.ArgumentParser(description="Run a Knapsack Algorithm")
    parser.add_argument("-inst", type=str, required=True, help="Input file name")
    parser.add_argument("-alg", type=str, required=True, choices=["BnB", "Approx", "LS1", "LS2"], help="Algorithm to use")
    parser.add_argument("-time", required=True, type=int, help="Cut-off time in seconds")
    parser.add_argument("-seed", required=True, type=int, help="Random seed")
    args = parser.parse_args()

    #print(args)

    if args.alg == "Approx":
        #Approximation function
        out = args.inst + "_Approx.sol"
        approximation.approximation(args.inst, out)

    elif args.alg == "BnB":
        #Branch and Bound Algorithm
        items, W = BnB.read_input_file(args.inst)
        max_profit, included_items = BnB.process_file(args.inst, items, W, timeout=args.time) or (0, [])
        output_file_name = f"{args.inst}_{args.alg}_{args.time}.sol"
        BnB.write_output_file(output_file_name, max_profit, included_items)

    elif args.alg == "LS1" or args.alg == "LS2":
        # Parse the knapsack input file to get values, weights, and capacity
        values, weights, capacity = LS.parse_knapsack_file(args.inst)

        # Execute the selected algorithm
        if args.alg == "LS1":
            # Simulated Annealing function
            # Define Simulated Annealing parameters
            initial_temp = 100
            final_temp = 1
            alpha = 0.99  # Ensure alpha is defined

            best_solution, best_value, solution_trace = LS.simulated_annealing(
                values, weights, capacity, initial_temp, final_temp, alpha, args.time, args.seed)

        elif args.alg == "LS2":
            # Hill Climbing function
            best_solution, best_value, solution_trace = LS.hill_climbing(values, weights, capacity, args.time, args.seed)

        # Save solution and trace files
        solution_filename = f"{args.inst}_{args.alg}_{args.time}_{args.seed}.sol"
        trace_filename = f"{args.inst}_{args.alg}_{args.time}_{args.seed}.trace"

        LS.save_solution(solution_filename, best_solution, best_value)  # Save best solution
        LS.save_trace(trace_filename, solution_trace)  # Save trace with timestamps and quality

if __name__ == "__main__":
    main()
