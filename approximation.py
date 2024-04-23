"""
Approximation function for Knapsack

Program is a 2-approximation of the knapsack.

It works by naively sorting all values by "value density" (value/weight),
Then naively attempts to just take the highest value item at all points.
"""

import argparse
import os
from time import time

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
    data = sorted(enumerate(data), reverse=True,key=lambda pt: pt[1][0]/pt[1][1])

    outputs = []
    weight = 0
    value = 0
    i = 0
    while i < items:
        weight += data[i][1][1]
        if (weight > maxWeight):
            if data[i][1][0] > value:
                return [data[i][0]], data[i][1][0]
            return outputs, value
        
        outputs.append(data[i][0])
        weight += data[i][1][1]
        value += data[i][1][0]
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
    return value

#Specialized function for processing data outputs quickly
def process_submission():
    # The directory where your test files are located
    directory = 'data/test'  # Replace this with the actual path to your test directory

    # File pattern to match your files
    file_pattern = "KP_s_{:02d}"  # Adjust the padding as needed based on the file names

    # Number of files to process
    num_files = 8  # Update this to match the number of files you have
    
    for i in range(1, num_files + 1):
        file_name = os.path.join(directory, file_pattern.format(i))
        if os.path.isfile(file_name):
            output_file_name = f"{file_name}_output.txt"
            t_start = time()
            value = approximation(file_name, output_file_name)
            end = time() - t_start
            print('Took: ' + str(end))
            print('Final Value: ' + str(value))
            print('Optimal Below: ' + str(2 * value))
        else:
            print(f"File {file_name} does not exist.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Arguments to execute the fully-polynomial approximation of Knapsack Problem.")
    parser.add_argument('--file', help='Location of file to analyze')
    parser.add_argument('--output', help="Location to output files. Output will have the same name as input.")
    parser.add_argument('--submission', help='Flag to run approximation on all data files expected. Note that this will NOT calculate errors. Set as True if you want to run.', default=False)
    args = parser.parse_args()
    if args.submission:
        print("Now executing all trials.")
    t_start = time()
    value = approximation(args.file, args.output)
    end = time() - t_start
    print('Took: ' + str(end))
    print('Final Value: ' + str(value))
    print('Optimal Below: ' + str(2 * value))