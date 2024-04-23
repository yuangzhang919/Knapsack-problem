"""
Approximation function for Knapsack

Program is a 2-approximation of the knapsack.

It works by naively sorting all values by "value density" (value/weight),
Then naively attempts to just take the highest value item at all points.
"""

import argparse
from time import time

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

#Outputs Data to location using name defined in naming conventions.
def writeData(fileName, result, value):
    f = open(fileName, 'w')
    f.write(str(value))
    f.write('\n')
    f.write(str(result))
    return 

#Approximation Algorithm
def greedy(items, maxWeight, data):
    data.sort(reverse=True,key=lambda pt: pt[0]/pt[1])

    outputs = []
    weight = 0
    value = 0
    i = 0
    while i < items:
        if (weight + data[i][1] <= maxWeight):
            outputs.append(i)
            weight += data[i][1]
            value += data[i][0]
        i += 1
    return outputs, value

"""
Function call performs the whole approximation algorithm.

Starts by reading data from file, and then rescaling data.
Then runs the dynamic programming solution, and returns found values.
"""
def approximation(file, output):
    items, weight, data = readData(file)
    outputs, value = greedy(items, weight, data)
    writeData(output, outputs, value)

    return 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Arguments to execute the fully-polynomial approximation of Knapsack Problem.")
    parser.add_argument('--file', help='Location of file to analyze')
    parser.add_argument('--output', help="Location to output files. Output will have the same name as input.")
    args = parser.parse_args()
    t_start = time()
    approximation(args.file, args.output)
    end = time() - t_start
    print('Took: ' + str(end))