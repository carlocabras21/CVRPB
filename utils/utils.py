from scipy.spatial import distance

def compute_distance(i, j):
    return distance.euclidean([i.x, i.y], [j.x, j.y])
