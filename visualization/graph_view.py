import networkx as nx
import plotly.graph_objects as go


# Fixed positions make the city map consistent and easier to read.
CITY_POSITIONS = {
    "College": (0, 1),
    "Market": (2, 1),
    "City Center": (2.2, -1),
    "Hospital": (0.2, -0.5),
    "Bus Stand": (-0.2, -2),
    "Railway Station": (-2, -1),
    "Airport": (-3.5, 0.5),
    "Park": (2.1, -3),
    "Mall": (-1.8, 1.5),
    "Library": (-1.8, 3),
}


# ---------------------------------------------------------------------------
# Colour palette (light theme)
# ---------------------------------------------------------------------------
_BG = "#F8FAFC"            # outer background
_PLOT_BG = "#FFFFFF"       # plot-area background
_TEXT = "#1E293B"          # primary text
_MUTED = "#64748B"         # secondary text / distance labels

_EDGE = "rgba(148, 163, 184, 0.50)"      # normal road
_ROUTE_EDGE = "#3B82F6"                  # highlighted route

_SOURCE = "#22C55E"        # green
_DEST = "#F97316"          # orange
_ROUTE_NODE = "#93C5FD"    # on-route intermediate
_NORMAL = "#94A3B8"        # other locations

_FONT = "Inter, system-ui, -apple-system, Segoe UI, sans-serif"


def _midpoint(p1, p2):
    return ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)


