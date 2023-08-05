from __future__ import print_function

import os
import unittest

from data import RelationFactory, BP


class Tests(unittest.TestCase):

    def test_arff(self):
        """Test if all is good if we have a valid arff.
        """
        expected_classes = {'5', '11', '12', '8', '20', '14', '16', '18', '7', '13', '4', '10', '19', '15', '9'}
        expected_active_classes = {'5', '11', '12', '8', '20', '14', '16', '18', '7', '13', '4', '10', '19', '15', '9'}
        expected_field_names = ["'Length'", "'Diameter'", "'Height'", "'Class_Rings'"]
        expected_datasets = [[0.455, 0.365, 0.095, '15'], [0.35, 0.265, 0.09, '7'], [0.53, 0.42, 0.135, '9'], [0.44, 0.365, 0.125, '10'], [0.33, 0.255, 0.08, '7'], [0.425, 0.3, 0.095, '8'], [0.53, 0.415, 0.15, '20'], [0.545, 0.425, 0.125, '16'], [0.475, 0.37, 0.125, '9'], [0.55, 0.44, 0.15, '19'], [0.525, 0.38, 0.14, '14'], [0.43, 0.35, 0.11, '10'], [0.49, 0.38, 0.135, '11'], [0.535, 0.405, 0.145, '10'], [0.47, 0.355, 0.1, '10'], [0.5, 0.4, 0.13, '12'], [0.355, 0.28, 0.085, '7'], [0.44, 0.34, 0.1, '10'], [0.365, 0.295, 0.08, '7'], [0.45, 0.32, 0.1, '9'], [0.355, 0.28, 0.095, '11'], [0.38, 0.275, 0.1, '10'], [0.565, 0.44, 0.155, '12'], [0.55, 0.415, 0.135, '9'], [0.615, 0.48, 0.165, '10'], [0.56, 0.44, 0.14, '11'], [0.58, 0.45, 0.185, '11'], [0.59, 0.445, 0.14, '12'], [0.605, 0.475, 0.18, '15'], [0.575, 0.425, 0.14, '11'], [0.58, 0.47, 0.165, '10'], [0.68, 0.56, 0.165, '15'], [0.665, 0.525, 0.165, '18'], [0.68, 0.55, 0.175, '19'], [0.705, 0.55, 0.2, '13'], [0.465, 0.355, 0.105, '8'], [0.54, 0.475, 0.155, '16'], [0.45, 0.355, 0.105, '8'], [0.575, 0.445, 0.135, '11'], [0.355, 0.29, 0.09, '9'], [0.45, 0.335, 0.105, '9'], [0.55, 0.425, 0.135, '14'], [0.24, 0.175, 0.045, '5'], [0.205, 0.15, 0.055, '5'], [0.21, 0.15, 0.05, '4'], [0.39, 0.295, 0.095, '7'], [0.47, 0.37, 0.12, '9']]
        
        data = RelationFactory.loadFromFile(os.path.join(BP, 'fixtures/abalone-train.arff'))
        
        self.assertEqual(data.relName, "'abalone'")
        self.assertEqual(data.allClasses, expected_classes)
        self.assertEqual(data.activeClasses, expected_active_classes)
        self.assertEqual(data.numDatasets, 47)
        self.assertEqual(data.fieldNames, expected_field_names)
        self.assertEqual(data.datasets, expected_datasets)
