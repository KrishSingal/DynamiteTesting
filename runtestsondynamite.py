import os
import time
import re
import sys
import csv
import datetime

# os.system("./buildCLITool.sh")
os.system("mkdir output")

# traverse root directory, and list directories as dirs and files as files
fieldnames = ['benchmark_name', 'status', 'execution_time_seconds']
dictList = list()

timeLimit = 300

if len(sys.argv) == 2:
    timeLimit = int(sys.argv[1])

print ("timeLimit: " + str(timeLimit))

for root, dirs, files in os.walk("benchmarks/ultimate/benchmarks/regressions"):
    path = root.split(os.sep)
    pathToFile = "/".join(path[1:])
    fullpath = "output/" + pathToFile
    os.system("mkdir -p " + fullpath)
    for file in files:
        splitted = file.split(".")
        if splitted[len(splitted)-1] == "c":
        # if splitted[len(splitted)-1] == "c" or splitted[len(splitted)-1] == "java":
            outputfilepath = fullpath + "/" + file + ".log"
            print ("running: " + "/".join(path) + "/" + file)
            start = datetime.datetime.now()
            os.system("timeout " + str(timeLimit) + " python3 src/dynamo.py " + "/".join(path) + "/" + file + " >> " + outputfilepath)
            end = datetime.datetime.now()
            time_diff = (end - start)
            timeTaken = round(time_diff.total_seconds(), 3)
            d = dict()
            d['benchmark_name'] = fullpath + "/" + file
            d['execution_time_seconds'] = str(timeTaken)
            if timeTaken >= timeLimit:
                d['status'] = 'timeout'
            else:
                d['status'] = 'pass'
            print(d)

            '''
            f = open(outputfilepath, 'r')
            all_of_it = f.read()
            f.close()
            verifiedPattern = "Verified in \d+ iterations"
            verifiedPatternSearch = re.search(verifiedPattern, all_of_it)
            if verifiedPatternSearch is not None:
                theMatch = verifiedPatternSearch.group(0)
                theMatchSplitted = theMatch.split(" ")
                d['status'] = 'verified'
                d['num_refinements'] = theMatchSplitted[2]
                print (d)
                dictList.append(d)
                continue

            counterExamplePattern = "Counterexample found in \d+ iterations"
            counterExamplePatternSearch = re.search(counterExamplePattern, all_of_it)
            if counterExamplePatternSearch is not None:
                theMatch = counterExamplePatternSearch.group(0)
                theMatchSplitted = theMatch.split(" ")
                d['status'] = "counterexample"
                d['num_refinements'] = theMatchSplitted[3]
                print (d)
                dictList.append(d)
                continue

            refinementPattern = "====== Refinement \d+ ======"
            refinementMatches = re.findall(refinementPattern, all_of_it, re.DOTALL)
            numRefinements = 0
            if len(refinementMatches) > 0:
                lastRefinement = refinementMatches[len(refinementMatches)-1]
                lastRefinementSplitted = lastRefinement.split(" ")
                numRefinements = int(lastRefinementSplitted[2])
                d['num_refinements'] = numRefinements

            # echo $? didn't work

            if timeTaken >= timeLimit:
                d['status'] = 'timeout'
            else:
                d['status'] = 'error'

            print(d)
            dictList.append(d)


with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for d in dictList:
        writer.writerow(d)

            '''

