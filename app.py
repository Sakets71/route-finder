import streamlit as st
import matplotlib.pyplot as plt

from algorithms.graph import load_city_map
from algorithms.bfs import bfs
from algorithms.dijkstra import dijkstra
from visualization.graph_view import draw_city_graph


# =====================================================
# Page configuration
# =====================================================
st.set_page_config(
    page_title="Route Finder · City Navigation",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =====================================================
# Design system
# =====================================================
st.markdown(
    """
    <style>
    /* ---------- Base ---------- */
    html, body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                     Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    .stApp { background: #F6F6F1; color: #17211B; }
    .block-container {
        max-width: 1160px;
        padding: 2.25rem 2rem 3.5rem;
    }

    /* ---------- Typography ---------- */
    h1, h2, h3, h4 {
        color: #17211B !important;
        letter-spacing: -0.02em;
        font-weight: 650 !important;
    }
    h1 { font-size: 2.4rem !important; line-height: 1.15 !important; }
    h2 { font-size: 1.35rem !important; }
    h3 { font-size: 1.18rem !important; }

    /* ---------- Hero ---------- */
    .hero-kicker {
        display: inline-flex;
        align-items: center;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: #2E6B4E;
        background: #E8F0EA;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        margin-bottom: 1rem;
    }
    .hero-subtitle {
        color: #5A6B60;
        font-size: 1.02rem;
        max-width: 580px;
        line-height: 1.6;
        margin: 0 0 1.5rem;
    }

    /* ---------- Card containers ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF;
        border: 1px solid #E4E8DF;
        border-radius: 14px;
        box-shadow: 0 1px 2px rgba(20, 35, 27, 0.03);
    }
    /* Remove the inner form's own border so it doesn't double-up */
    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
    }

    /* ---------- Form inputs ---------- */
    div[data-baseweb="select"] > div {
        background: #FFFFFF !important;
        border: 1px solid #DCE1D8 !important;
        border-radius: 10px !important;
        min-height: 44px !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: #B8C6BA !important;
    }
    div[data-baseweb="select"] > div:focus-within {
        border-color: #2E6B4E !important;
        box-shadow: 0 0 0 3px rgba(46, 107, 78, 0.12) !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] input { color: #17211B !important; }

    [data-testid="stWidgetLabel"] p {
        color: #4B5A50 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.35rem !important;
    }

    /* ---------- Metrics ---------- */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E4E8DF;
        border-radius: 12px;
        padding: 1rem 1.15rem;
        box-shadow: 0 1px 2px rgba(20, 35, 27, 0.03);
    }
    div[data-testid="stMetricLabel"] p {
        color: #6B7A70 !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    div[data-testid="stMetricValue"] {
        color: #17211B !important;
        font-size: 1.65rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    /* ---------- Buttons ---------- */
    div[data-testid="stFormSubmitButton"] button,
    div[data-testid="stButton"] button {
        background: #2E6B4E;
        color: #FFFFFF !important;
        border: 1px solid #2E6B4E;
        border-radius: 10px;
        min-height: 46px;
        font-weight: 600;
        font-size: 0.95rem;
        transition: background 0.15s ease, border-color 0.15s ease;
    }
    div[data-testid="stFormSubmitButton"] button:hover,
    div[data-testid="stButton"] button:hover {
        background: #245640;
        border-color: #245640;
        color: #FFFFFF !important;
    }

    /* ---------- Dividers ---------- */
    hr {
        border: none;
        border-top: 1px solid #E4E8DF;
        margin: 2rem 0 !important;
    }

    /* ---------- Route timeline ---------- */
    .route-timeline { display: flex; flex-direction: column; }
    .timeline-item {
        display: grid;
        grid-template-columns: 20px 1fr;
        gap: 1rem;
        padding-bottom: 1.4rem;
        position: relative;
        align-items: start;
    }
    .timeline-item:last-child { padding-bottom: 0; }
    .timeline-item:not(:last-child)::before {
        content: "";
        position: absolute;
        left: 9px;
        top: 22px;
        bottom: 0;
        width: 2px;
        background: #D5DED6;
        border-radius: 1px;
    }
    .timeline-dot {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        border: 3px solid #2E6B4E;
        background: #FFFFFF;
        box-sizing: border-box;
        margin: 4px auto 0;
        position: relative;
        z-index: 1;
    }
    .timeline-item.destination .timeline-dot { background: #2E6B4E; }
    .timeline-label {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #6B7A70;
        margin-bottom: 0.2rem;
    }
    .timeline-item.start .timeline-label,
    .timeline-item.destination .timeline-label { color: #2E6B4E; }
    .timeline-title {
        font-size: 1.05rem;
        font-weight: 650;
        color: #17211B;
        letter-spacing: -0.01em;
        margin-bottom: 0.15rem;
    }
    .timeline-meta { font-size: 0.85rem; color: #6B7A70; }

    /* ---------- Location chips ---------- */
    .location-chip {
        display: inline-block;
        background: #FFFFFF;
        border: 1px solid #E4E8DF;
        border-radius: 999px;
        padding: 0.4rem 0.85rem;
        margin: 0.2rem 0.3rem 0.2rem 0;
        font-size: 0.87rem;
        color: #17211B;
        font-weight: 500;
    }

    /* ---------- Footer ---------- */
    .app-footer {
        color: #7A887F;
        font-size: 0.82rem;
        text-align: center;
        padding: 1rem 0;
    }

    /* ---------- Responsive ---------- */
    @media (max-width: 780px) {
        .block-container { padding: 1.25rem 1rem 2rem; }
        h1 { font-size: 1.85rem !important; }
        div[data-testid="stMetricValue"] { font-size: 1.35rem !important; }
        div[data-testid="stHorizontalBlock"] { gap: 0.75rem !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# Hero
# =====================================================
st.markdown('<div class="hero-kicker">City Routing Project</div>', unsafe_allow_html=True)
st.title("Route Finder")
st.markdown(
    """
    <p class="hero-subtitle">
        Plan the shortest or simplest journey across the sample city network.
        Choose a starting point, pick a destination, and let the algorithm
        find the route.
    </p>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# Load graph
# =====================================================
try:
    graph = load_city_map()
except (OSError, ValueError, KeyError) as error:
    st.error(f"Could not load the city map: {error}")
    st.stop()

locations = list(graph.keys())
if not locations:
    st.error("The city map contains no locations.")
    st.stop()

total_locations = len(graph)
total_roads = sum(len(neighbours) for neighbours in graph.values()) // 2


# =====================================================
# Session state
# =====================================================
if "route_result" not in st.session_state:
    st.session_state.route_result = None
if "route_details" not in st.session_state:
    st.session_state.route_details = None


# =====================================================
# Stats ribbon
# =====================================================
details_now = st.session_state.route_details

m1, m2, m3 = st.columns(3)
m1.metric("Locations", total_locations)
m2.metric("Road connections", total_roads)
m3.metric("Route method", details_now["algorithm"] if details_now else "—")


# =====================================================
# Route planner
# =====================================================
st.write("")
with st.container(border=True):
    st.subheader("Plan your route")
    st.caption("Select your starting point, destination, and route method.")

    with st.form("route_form"):
        col_start, col_dest, col_algo = st.columns([1.2, 1.2, 1])

        with col_start:
            source = st.selectbox(
                "Starting point",
                locations,
                index=locations.index("College") if "College" in locations else 0,
            )
        with col_dest:
            destination = st.selectbox(
                "Destination",
                locations,
                index=locations.index("Hospital") if "Hospital" in locations else 0,
            )
        with col_algo:
            algorithm = st.selectbox(
                "Route method",
                ["Dijkstra", "BFS"],
                help=(
                    "Dijkstra minimizes total distance. "
                    "BFS minimizes the number of road segments."
                ),
            )

        find_route = st.form_submit_button(
            "Find route",
            type="primary",
            use_container_width=True,
        )


# =====================================================
# Route calculation
# =====================================================
if find_route:
    if source == destination:
        st.session_state.route_result = None
        st.session_state.route_details = None
        st.warning("Choose two different locations to find a route.")
    else:
        try:
            with st.spinner("Calculating your route…"):
                if algorithm == "BFS":
                    result = bfs(graph, source, destination)
                else:
                    result = dijkstra(graph, source, destination)

            if result:
                st.session_state.route_result = result
                st.session_state.route_details = {
                    "source": source,
                    "destination": destination,
                    "algorithm": algorithm,
                }
            else:
                st.session_state.route_result = None
                st.session_state.route_details = None
                st.warning("No route was found between these locations.")
        except (ValueError, KeyError) as error:
            st.session_state.route_result = None
            st.session_state.route_details = None
            st.error(f"Could not calculate the route: {error}")


# =====================================================
# Results / empty state
# =====================================================
result = st.session_state.route_result
details = st.session_state.route_details

if result and details:
    path = result["path"]
    total_distance = result["total_distance"]
    road_segments = result["road_segments"]

    st.divider()

    # Journey header
    st.subheader("Your journey")
    st.markdown(f"**{details['source']}** → **{details['destination']}**")
    st.caption(f"Calculated using {details['algorithm']}")

    st.write("")

    # Journey metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Total distance", f"{total_distance:g} km")
    c2.metric("Road segments", road_segments)
    c3.metric("Locations visited", len(path))

    st.write("")

    # Timeline
    with st.container(border=True):
        st.subheader("Route details")

        parts = []
        for i, location in enumerate(path):
            is_start = i == 0
            is_end = i == len(path) - 1
            cls = "timeline-item"
            if is_start:
                cls += " start"
            if is_end:
                cls += " destination"

            if is_start:
                label = "Start"
            elif is_end:
                label = "Destination"
            else:
                label = f"Stop {i}"

            meta = ""
            if i < len(path) - 1:
                nxt = path[i + 1]
                dist = graph[location][nxt]
                meta = f'<div class="timeline-meta">{dist:g} km to {nxt}</div>'

            parts.append(
                f'<div class="{cls}">'
                f'<div class="timeline-dot"></div>'
                f'<div>'
                f'<div class="timeline-label">{label}</div>'
                f'<div class="timeline-title">{location}</div>'
                f'{meta}'
                f'</div>'
                f'</div>'
            )

        st.markdown(
            f'<div class="route-timeline">{"".join(parts)}</div>',
            unsafe_allow_html=True,
        )

    # Graph
    st.write("")
    st.subheader("City network diagram")

    try:
        fig = draw_city_graph(
            graph=graph,
            path=path,
            title=f"{details['algorithm']} route",
            save_path=None,
            show=False,
        )
        if fig is not None:
            st.plotly_chart(
            fig,
            use_container_width=True,
             config={
                   "scrollZoom": True,
                 "displaylogo": False
                }
        )
            
        else:
            st.info(
                "The visualization function did not return a Matplotlib figure. "
                "The UI is ready, but the visualization function will need "
                "a small adjustment."
            )
    except Exception as error:
        st.warning(f"Could not display the network diagram: {error}")

else:
    st.divider()
    st.subheader("Locations in this city")
    st.caption("Your sample network currently contains these locations.")

    chips = "".join(
        f'<span class="location-chip">{loc}</span>' for loc in locations
    )
    st.markdown(f"<div>{chips}</div>", unsafe_allow_html=True)


# =====================================================
# Footer
# =====================================================
st.write("")
st.divider()
st.markdown(
    '<div class="app-footer">Route Finder · Built with Python, Streamlit, and graph algorithms</div>',
    unsafe_allow_html=True,
)