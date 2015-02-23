import sys
import random

"""
Module definissant des algorithmes de classification
"""

class KMeans(object) :
    """
    Algorithme du K-Means
    """

    def __init__(self, values, k, distance, factory=None) :
        """
        values : les entrees a traiter
        k : le nombre de clusters souhaite (k > 0)
        distance : la function de distance a utiliser
        """
        self.values = values
        self.k = k
        self.distance = distance
        self.factory = factory
        self.clusters = []
        self.init_clusters(k)

    def init_clusters(self, k) :
        centers = random.sample(self.values, k)
        for center in centers :
            print "Center choice:", center 
            cluster = self.factory.createCluster(center)
            self.clusters.append(cluster)

    def choose_cluster(self, value) :
        min = sys.maxint
        choice = None
        for cluster in self.clusters :
            center = cluster.getCenter()
            dist = self.distance(center, value)
            if dist < min :
                min = dist
                choice = cluster
        choice.addValue(value)
