"""
Approximation function for Knapsack

Program is a fully-polynomial approximation of the knapsack.
The program works by initally rescaling all values in dataset
based on the highest found value. This allows for the execution of
the standard DP analysis, but due to the scaling a bound can be found
for the total difference between the found solution and the
actual optimal solution

Uses numpy, for matrix operations
"""

import argparse
import numpy as np
import sys

from functools import lru_cache

#Reads data from file
#Returns the number of items and weight from the first line
#Then returns the full dataset
def readData(fileName):
    f = open(fileName, 'r')
    tmp = (f.readline().split(' '))
    item = int(tmp[0])
    weight = int(tmp[1])
    data = []
    for line in f:
        data.append([int(i) for i in line.split()])
    return item,weight,data

#Scales the dataset based on EPS value
def scaler(items, eps, maxVal, data):
    val = eps * maxVal / items
    return [(int(i[0]/val), i[1]) for i in data]

#DP process
def dp(data, maxWeight, items):
    bestvalues = [[0] * (maxWeight + 1)
                  for i in range(items + 1)]
    
    for i, (value, weight) in enumerate(data):
        i += 1
        for capacity in range(maxWeight + 1):
            if weight > capacity:
                bestvalues[i][capacity] = bestvalues[i-1][capacity]
            else:
                bestvalues[i][capacity] = max(bestvalues[i-1][capacity], bestvalues[i-1][capacity - weight] + value)

    j = maxWeight
    i = items
    result = []
    
    while i > 0:
        if bestvalues[i][j] != bestvalues[i-1][j]:
            result.append(i-1)
            j -= data[i-1][1]
        i -= 1

    result.reverse()
    
    return bestvalues[items][maxWeight], result

#Outputs Data to location using name defined in naming conventions.
def writeData(fileName, result, data):
    f = open(fileName, 'w')
    val = 0
    for i in result:
        val += data[i][0]
    f.write(str(val))
    f.write('\n')
    f.write(str(result))
    return 

"""
Function call performs the whole approximation algorithm.

Starts by reading data from file, and then rescaling data.
Then runs the dynamic programming solution, and returns found values.
"""
def approximation(file, output, eps):
    #sys.setrecursionlimit(1000)
    items, weight, data = readData(file)

    maxprofit = np.array(data).max(axis=0)[1]
    scaled = scaler(items, eps, maxprofit, data)
    outputs = dp(scaled, weight, items)
    print(outputs)
    writeData(output, outputs[1], data)

    return 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Arguments to execute the fully-polynomial approximation of Knapsack Problem.")
    parser.add_argument('--file', help='Location of file to analyze')
    parser.add_argument('--output', help="Location to output files. Output will have the same name as input.")
    parser.add_argument('--eps', help="Epsilon value for bounding approximation. Smaller makes you more accurate, but may run slower", default='0.1')
    args = parser.parse_args()

    approximation(args.file, args.output, float(args.eps))