# PathNova — Route Finder

**PathNova** is a Python route-finding project that demonstrates graph traversal and shortest-path algorithms through an interactive Streamlit web application.

- **Live demo:** https://pathnova.streamlit.app/
- **GitHub repository:** https://github.com/Sakets71/route-finder

## Features

- Choose a starting location and destination in a sample city network.
- Find routes using **Breadth-First Search (BFS)** or **Dijkstra's algorithm**.
- View total route distance, number of road segments, and locations visited.
- Explore an interactive Plotly graph with road-distance labels and highlighted route edges.
- View a step-by-step route timeline.
- Use a light-themed, responsive Streamlit interface.

## Algorithms

### Breadth-First Search (BFS)

BFS explores the graph level by level and finds a path with the fewest road segments (edges). Because road distances can differ, this path is not necessarily the shortest by total distance.

### Dijkstra's Algorithm

Dijkstra's algorithm finds a route with the minimum total edge weight when all road weights are non-negative. In this project, edge weights represent distances in kilometres.

## Tech Stack

- Python
- Streamlit
- NetworkX
- Plotly
- Matplotlib (imported in the current `app.py`)
- JSON city-map data

## Project Structure

```text
route_finder/
├── .devcontainer/
│   └── devcontainer.json
├── algorithms/
│   ├── bfs.py
│   ├── dijkstra.py
│   └── graph.py
├── data/
│   └── city_map.json
├── visualization/
│   └── graph_view.py
├── app.py
├── bfs_route.png
├── .gitignore
├── requirements.txt
└── README.md
```

The `.venv/` directory is a local virtual environment and should not be uploaded to GitHub.

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Sakets71/route-finder.git
cd route-finder
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Make sure `requirements.txt` contains the external packages imported by your code. For the current files, it will likely include:

```text
streamlit
matplotlib
networkx
plotly
```

Add any other third-party packages your code requires.

### 4. Start the app

```bash
streamlit run app.py
```

Streamlit prints a local URL in the terminal. Open that URL in your browser.

## How to Use

1. Select a starting point.
2. Select a different destination.
3. Choose **BFS** or **Dijkstra**.
4. Click **Find route**.
5. Review the distance, road segments, locations visited, route timeline, and highlighted graph.

## Live Deployment

Try the deployed app: **https://pathnova.streamlit.app/**

The app is deployed from GitHub using Streamlit Community Cloud. The deployment needs a valid `requirements.txt` at the repository root (or next to the app entrypoint) so the cloud environment can install the packages used by the code.

## Notes

- This is a sample weighted city graph, not a live GPS navigation system.
- Node positions in the graph visualization are illustrative drawing coordinates, not GPS coordinates.
- BFS minimizes the number of edges; Dijkstra minimizes the total edge weight.

## Future Improvements

- Further refine the mobile layout.
- Add more locations and road connections.
- Expand automated tests for unreachable destinations and invalid input.
- Improve accessibility and graph controls.

## Author

Created as a Python Data Structures and Algorithms project.

## License

No license has been specified yet. Add a `LICENSE` file if you want to grant others explicit permission to reuse, modify, or distribute this project.
