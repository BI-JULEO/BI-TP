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

    def init_clusters(self, k) :
        print "Initilalization of", k, "clusters..."
        centers = random.sample(self.values, k)
        for center in centers :
            cluster = self.factory.create_cluster(center)
            self.clusters.append(cluster)

    def choose_cluster(self, value) :
        min = sys.maxint
        choice = None
        for cluster in self.clusters :
            center = cluster.get_center()
            dist = self.distance(center, value)
            if dist < min :
                min = dist
                choice = cluster

        choice.add_value(value)

        print "Removing", value, "from others clusters..."
        for cluster in filter((lambda x: x != choice), self.clusters) :
            cluster.remove_if_present(value)

    def distribute_values(self) :
        self.init_clusters(self.k)
        while True :
            for value in self.values :
                self.choose_cluster(value)
            states = map((lambda x: x.has_changed()), self.clusters)
            if not any(states) :
                break
            for cluster in self.clusters :
                cluster.update_center()
        print "Finished!"
        print ""

class Cluster(object) :

    def __init__(self, center) :
        self.center = center
        self.values = []
        self.changed = False
        self.add_value(center)

    def add_value(self, value) :
        if self.values.count(value) == 0 :
            self.values.append(value)
            self.changed = True
    
    def remove_if_present(self, value) :
        if value == self.center :
            raise CannotRemoveTheCenterError()

        try :
            self.changed = True
            self.values.remove(value)
        except ValueError :
            pass

    def get_center(self) :
        return self.center

    def update_center(self) :
        self.changed = False
        self.center = sum(self.values)/len(self.values)

    def has_changed(self) :
        return self.changed

class CannotRemoveTheCenterError(Exception) :
    pass