def draw_city_graph(
    graph,
    path=None,
    title="City Route Map",
    save_path=None,
    show=True,
):
    """Draw an interactive Plotly city graph and highlight an optional route.

    Same signature and return contract as the previous Matplotlib version:
      - show=True  -> opens the figure, returns None
      - show=False -> returns the go.Figure
    """

    # --- Build NetworkX graph from the adjacency dict ------------------------
    network = nx.Graph()
    for location, neighbours in graph.items():
        network.add_node(location)
        for neighbour, distance in neighbours.items():
            network.add_edge(location, neighbour, distance=distance)

    # --- Positions -----------------------------------------------------------
    positions = {
        location: CITY_POSITIONS[location]
        for location in network.nodes
        if location in CITY_POSITIONS
    }
    missing = set(network.nodes) - set(positions)
    if missing:
        raise ValueError(f"Missing map positions for: {sorted(missing)}")

    # --- Route validation ----------------------------------------------------
    route_edges = []
    if path and len(path) > 1:
        route_edges = list(zip(path, path[1:]))
        for source, destination in route_edges:
            if not network.has_edge(source, destination):
                raise ValueError(
                    f"Route contains a road that does not exist: "
                    f"{source} -> {destination}"
                )
    route_edge_set = {frozenset(e) for e in route_edges}
    path_set = set(path) if path else set()

    # --- Split edges into normal vs route geometry ---------------------------
    normal_x, normal_y = [], []
    route_x, route_y = [], []

    for s, d, _data in network.edges(data=True):
        x1, y1 = positions[s]
        x2, y2 = positions[d]
        if frozenset((s, d)) in route_edge_set:
            route_x.extend([x1, x2, None])
            route_y.extend([y1, y2, None])
        else:
            normal_x.extend([x1, x2, None])
            normal_y.extend([y1, y2, None])

    # --- Midpoint labels + hover for each road -------------------------------
    label_x, label_y, label_text, label_hover = [], [], [], []
    for s, d, data in network.edges(data=True):
        mx, my = _midpoint(positions[s], positions[d])
        dist = data.get("distance", 0)
        label_x.append(mx)
        label_y.append(my)
        label_text.append(f"{dist:g} km")
        label_hover.append(f"<b>{s}</b> ↔ <b>{d}</b><br>{dist:g} km")

    # --- Classify nodes ------------------------------------------------------
    source_node = path[0] if path else None
    dest_node = path[-1] if path else None

    def classify(node):
        if node == source_node:
            return "source"
        if node == dest_node:
            return "dest"
        if path and node in path_set:
            return "route"
        return "normal"

    def node_hover(node):
        role = classify(node)
        role_label = {
            "source": "Source",
            "dest": "Destination",
            "route": "On route",
            "normal": "Location",
        }[role]
        degree = network.degree(node)
        adj_dist = sum(
            data.get("distance", 0)
            for _, _, data in network.edges(node, data=True)
        )
        return (
            f"<b>{node}</b><br>"
            f"{role_label}<br>"
            f"Connected roads: {degree}<br>"
            f"Total adjacent distance: {adj_dist:g} km"
        )

    grouped = {"source": [], "dest": [], "route": [], "normal": []}
    for node in network.nodes:
        grouped[classify(node)].append(node)

    # --- Build the figure ----------------------------------------------------
    fig = go.Figure()

    # 1. Normal roads
    if normal_x:
        fig.add_trace(go.Scatter(
            x=normal_x, y=normal_y,
            mode="lines",
            line=dict(color=_EDGE, width=2),
            hoverinfo="skip",
            name="Road",
            legendgroup="roads",
            showlegend=True,
        ))

    # 2. Selected route (drawn above normal roads)
    if route_x:
        fig.add_trace(go.Scatter(
            x=route_x, y=route_y,
            mode="lines",
            line=dict(color=_ROUTE_EDGE, width=5),
            hoverinfo="skip",
            name="Selected route",
            legendgroup="route",
            showlegend=True,
        ))

    # 3. Distance labels at midpoints (also hoverable for road info)
    if label_x:
        fig.add_trace(go.Scatter(
            x=label_x, y=label_y,
            mode="markers+text",
            marker=dict(
                size=12,
                color="rgba(255, 255, 255, 0.01)",  # invisible but hoverable
                line=dict(color="rgba(0,0,0,0)", width=0),
            ),
            text=label_text,
            textposition="middle center",
            textfont=dict(family=_FONT, size=10, color=_MUTED),
            hovertext=label_hover,
            hoverinfo="text",
            showlegend=False,
        ))

    # 4. Nodes (drawn last so labels sit on top of edges)
    node_styles = {
        "route":  dict(color=_ROUTE_NODE, size=20, name="On route"),
        "normal": dict(color=_NORMAL,     size=18, name="Location"),
        "source": dict(color=_SOURCE,     size=26, name="Source"),
        "dest":   dict(color=_DEST,       size=26, name="Destination"),
    }

    for category in ("route", "normal", "source", "dest"):
        nodes = grouped[category]
        if not nodes:
            continue
        style = node_styles[category]
        fig.add_trace(go.Scatter(
            x=[positions[n][0] for n in nodes],
            y=[positions[n][1] for n in nodes],
            mode="markers+text",
            marker=dict(
                size=style["size"],
                color=style["color"],
                line=dict(color="white", width=2.5),
            ),
            text=nodes,
            textposition="top center",
            textfont=dict(family=_FONT, size=12, color=_TEXT),
            hovertext=[node_hover(n) for n in nodes],
            hoverinfo="text",
            name=style["name"],
            legendgroup=category,
            showlegend=True,
        ))

    # --- Layout --------------------------------------------------------------
    fig.update_layout(
        title=dict(
            text=title,
            x=0.02, xanchor="left",
            font=dict(family=_FONT, size=20, color=_TEXT),
        ),
        paper_bgcolor=_BG,
        plot_bgcolor=_PLOT_BG,
        font=dict(family=_FONT, color=_TEXT),
        # FIX: Increased bottom margin to b=120 so text doesn't cut off
        margin=dict(l=40, r=40, t=80, b=120),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#E2E8F0",
            font=dict(family=_FONT, size=12, color=_TEXT),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=-0.15,
            xanchor="center", x=0.5,
            bgcolor="rgba(255,255,255,0)",
            font=dict(size=11, color=_MUTED),
        ),
        dragmode="pan",
        hovermode="closest",
        # FIX: Added height to make mobile rendering larger
        height=600,
        annotations=[
            dict(
                text=(
                    "Abstract layout — node positions are drawing "
                    "coordinates, not GPS coordinates."
                ),
                xref="paper", yref="paper",
                x=0.5, y=-0.22,
                xanchor="center", yanchor="top",
                showarrow=False,
                font=dict(family=_FONT, size=10, color=_MUTED),
            ),
        ],
    )

    # Equal aspect ratio keeps the drawing undistorted
    fig.update_xaxes(visible=False, scaleanchor="y", scaleratio=1)
    fig.update_yaxes(visible=False)

    # --- Save / show ---------------------------------------------------------
    if save_path:
        if save_path.lower().endswith(".html"):
            fig.write_html(save_path, include_plotlyjs="cdn")
        else:
            try:
                fig.write_image(save_path, scale=2)
            except Exception as error:
                raise RuntimeError(
                    "Saving to an image file requires `kaleido`. "
                    "Install with: python -m pip install kaleido. "
                    f"Original error: {error}"
                )

    if show:
        fig.show()
        return None

    return fig


if __name__ == "__main__":
    from algorithms.graph import load_city_map
    from algorithms.bfs import bfs

    city_graph = load_city_map()
    result = bfs(city_graph, "College", "Hospital")

    if result:
        draw_city_graph(
            city_graph,
            path=result["path"],
            title="BFS Route: College to Hospital",
            save_path="bfs_route.html",
        )
    else:
        print("No route found.")
        