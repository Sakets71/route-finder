
import heapq
from math import inf


def dijkstra(graph, start, destination):
    """
    Find the minimum-distance route using Dijkstra's algorithm.

    Returns a dictionary containing:
        path: list of locations
        total_distance: shortest distance in kilometres
        road_segments: number of roads in the path

    Raises:
        ValueError if the start or destination is invalid.

    Returns None if the destination is unreachable.
    """

    if start not in graph:
        raise ValueError(f"Invalid starting location: {start}")

    if destination not in graph:
        raise ValueError(f"Invalid destination: {destination}")

    distances = {location: inf for location in graph}
    distances[start] = 0

    predecessor = {start: None}
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current = heapq.heappop(priority_queue)

        # Ignore outdated queue entries
        if current_distance > distances[current]:
            continue

        # The shortest distance to the destination is finalized
        if current == destination:
            break

        for neighbour, road_distance in graph[current].items():
            new_distance = current_distance + road_distance

            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                predecessor[neighbour] = current

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbour)
                )

    # Destination is unreachable
    if distances[destination] == inf:
        return None

    # Reconstruct the shortest path
    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = predecessor[current]

    path.reverse()

    return {
        "path": path,
        "total_distance": distances[destination],
        "road_segments": len(path) - 1,
    }


if __name__ == "__main__":
    from graph import load_city_map

    city_graph = load_city_map()
    result = dijkstra(city_graph, "College", "Hospital")

    if result:
        print("Shortest Route:", " -> ".join(result["path"]))
        print("Road segments:", result["road_segments"])
        print("Total distance:", result["total_distance"], "km")
    else:
        print("No route found.")
