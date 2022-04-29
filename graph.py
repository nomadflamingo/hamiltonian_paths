from typing import NamedTuple

import utils

graph = dict()
vertices = set()


class Route(NamedTuple):
    end: int
    train: int
    price: int
    departure_time: int
    arrival_time: int


def add_station(v):
    if v in vertices:
        raise ValueError(f'Cannot add vertex {v} because it is already in a graph')
    vertices.add(v)
    graph[v] = []


def add_route(start: int, route: Route):
    if start not in vertices:
        raise ValueError(f'Cannot add route because start station {start} is not in a graph')
    if route.end not in vertices:
        raise ValueError(f'Cannot add route because end station {route.end} is not in a graph')

    graph[start].append(route)


def print_graph():
    for station in graph.keys():
        for route in graph[station]:
            print(station, "->", route.end,
                  " train:", route.train,
                  " price:", route.price,
                  " t1:", route.departure_time,
                  " t2:", route.arrival_time)


def routes_from(v):
    return graph[v]


def duration(route):
    t1 = route.departure_time
    t2 = route.arrival_time
    return utils.subtract_dates_in_seconds(t2, t1)
