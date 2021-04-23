import os
import time
import re
import sys
import csv
import datetime


# traverse root directory, and list directories as dirs and files as files
fieldnames = ['benchmark_name', 'status', 'correct', 'execution_time_seconds']
dictList = list()



for root, dirs, files in os.walk("output"):
    path = root.split(os.sep)
    fullpath = "/".join(path)
    for file in files:
        pathToFile = fullpath + '/' + file
        splitted = file.split(".")
        if splitted[len(splitted)-1] == "log":
            print ("looking at: " + "/".join(path) + "/" + file)
            reader = open(pathToFile, "r")
            DynamiteOutput = reader.read()

            result = DynamiteOutput.find("TNT result:")

            d = dict()
            d['benchmark_name'] = path[len(path)-1] + '/' + ".".join(splitted[:2])

            if(result < 0 ):
                d['status'] = 'timeout'
                d['correct'] = 'no'
                d['execution_time_seconds'] = '-'
            else:
                relevantOutput = DynamiteOutput[result:]
                split_relevant = relevantOutput.split("\n")

                status = ''
                correct = ''

                if 'True' in split_relevant[0]:
                    status = 'True'
                    correct = 'yes' if path[len(path) -1] == 'termination' else 'no'
                elif 'False' in split_relevant[0]:
                    status = 'False'
                    correct = 'yes' if path[len(path) -1] == 'nontermination' else 'no'
                else:
                    status = 'None'
                    correct = 'no'

                d['status'] = status
                d['correct'] = correct

                timeTaken = 0

                for log in split_relevant[2:]:
                    if(len(log) > 0):
                        log_decomp = log.split(' ')
                        # print(log_decomp)
                        time_s = log_decomp[1]
                        time = float(time_s[:len(time_s)-1])
                        timeTaken += round(time, 3)

                d['execution_time_seconds'] = timeTaken

            print(d)
            dictList.append(d)


with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for d in dictList:
        writer.writerow(d)


