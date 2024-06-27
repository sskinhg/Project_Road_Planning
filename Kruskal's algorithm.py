import sys

# Constants based on problem constraints
MAX_VILLAGES = 1000  
MAX_ROADS = 3 * MAX_VILLAGES 
INF = 0x3f3f3f3f  

# Edge class to represent a road between two villages
class Edge:
    def __init__(self, x, y, v):
        self.x = x  # First vertex (village)
        self.y = y  # Second vertex (village)
        self.v = v  # Weight of the edge (cost of the road)

# Global variables
edges = [Edge(0, 0, 0) for _ in range(MAX_ROADS)]  # List to store all possible edges (roads)
n = 0  # Number of vertices (villages)
m = 0  # Number of edges (roads)
weight = 0  # Total weight of the minimum spanning tree (total cost of selected roads)
pred = [0] * (MAX_VILLAGES + 1)  # Parent array for disjoint set data structure (used for cycle detection)

# Quick sort implementation to sort edges by weight
def quicksort(l, r):
    global edges
    i, j = l, r
    m = edges[(l + r) // 2].v
    while i <= j:
        while edges[i].v < m:
            i += 1
        while edges[j].v > m:
            j -= 1
        if i <= j:
            edges[i], edges[j] = edges[j], edges[i]
            i += 1
            j -= 1
    if l < j:
        quicksort(l, j)
    if i < r:
        quicksort(i, r)

# Find operation for disjoint set with path compression
def search(x):
    global pred
    # If x is the root of its set
    if pred[x] == x:
        return x
    else:
        # Path compression: make every node on the path point directly to the root
        pred[x] = search(pred[x])
        return pred[x]

def main():
    global n, m, weight, edges, pred

    # Example
    input_data = """6 15
1 2 5
1 3 3
1 4 7
1 5 4
1 6 2
2 3 4
2 4 6
2 5 2
2 6 6
3 4 6
3 5 1
3 6 1
4 5 10
4 6 8
5 6 3"""

    # Process input
    lines = input_data.split('\n')
    n, m = map(int, lines[0].split())
    print(f"Number of villages: {n}")
    print(f"Number of candidate roads: {m}")
    
    # Read and store all edges
    print("\nReading edges:")
    for i, line in enumerate(lines[1:], start=1):
        x, y, v = map(int, line.split())
        edges[i-1] = Edge(x, y, v)
        print(f"Edge {i}: {x}-{y}, Weight: {v}")

    # Sort edges by weight (a key step in Kruskal's algorithm)
    print("\nSorting edges...")
    quicksort(0, m - 1)  # Using quicksort for efficiency
    
    # Display sorted edges for verification
    print("\nSorted edges:")
    for i in range(m):
        print(f"Edge: {edges[i].x}-{edges[i].y}, Weight: {edges[i].v}")
    
    # Initialize disjoint sets (each village in its own set)
    print("\nInitializing disjoint sets...")
    for i in range(1, n + 1):
        pred[i] = i  # Each village is initially its own parent
    
    # Main loop of Kruskal's algorithm
    print("\nBuilding Minimum Spanning Tree:")
    weight = 0
    mst_edges = []
    for i in range(m):
        x_root = search(edges[i].x)
        y_root = search(edges[i].y)
        if x_root != y_root:
            # If villages are not in the same set, add the edge to MST
            print(f"Adding edge {edges[i].x}-{edges[i].y} with weight {edges[i].v}")
            pred[x_root] = y_root  # Union operation: merge the sets
            weight += edges[i].v  # Add the weight to the total
            mst_edges.append((edges[i].x, edges[i].y, edges[i].v))
    
    # Check if all villages are connected (MST should have n-1 edges)
    print("\nChecking if all villages are connected...")
    root = search(1)
    all_connected = all(search(i) == root for i in range(1, n + 1))
    
    print("\nFinal result:")
    if not all_connected:
        print("orz (Not all villages can be connected)")
    else:
        print(f"Minimum cost to connect all villages: {weight}")
        print("Edges in the Minimum Spanning Tree:")
        for edge in mst_edges:
            print(f"{edge[0]}-{edge[1]}: {edge[2]}")

if __name__ == "__main__":
    main()