import unittest

from mockito import *
from utils.algorithm import *

class TestKMeans(unittest.TestCase) :

    def test_k_clusters_created(self) :
        values = [5, 8, 10]
        k = 3

        factory = mock()

        algo = KMeans(values, k, (lambda x, y: x - y), factory)
        self.assertEquals(len(algo.clusters), 3)

    def test_test_distance(self) :
        values = [5, 8, 10]
        k = 3

        factory = mock()

        x = 2
        center1 = 5
        center2 = 8
        center3 = 10
        cluster1 = mock()
        cluster2 = mock()
        cluster3 = mock()

        when(cluster1).getCenter().thenReturn(center1)
        when(cluster2).getCenter().thenReturn(center2)
        when(cluster3).getCenter().thenReturn(center3)

        when(factory).createCluster(center1).thenReturn(cluster1)
        when(factory).createCluster(center2).thenReturn(cluster2)
        when(factory).createCluster(center3).thenReturn(cluster3)

        algo = KMeans(values, k, (lambda x, y: x - y), factory)
        algo.choose_cluster(x)

        verify(cluster1).addValue(x)
        verify(cluster2, never).addValue(x)
        verify(cluster3, never).addValue(x)
