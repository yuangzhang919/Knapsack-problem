# Knapsack-problem

We have solved the knapsack problem using a Branch and Bound algorithm, an 2-Approximation Algorithm, and 2 Local Search Algorithms of Simulated Annealing and Hill Search.

All overarching algorithm are stored in the respective file corresponding to the type of algorithm:
    BnB: Branch and Bound Algorithm
    approximation: 2-Approximation Algorithm
    LS: Simulated Annealing and Hill Search Local Search ALgorithms

All files can be run using the exec file. To call it, simply run:
    python3 exec.py -inst <filename> -alg <Algorithm> -time <timeout> -seed <Random Seed>

This will output a corresponding file described in the original problem requirements, and a trace file if running Branch and Bound or Local Search.

More information about each field and how to run the command can be found in the exec file itself at the head.

All output data is stored in the output folder. The outputs for each algorithm, and trace files, can be found under the folder corresponding to the algorithm's name.
BnB output and trace are missing due to errors in output processing.

Our report is also included as a pdf.

run_approximation.py was a utility file used to rapidly produce outputs, and should be ignored for simulations.