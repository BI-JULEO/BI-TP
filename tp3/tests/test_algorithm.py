import unittest

from mockito import *
from utils.algorithm import *

class TestKMeans(unittest.TestCase) :

    def test_k_clusters_created(self) :
        values = [5, 8, 10]
        k = 3

        factory = mock()

        algo = KMeans(values, k, (lambda x, y: x - y), factory)
        algo.init_clusters(k)

        self.assertEquals(len(algo.clusters), 3)

    def test_test_distance(self) :
        values = [5, 8, 10]
        k = 3

        x = 2
        center1 = 5
        center2 = 8
        center3 = 10
        cluster1 = mock()
        cluster2 = mock()
        cluster3 = mock()

        when(cluster1).get_center().thenReturn(center1)
        when(cluster2).get_center().thenReturn(center2)
        when(cluster3).get_center().thenReturn(center3)

        factory = mock()
        when(factory).create_cluster(center1).thenReturn(cluster1)
        when(factory).create_cluster(center2).thenReturn(cluster2)
        when(factory).create_cluster(center3).thenReturn(cluster3)

        algo = KMeans(values, k, (lambda x, y: x - y), factory)
        algo.init_clusters(k)
        algo.choose_cluster(x)

        verify(cluster1).add_value(x)
        verify(cluster1, never).remove_if_present(x)
        verify(cluster2, never).add_value(x)
        verify(cluster2).remove_if_present(x)
        verify(cluster3, never).add_value(x)
        verify(cluster3).remove_if_present(x)

    def test_stop_iteration(self) :
        values = [5, 8, 10]
        k = 3

        center1 = 5
        center2 = 8
        center3 = 10
        cluster1 = mock()
        cluster2 = mock()
        cluster3 = mock()

        when(cluster1).get_center().thenReturn(center1)
        when(cluster2).get_center().thenReturn(center2)
        when(cluster3).get_center().thenReturn(center3)
        when(cluster1).has_changed().thenReturn(False)
        when(cluster2).has_changed().thenReturn(False)
        when(cluster3).has_changed().thenReturn(False)

        factory = mock()
        when(factory).create_cluster(center1).thenReturn(cluster1)
        when(factory).create_cluster(center2).thenReturn(cluster2)
        when(factory).create_cluster(center3).thenReturn(cluster3)

        algo = KMeans(values, k, (lambda x, y: x - y), factory)
        algo.distribute_values()

        verify(cluster1, never).update_center()
        verify(cluster2, never).update_center()
        verify(cluster3, never).update_center()

    def test_continue_iteration_and_update_center(self) :
        values = [5, 8, 10]
        k = 3

        center1 = 5
        center2 = 8
        center3 = 10
        cluster1 = mock()
        cluster2 = mock()
        cluster3 = mock()

        when(cluster1).get_center().thenReturn(center1)
        when(cluster2).get_center().thenReturn(center2)
        when(cluster3).get_center().thenReturn(center3)
        when(cluster1).has_changed().thenReturn(True).thenReturn(False)
        when(cluster2).has_changed().thenReturn(False)
        when(cluster3).has_changed().thenReturn(False)

        factory = mock()
        when(factory).create_cluster(center1).thenReturn(cluster1)
        when(factory).create_cluster(center2).thenReturn(cluster2)
        when(factory).create_cluster(center3).thenReturn(cluster3)

        algo = KMeans(values, k, (lambda x, y: x - y), factory)
        algo.distribute_values()

        verify(cluster1).update_center()
        verify(cluster2).update_center()
        verify(cluster3).update_center()

class TestCluster(unittest.TestCase) :

    def test_ceation_add_the_center_in_values(self) :
        center = 4

        cluster = Cluster(center)
        
        self.assertEquals(len(cluster.values), 1)

    def test_add_value(self) :
        value = 5

        cluster = Cluster(2)
        cluster.add_value(value)

        self.assertEquals(len(cluster.values), 2)

    def test_add_value_duplicate_value(self) :
        value = 5

        cluster = Cluster(2)
        cluster.add_value(value)
        cluster.add_value(value)

        self.assertEquals(len(cluster.values), 2)
    
    def test_remove_if_present(self) :
        value = 5

        cluster = Cluster(2)
        cluster.add_value(value)
        cluster.remove_if_present(value)

        self.assertEquals(len(cluster.values), 1)

    def test_remove_if_present_not_raise_exception(self) :
        value = 5

        cluster = Cluster(2)
        try :
            cluster.remove_if_present(value)
        except ValueError :
            self.fail("Should not raise the exception ValueError")

    def test_remove_if_present_cant_remove_center(self) :
        value = 5

        cluster = Cluster(value)
        self.assertRaises(CannotRemoveTheCenterError, cluster.remove_if_present, value)

    def test_update_center(self) :
        center = 1.
        values = [3., 2., 4.]

        cluster = Cluster(center)
        for value in values :
            cluster.add_value(value)

        cluster.update_center()
        
        self.assertEquals(cluster.center, 2.5)

    def test_add_value_change_the_state(self) :
        value = 5

        cluster = Cluster(4)
        cluster.add_value(value)

        self.assertTrue(cluster.has_changed())

    def test_update_center_reset_state(self) :
        center = 1
        value = 5

        cluster = Cluster(center)
        cluster.add_value(value)
        cluster.update_center()

        self.assertFalse(cluster.has_changed())

    def test_remove_change_the_state(self) :
        value = 5

        cluster = Cluster(4)
        cluster.add_value(value)
        cluster.update_center()
        cluster.remove_if_present(value)

        self.assertTrue(cluster.has_changed())
