import math
from unittest import TestCase

import graph
import parser
import pathfinder


class PathfinderTests(TestCase):
    def test_parse(self):
        # Act
        parser.parse_data('test_data/test_K_4_data.csv')

        # Assert
        self.assertEqual(len(graph.graph.keys()), 4)
        self.assertEqual(len(graph.vertices), 4)
        self.assertEqual(len(graph.routes_from(1)), 3)
        self.assertEqual(len(graph.routes_from(2)), 3)
        self.assertEqual(len(graph.routes_from(3)), 3)
        self.assertEqual(len(graph.routes_from(4)), 3)

    def test_cheapest_and_fastest(self):
        # Arrange
        parser.parse_data('test_data/test_simple_data.csv')

        # Act
        cheapest = pathfinder.find_cheapest()
        fastest = pathfinder.find_fastest()

        # Assert
        self.assertEqual(len(cheapest), 1)
        self.assertEqual(len(cheapest[0].stations), 3)
        self.assertEqual(cheapest[0].stations, {10: None, 11: 1, 12: 3})

        self.assertEqual(len(fastest), 1)
        self.assertEqual(len(fastest[0].stations), 3)
        self.assertEqual(fastest[0].stations, {10: None, 11: 2, 12: 4})

    def test_complete_graph(self):
        # Arrange
        parser.parse_data('test_data/test_K_4_data.csv')

        # Act
        cheapest = pathfinder.find_cheapest()
        fastest = pathfinder.find_fastest()

        # Assert
        self.assertEqual(len(cheapest), math.factorial(len(graph.vertices)))
        self.assertEqual(len(fastest), math.factorial(len(graph.vertices)))

    def test_duplicate_trains(self):
        # Arrange
        parser.parse_data('test_data/test_duplicate_trains_data.csv')

        # Act
        cheapest = pathfinder.find_cheapest()
        fastest = pathfinder.find_fastest()

        # Assert
        self.assertEqual(len(cheapest), 4)
        self.assertEqual(len(fastest), 4)

    def test_midnight_trains_time(self):
        # Arrange
        parser.parse_data('test_data/test_simple_data.csv')

        # Act
        fastest = pathfinder.find_fastest()

        # Assert
        self.assertEqual(fastest[0].duration, 7 * 3600 - 1)
        self.assertEqual(fastest[0].end_time, 6 * 3600)

    def test_neighbours(self):
        # Arrange
        parser.parse_data('test_data/test_simple_data_2.csv')
        expected_route_a = graph.Route(11, 1, 500, 23 * 3600, 3600)
        expected_route_b = graph.Route(11, 1, 1000, 23 * 3600 + 1, 3600)

        # Act
        cheap_route = pathfinder.find_cheapest_between_neighbours(10, 11, 1)
        fast_route_a = pathfinder.find_fastest_between_neighbours(10, 11, 1, 23 * 3600)
        fast_route_b = pathfinder.find_fastest_between_neighbours(10, 11, 1, 23 * 3600 + 1)

        # Assert
        self.assertEqual(cheap_route, expected_route_a)
        self.assertEqual(fast_route_a, expected_route_a)
        self.assertEqual(fast_route_b, expected_route_b)

