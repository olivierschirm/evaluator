from math import *
import numpy

def shortestDistancePntSeg(pnt, seg) :
    distPnt = [sqrt((pt[0] - pnt[0])**2 + (pt[1] - pnt[1])**2) for pt in seg]
    minIndex = distPnt.index(min(distPnt))
    if minIndex == 0 :
        return shortestDistancePntLine(pnt, seg[0], seg[1])
    elif minIndex == len(seg) - 1 :
        return shortestDistancePntLine(pnt, seg[-1], seg[-2])
    else :
        first = shortestDistancePntLine(pnt, seg[minIndex - 1], seg[minIndex])
        second = shortestDistancePntLine(pnt, seg[minIndex], seg[minIndex + 1])
        return min([first, second])

def shortestDistancePntLine(pnt, start, end) :
    line_vec = (end[0] - start[0], end[1] - start[1]) 
    pnt_vec = (pnt[0] - start[0], pnt[1] - start[1]) 
    line_len = numpy.linalg.norm(line_vec)
    line_unitvec = line_vec / line_len
    pnt_vec_scaled = pnt_vec / line_len
    t = numpy.dot(line_unitvec, pnt_vec_scaled)    
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    nearest = numpy.array(line_vec).dot(t)
    dist = numpy.linalg.norm((pnt_vec[0] - nearest[0], pnt_vec[1] - nearest[1]))
    return dist

def adjacency_matrix(network) :
    nodes = []
    for segment in network :
        if segment[0] not in nodes : nodes.append(segment[0])
        if segment[-1] not in nodes : nodes.append(segment[-1])

    if len(nodes) < 1: return []

    adjacency_matrix = numpy.zeros(shape=(len(nodes),len(nodes)))
    for i in range(0, len(nodes)):
        for j in range(0, len(nodes)):
            if i == j : continue
            for segment in network :
                if (segment[0] == nodes[i] and segment[-1] == nodes[j]) or (segment[-1] == nodes[i] and segment[0] == nodes[j]) :
                    adjacency_matrix[i, j] = 1
                    break           
            if adjacency_matrix[i, j] == 0 : adjacency_matrix[i, j] = 999999           
    return adjacency_matrix

def floyd(A) :
    n = len(A)
    for k in range(0, n) :
        for i in range(0, n) :
            for j in range(0, n) :
                A[i, j] = min(A[i, j], A[i, k] + A[k, j])
    return A

def averageOfNonDiagElem(A) :
    elements = []
    n = len(A)
    for i in range(0, n) : 
        for j in range(0, n) : 
            if A[i, j] != 0 : elements.append(A[i, j])
    return numpy.average(elements)