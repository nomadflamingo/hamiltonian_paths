import csv
import graph
import pathfinder
import utils


def parse_data(file_name):
    with open(file_name, 'r') as file:
        csvreader = csv.reader(file, delimiter=';')
        for row in csvreader:
            # Convert values
            train = int(row[0])
            start = int(row[1])
            end = int(row[2])
            cents = utils.convert_to_cents(row[3])
            departure_time = utils.convert_to_seconds_from_midnight(row[4])
            arrival_time = utils.convert_to_seconds_from_midnight(row[5])
            duration = utils.subtract_dates_in_seconds(arrival_time, departure_time)

            # Add vertices to graph, if they are not added
            if start not in graph.vertices:
                graph.add_station(start)
            if end not in graph.vertices:
                graph.add_station(end)

            # Add route (edge)
            route = graph.Route(end, train, cents, departure_time, arrival_time)
            graph.add_route(start, route)

            # Update pathfinder queues
            pathfinder.best_prices.put(
                pathfinder.PathWithPrice(cents, end, {start: None, end: train}))
            pathfinder.best_times.put(
                pathfinder.PathWithDuration(duration, end, arrival_time, {start: None, end: train}))
