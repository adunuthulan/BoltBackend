import math

def matchAPI(available):
    tmp = [(a, 1609) for a in available] #change to incorporate distance
    matches = list()
    visited = set()

    #Matches closest distance and picks lowest distance
    for i in range(len(tmp)):
        distDiff = -1
        for j in range(i, len(tmp)):
            if (distDiff == -1 or abs(tmp[i][1] - tmp[j][1]) < abs(tmp[i][1] - tmp[distDiff][1])) and i != j and j not in visited:
                distDiff = j

        if distDiff != -1:
            matches.append((tmp[i][0], tmp[distDiff][0], min(tmp[i][1], tmp[distDiff][1])))
            visited.add(i)
            visited.add(j)
    return matches
