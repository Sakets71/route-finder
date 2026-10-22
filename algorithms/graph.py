
import json
from pathlib import Path


def load_city_map():
    file_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "city_map.json"
    )

    with file_path.open("r", encoding="utf-8") as file:
        city_map = json.load(file)

    locations = city_map["locations"]
    roads = city_map["roads"]

    if len(locations) != len(set(locations)):
        raise ValueError("Duplicate locations found.")

    graph = {location: {} for location in locations}
    seen_roads = set()

    for road in roads:
        source = road["from"]
        destination = road["to"]
        distance = road["distance"]

        if source not in graph or destination not in graph:
            raise ValueError(
                f"Unknown location in road: {source} -> {destination}"
            )

        if source == destination:
            raise ValueError("A road cannot connect a location to itself.")

        if isinstance(distance, bool) or not isinstance(
            distance, (int, float)
        ) or distance <= 0:
            raise ValueError(
                f"Invalid distance for {source} -> {destination}"
            )

        road_key = frozenset((source, destination))

        if road_key in seen_roads:
            raise ValueError(
                f"Duplicate road found: {source} <-> {destination}"
            )

        seen_roads.add(road_key)

        graph[source][destination] = distance
        graph[destination][source] = distance

    validate_graph(graph)
    return graph


def validate_graph(graph):
    for location, neighbours in graph.items():
        for neighbour, distance in neighbours.items():
            if neighbour not in graph:
                raise ValueError(
                    f"Unknown connected location: {neighbour}"
                )

            if not isinstance(distance, (int, float)) or isinstance(
                distance, bool
            ) or distance <= 0:
                raise ValueError(
                    f"Invalid road distance: {location} -> {neighbour}"
                )

            reverse_distance = graph[neighbour].get(location)

            if reverse_distance != distance:
                raise ValueError(
                    f"Road is not two-way: {location} <-> {neighbour}"
                )


if __name__ == "__main__":
    graph = load_city_map()

    print("City graph loaded successfully!")
    print("Total locations:", len(graph))

    for location, neighbours in graph.items():
        print(f"{location}: {neighbours}")
