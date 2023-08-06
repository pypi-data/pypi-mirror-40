# -*- coding: utf-8 -*-

import unittest
from .context import ROOT_FOLDER
from safe import safe
import os
import pandas as p


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_0_absolute_truth_and_meaning(self):
        assert True

    def test_1_safe_single_gene(self):
        network = os.path.join(ROOT_FOLDER, 'resources/datasets/costanzo_2016/safe_layout.csv')
        neighbors = os.path.join(ROOT_FOLDER, 'resources/datasets/costanzo_2016/safe_neighbors.csv')
        attributes = p.DataFrame([[1]], index=[4545], columns=['test'])

        s = safe.Safe(network, attributes, neighbors)
        s.prepare_attributes()

        enrichments = s.calculate()
        enrichments = enrichments.loc[enrichments.any(axis=1)]

        assert enrichments.shape[0] == 0

    def test_2_safe_one_gene_from_each_cluster(self):
        network = os.path.join(ROOT_FOLDER, 'resources/datasets/costanzo_2016/safe_layout.csv')
        neighbors = os.path.join(ROOT_FOLDER, 'resources/datasets/costanzo_2016/safe_neighbors.csv')
        attributes = p.DataFrame([[1]],
                                 index=[4545, 5649, 5482, 1223, 4441, 1898, 5709, 386, 848, 962, 3662, 4643, 834],
                                 columns=['test'])

        s = safe.Safe(network, attributes, neighbors)
        s.prepare_attributes()

        enrichments = s.calculate()
        enrichments = enrichments.loc[enrichments.any(axis=1)]

        fig = s.plot()
        fig.savefig('test2.png', bbox_inches='tight', facecolor='black')

        print("TEST2", enrichments.shape)

    def test_3_safe_one_cluster_enriched(self):
        network = os.path.join(ROOT_FOLDER, 'resources/datasets/costanzo_2016/safe_layout.csv')
        neighbors = os.path.join(ROOT_FOLDER, 'resources/datasets/costanzo_2016/safe_neighbors.csv')
        attributes = p.DataFrame([[1]],
                                 index=[2028, 4584, 1810, 2602, 4639, 283, 3855, 2595, 5872, 4348, 654, 5208, 5644,
                                        1572, 3415],
                                 columns=['test'])

        s = safe.Safe(network, attributes, neighbors)
        s.prepare_attributes()

        enrichments = s.calculate()
        enrichments = enrichments.loc[enrichments.any(axis=1)]

        fig = s.plot()
        fig.savefig('test3.png', bbox_inches='tight', facecolor='black')

        print("TEST3", enrichments.shape)

    def test_4_safe_two_clusters_enriched(self):
        network = os.path.join(ROOT_FOLDER, 'resources/datasets/costanzo_2016/safe_layout.csv')
        neighbors = os.path.join(ROOT_FOLDER, 'resources/datasets/costanzo_2016/safe_neighbors.csv')
        attributes = p.DataFrame([[1]],
                                 index=[2087, 1005, 3922, 4933, 4782, 2081, 1328, 1861, 3685, 2195, 4136, 3806, 4968,
                                        4362, 3874, 6044, 386, 1371, 163, 985],
                                 columns=['test'])

        s = safe.Safe(network, attributes, neighbors)
        s.prepare_attributes()

        enrichments = s.calculate()
        enrichments = enrichments.loc[enrichments.any(axis=1)]

        fig = s.plot()
        fig.savefig('test4.png', bbox_inches='tight', facecolor='black')

        print("TEST4", enrichments.shape)


if __name__ == '__main__':
    unittest.main()
