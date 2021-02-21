import math
import pandas as pd

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

def complex(available):
    def find_matches(users, df):
        cluster_dict = dict()
        matches = []
        matchless = []

        for user in users:
            cluster_dict[user] = None

        for i, user in enumerate(users):
            if i == len(users) - 1:
                matchless.append(users[i])
    
            if cluster_dict[users[i]] == -1:
                continue

        cluster_dict[users[i]] = df.loc[df["User ID"] == users[i]].iloc[0][9]
        matched = False

        for potential_match in users[i+1:]:
            if cluster_dict[potential_match] == None:
                cluster_dict[potential_match] = df.loc[df["User ID"] == potential_match].iloc[0][9]
            
            if cluster_dict[users[i]] == cluster_dict[potential_match]:
                # print("users[i]:", users[i], "potential_match:", potential_match)
                # print("cluster_dict[users[i]]:", cluster_dict[users[i]], "cluster_dict[potential_match]:", cluster_dict[potential_match])
                matches.append((users[i], potential_match))
                cluster_dict[users[i]] = -1
                cluster_dict[potential_match] = -1
                matched = True
                break
    
        if not matched:
            matchless.append(users[i])

        for i in range(0, len(matchless), 2):
            if i + 1 < len(matchless):
                matches.append((matchless[i], matchless[i+1]))
            if i == len(matchless) - 1:
                matches.append((matchless[i], None))

        return matches
    return find_matches(available, pd.read_csv('/Users/niravadunuthula/Downloads/fake_data2.csv'))