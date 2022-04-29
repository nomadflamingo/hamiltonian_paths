import copy
import datetime
from dataclasses import field, dataclass
from queue import PriorityQueue
import graph
import utils

best_prices = PriorityQueue()
best_times = PriorityQueue()


@dataclass(order=True)
class PathWithPrice:
    """Data about the vertex stored in best_prices queue"""
    price: int
    last_station: int
    # Dictionaries are used here instead of sets, because dictionaries are ordered by insertion
    stations: dict = field(compare=False)


@dataclass(order=True)
class PathWithDuration:
    """Data about the vertex stored in best_prices queue"""
    duration: int
    last_station: int
    end_time: int
    # Dictionaries are used here instead of sets, because dictionaries are ordered by insertion
    stations: dict = field(compare=False)


def copy_path(path):
    new_path = copy.copy(path)
    new_path.stations = path.stations.copy()
    return new_path


def find_cheapest_between_neighbours(start: int, end: int, train: int):
    routes_between = PriorityQueue()

    # Iterate through all routes that go from start
    for route in graph.routes_from(start):
        if route.end == end and route.train == train:  # If route leads to the correct station
            routes_between.put((route.price, route))

    if routes_between.empty():
        raise ValueError(f'No routes between {start} and {end}')

    cheapest_price, cheapest_route = routes_between.get()

    return cheapest_route


def find_fastest_between_neighbours(start: int, end: int, train: int, from_time):
    routes_between = PriorityQueue()

    # Iterate through all routes that go from start
    for route in graph.routes_from(start):
        if route.end == end and route.train == train:  # If route leads to the correct station
            waiting_time = 0 if from_time is None else utils.subtract_dates_in_seconds(route.departure_time, from_time)
            trip_duration = graph.duration(route)
            routes_between.put((waiting_time + trip_duration, route))

    if routes_between.empty():
        raise ValueError(f'No routes between {start} and {end}')

    fastest_time, fastest_route = routes_between.get()

    return fastest_route


def reconstruct_path(path):
    stations = list(path.stations.keys())
    routes = []
    if isinstance(path, PathWithPrice):
        for i in range(len(stations) - 1):
            start = stations[i]
            end = stations[i + 1]
            train = path.stations[end]
            routes.append(find_cheapest_between_neighbours(start, end, train))
    elif isinstance(path, PathWithDuration):
        for i in range(len(stations) - 1):
            start = stations[i]
            end = stations[i + 1]
            train = path.stations[end]
            from_time = None if len(routes) == 0 else routes[-1].arrival_time
            routes.append(find_fastest_between_neighbours(start, end, train, from_time))
    start = stations[0]
    print('Route info:')
    for route in routes:
        print(f'{start} -> {route.end}'
              f'  train: {route.train}'
              f'  leaves at: {datetime.timedelta(seconds=route.departure_time)}'
              f'  arrives at: {datetime.timedelta(seconds=route.arrival_time)}'
              f'  price: {route.price/100}')
        start = route.end
    if isinstance(path, PathWithPrice):
        print(f'Total price: {path.price/100}\n')
    elif isinstance(path, PathWithDuration):
        print(f'Total duration: {datetime.timedelta(seconds=path.duration)}\n')


def find_cheapest():
    cheapest_paths = []
    cheapest_so_far = None
    while not best_prices.empty():
        path = best_prices.get()

        # If all the remaining paths are more expensive than the one we've found, break
        if len(cheapest_paths) != 0:
            if path.price > cheapest_paths[0].price:
                break

        # If all stations have been visited, add path to the result
        if len(path.stations.keys()) == len(graph.vertices):
            cheapest_paths.append(path)
            continue

        # Get the last station and iterate through all its routes
        last_station = path.last_station
        for route in graph.routes_from(last_station):
            next_station = route.end

            # If the station that the connection leads to has already been visited, skip this connection
            if next_station in path.stations:
                continue

            # Copy path so that it is unique and not shared between all last_station connections
            new_path = copy_path(path)

            # Update the new path
            new_path.stations[next_station] = route.train
            new_path.last_station = next_station
            new_path.price = new_path.price + route.price

            # Don't put new complete path to queue if it is more expensive than
            # the cheapest complete path that we've found
            if len(new_path.stations.keys()) == len(graph.vertices):
                if cheapest_so_far is None:
                    cheapest_so_far = new_path.price
                else:
                    if new_path.price > cheapest_so_far:
                        break
                    else:
                        cheapest_so_far = new_path.price

            # Put updated path in a queue
            best_prices.put(new_path)
    return cheapest_paths


def find_fastest():
    fastest_paths = []
    fastest_so_far = None
    while not best_times.empty():
        path = best_times.get()

        # If all the remaining paths are longer than the one we've found, break
        if len(fastest_paths) != 0:
            if path.duration > fastest_paths[0].duration:
                break

        # If all stations have been visited, add path to the result
        if len(path.stations.keys()) == len(graph.vertices):
            fastest_paths.append(path)
            continue

        # Get the last station and iterate through all its routes
        last_station = path.last_station
        for route in graph.routes_from(last_station):
            next_station = route.end

            # If the station that the connection leads to has already been visited, skip this connection
            if next_station in path.stations:
                continue

            # Copy path so that it is unique and not shared between all last_station connections
            new_path = copy_path(path)

            # Update the stations in path
            new_path.stations[next_station] = route.train
            new_path.last_station = next_station

            # Set new path duration time
            waiting_time = utils.subtract_dates_in_seconds(route.departure_time, new_path.end_time)
            trip_duration = graph.duration(route)
            new_path.end_time = route.arrival_time
            new_path.duration = new_path.duration + waiting_time + trip_duration

            # Don't put new complete path to queue if it is longer than
            # the fastest complete path that we've found
            if len(new_path.stations.keys()) == len(graph.vertices):
                if fastest_so_far is None:
                    fastest_so_far = new_path.duration
                else:
                    if new_path.duration > fastest_so_far:
                        break
                    else:
                        fastest_so_far = new_path.duration

            # Put updated path in a queue
            best_times.put(new_path)
    return fastest_paths
