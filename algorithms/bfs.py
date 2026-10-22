
from collections import deque


def bfs(graph, start, destination):
    """
    Find a path with the fewest road segments using BFS.

    Returns:
        A dictionary containing the path, road segments,
        and total distance.
        Returns None if no path exists.
    Raises:
        ValueError for invalid locations.
    """

    if start not in graph:
        raise ValueError(f"Invalid starting location: {start}")

    if destination not in graph:
        raise ValueError(f"Invalid destination: {destination}")

    queue = deque([start])
    visited = {start}
    predecessor = {start: None}

    while queue:
        current = queue.popleft()

        if current == destination:
            break

        for neighbour in graph[current]:
            if neighbour not in visited:
                visited.add(neighbour)
                predecessor[neighbour] = current
                queue.append(neighbour)

    # Destination cannot be reached
    if destination not in visited:
        return None

    # Reconstruct the path
    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = predecessor[current]

    path.reverse()

    # Calculate the distance along the BFS path
    total_distance = sum(
        graph[path[i]][path[i + 1]]
        for i in range(len(path) - 1)
    )

    return {
        "path": path,
        "road_segments": len(path) - 1,
        "total_distance": total_distance,
    }


if __name__ == "__main__":
    from graph import load_city_map

    city_graph = load_city_map()
    result = bfs(city_graph, "College", "Hospital")

    if result:
        print("BFS Route:", " -> ".join(result["path"]))
        print("Road segments:", result["road_segments"])
        print("Total distance:", result["total_distance"], "km")
    else:
        print("No route found.")
