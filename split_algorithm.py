import numpy as np
import math
from kneed import KneeLocator
import matplotlib.pyplot as plt

def get_splits(arr, split_num):
    sub_arr_num = split_num - 1
    arr = np.array(arr)

    dist_matrix = np.linalg.norm(arr[:, np.newaxis] - arr, axis=2)

    # cost is a dp array. dp[k][i] = minimum cost in each subarray by split arr[0....i] into k subarray
    cost = [[float('inf') for i in range(len(arr))] for j in range(sub_arr_num + 1)]
    # splits is used to back trace
    splits = [[0 for i in range(len(arr))] for j in range(sub_arr_num + 1)]

    # print(dist_matrix)
    # print(cost)
    # init cost
    for i in range(len(arr)):
        # print(i)
        cost[0][i] = np.sum(dist_matrix[0:i+1, 0:i+1])

    for k in range(1, sub_arr_num + 1):
        print("Computing splits for using %d scenes" %(k))
        for i in range(len(arr)):
            for j in range(i):
                new_cost = cost[k-1][j] + np.sum(dist_matrix[j+1:i+1, j+1:i+1])
                if new_cost < cost[k][i]:
                    cost[k][i] = new_cost
                    splits[k][i] = j + 1

    # get the last element of each array in cost
    errors = [subarr[-1] for subarr in cost]
    indices = range(len(errors))

    kl = KneeLocator(indices, errors, curve='convex', direction='decreasing')

    elbow_point = int(kl.elbow)

    print(f"Optimal number of clusters based on elbow method: %s" %(elbow_point))

    # plt.plot(indices, errors)
    # plt.xlabel('Index')
    # plt.ylabel('Number')
    # plt.title('List of Numbers:')
    # plt.show()

    # backtrack
    i = len(arr) - 1
    split_points = []
    for k in range(elbow_point, 0, -1):
        split_points.append(splits[k][i])
        i = splits[k][i] - 1
    split_points.reverse()
    return (split_points, cost[-1][-1])

# a = [[1, 2, 3], [1, 1, 1], [5, 6, 7], [5,7, 8], [2, 1, 1], [1, 1, 1], [2, 2, 1],[100, 100, 1], [100, 100, 0], [100, 100, 1]]
# print(get_splits(a,7))

