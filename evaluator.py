import sys
import json
from termcolor import colored
import numpy
from math import *
from functions import *

#Parameters
path = sys.argv[1]
pathTruth = sys.argv[2]
Tmatch = 50
convCoef = 110466

#Input
segments = []
intersections= []
with open(path) as resultGeojson:
    for jsonSegment in json.load(resultGeojson)['features'] :
        if jsonSegment['geometry']['type'] == "Point" :
            intersections.append(jsonSegment['geometry']['coordinates'])
        elif jsonSegment['geometry']['type'] == "LineString" :
            segments.append(jsonSegment['geometry']['coordinates'])

segmentsTruth = []
intersectionsTruth = []
with open(pathTruth) as TruthGeojson:
    for jsonSegment in json.load(TruthGeojson)['features'] :
        if jsonSegment['geometry']['type'] == "Point" :
            intersectionsTruth.append(jsonSegment['geometry']['coordinates'])
        elif jsonSegment['geometry']['type'] == "LineString" :
            segmentsTruth.append(jsonSegment['geometry']['coordinates'])


##Intersections evaluation

#Return an map dictionnary with the following constitution :
# - Key : Intersection Truth point 
# - Value 1 : Closest Computed intersection point
# - Value 2 : Distance between Truth and Computed intersections.
mapping = {}
for intersection in intersections :
    distances = [sqrt((iT[0] - intersection[0])**2 + (iT[1] - intersection[1])**2) for iT in intersectionsTruth]
    distance = min(distances)
    intersectionTruth = intersectionsTruth[distances.index(distance)]
    if distance * convCoef < Tmatch and ((intersectionTruth[0], intersectionTruth[1]) not in mapping or mapping[(intersectionTruth[0], intersectionTruth[1])][1] >= distance) :
        mapping[(intersectionTruth[0], intersectionTruth[1])] = (intersection, distance)

#Compute the next respective four value : 
# - Intersections that have been matched
# - Intersections that have not been matched
# - Intersections Truth that have been matched
# - Intersections Truth that have not been matched
TP = [value[0] for value in mapping.values()]
FP = [i for i in intersections if i not in TP]
TN = [key for key in mapping.keys()]
FN = [it for it in intersectionsTruth if (it[0], it[1]) not in TN]

#Compute the 4 metrics
precision = numpy.around(len(TN) / len(intersections) * 100, 2)
recall = numpy.around(len(TN) / len(intersectionsTruth)  * 100, 2)
fscore = numpy.around((2 * recall * precision) / (recall + precision), 2)
accuracy = numpy.around(numpy.average([elem[1] for elem in mapping.values()]) * convCoef, 2)
print(colored("###Intersection evaluation###", "magenta"))
print(colored("Acceptation Distance = " + str(Tmatch) + "m", "green"))
print("Precision = ", precision, "%")
print("Recall = ", recall, "%")
print("FScore = ", fscore, "%")
print("Accuracy = ", accuracy, "m")
print()

##Segment evaluation

#Return an map dictionnary with the following constitution :
# - Key : Segment Truth 
# - Value : Distance with its closest computed segment
mapping = {}
for segmentId in range(0, len(segments)) :
    closetSegmentTruthDistance = ()
    for segmentTruthId in range(0, len(segmentsTruth)) :
        distance = numpy.average([shortestDistancePntSeg(point, segmentsTruth[segmentTruthId]) for point in segments[segmentId]])
        if closetSegmentTruthDistance == () or closetSegmentTruthDistance[1] >= distance :
            closetSegmentTruthDistance = (segmentTruthId, distance)   
    mapping[closetSegmentTruthDistance[0]] = closetSegmentTruthDistance[1]

#Compute the next respective four value : 
# - Segments Truth that have been matched ids
# - Segments Truth that have not been matched ids      
TN = [key for key in mapping.keys()]
FN = [segmentsTruth.index(segmentTruth) for segmentTruth in segmentsTruth if segmentsTruth.index(segmentTruth) not in TN]

#For each computed and truth network do the following steps :
# - Compute the adjacency matrix
# - Compute the floyd matrix
# - Compute the non diagonal average
avgc = averageOfNonDiagElem(floyd(adjacency_matrix(segments)))
avgt = averageOfNonDiagElem(floyd(adjacency_matrix(segmentsTruth)))

#Compute the 6 metrics
precision = numpy.around(len(TN) / len(segments) * 100, 2)
recall = numpy.around(len(TN) / len(segmentsTruth) * 100, 2)
fscore = numpy.around((2 * recall * precision) / (recall + precision), 2)
accuracy = numpy.around(numpy.average([distance for distance in mapping.values()]) * convCoef, 2)
std = numpy.around(numpy.std([distance for distance in mapping.values()]) * convCoef, 2)
correctness = numpy.around(avgt / avgc, 2) * 100

print(colored("###Segment evalution###", "magenta"))
print("Precision = ", precision, "%")
print("Recall = ", recall, "%")
print("FScore = ", fscore, "%")
print("Accuracy = ", accuracy, "m")
print("Standard deviation = ", std, "m")
print("Correctness = ", correctness, "%")

# resultfile = open("results.txt","a")
# resultfile.write(path + ' ' + pathTruth + ' ' + str(Tmatch) + ' ' + str(precision) + ' ' + str(recall) + ' ' + str(fscore) + ' ' + str(completeness) + ' ' + str(precision) + ' ' + str(std) + ' ' + str(correctness) + '\n') 
# resultfile.close()