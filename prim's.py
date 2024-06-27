import math


MAX_VILLAGES = 1000  # Maximum number of villages (vertices)
MAX_ROADS = 3 * MAX_VILLAGES  # Maximum number of roads (edges)
INF = 0x3f3f3f3f 

# Fibonacci Heap Node class
class FibonacciNode:
    def __init__(self, vertex, key):
        self.vertex = vertex  # Vertex number
        self.key = key  # Key value (distance/weight)
        self.parent = self.child = self.left = self.right = None  # Pointers for heap structure
        self.degree = 0  # Number of children
        self.mark = False  # Mark for cascading cuts

# Fibonacci Heap class
class FibonacciHeap:
    def __init__(self):
        self.min = None  # Pointer to the minimum node
        self.count = 0  # Number of nodes in the heap

    # Insert a new node into the heap
    def insert(self, vertex, key):
        node = FibonacciNode(vertex, key)
        node.left = node.right = node
        self.merge(node)
        self.count += 1
        return node

    # Merge a node into the root list
    def merge(self, node):
        if not self.min:
            self.min = node
        else:
            # Insert node into the root list
            node.right = self.min.right
            node.left = self.min
            self.min.right.left = node
            self.min.right = node
            if node.key < self.min.key:
                self.min = node

    # Extract the minimum node from the heap
    def extract_min(self):
        z = self.min
        if z:
            if z.child:
                # Add all of z's children to the root list
                children = [z.child]
                current = z.child.right
                while current != z.child:
                    children.append(current)
                    current = current.right
                for child in children:
                    self.merge(child)
                    child.parent = None
            # Remove z from the root list
            z.left.right = z.right
            z.right.left = z.left
            if z == z.right:
                self.min = None
            else:
                self.min = z.right
                self.consolidate()
            self.count -= 1
        return z

    # Consolidate the heap after extraction
    def consolidate(self):
        max_degree = int(math.log2(self.count)) + 1
        A = [None] * (max_degree + 1)
        nodes = []
        current = self.min
        while current:
            nodes.append(current)
            current = current.right
            if current == self.min:
                break

        for w in nodes:
            x = w
            d = x.degree
            while d < len(A) and A[d]:
                y = A[d]
                if x.key > y.key:
                    x, y = y, x
                self.heap_link(y, x)
                A[d] = None
                d += 1
            if d == len(A):
                A.append(None)
            A[d] = x

        # Reconstruct the root list from the array
        self.min = None
        for node in A:
            if node:
                if not self.min:
                    self.min = node
                    node.left = node.right = node
                else:
                    self.merge(node)

    # Link two nodes in the consolidation process
    def heap_link(self, y, x):
        y.left.right = y.right
        y.right.left = y.left
        y.parent = x
        if not x.child:
            x.child = y
            y.left = y.right = y
        else:
            y.left = x.child
            y.right = x.child.right
            x.child.right.left = y
            x.child.right = y
        x.degree += 1
        y.mark = False

    # Decrease the key of a node
    def decrease_key(self, node, new_key):
        if new_key > node.key:
            return
        node.key = new_key
        parent = node.parent
        if parent and node.key < parent.key:
            self.cut(node, parent)
            self.cascading_cut(parent)
        if node.key < self.min.key:
            self.min = node

    # Cut a node from its parent
    def cut(self, child, parent):
        if child == child.right:
            parent.child = None
        else:
            child.left.right = child.right
            child.right.left = child.left
            if parent.child == child:
                parent.child = child.right
        parent.degree -= 1
        child.left = child.right = child
        child.parent = None
        child.mark = False
        self.merge(child)

    # Perform cascading cut operation
    def cascading_cut(self, node):
        parent = node.parent
        if parent:
            if not node.mark:
                node.mark = True
            else:
                self.cut(node, parent)
                self.cascading_cut(parent)

vertexNum = 0  # Number of vertices (villages)
edgeNum = 0  # Number of edges (roads)
g = [[] for _ in range(MAX_VILLAGES + 1)]  # Adjacency list representation of the graph
parent = [0] * (MAX_VILLAGES + 1)  # Parent array to store the MST structure

# Prim's algorithm implementation using Fibonacci Heap
def prim():
    global vertexNum, g, parent
    
    dist = [INF] * (MAX_VILLAGES + 1)  # Distance array
    visited = [False] * (MAX_VILLAGES + 1)  # Visited array
    parent = [0] * (MAX_VILLAGES + 1)  # Parent array
    node_refs = [None] * (MAX_VILLAGES + 1)  # References to heap nodes
    
    fheap = FibonacciHeap()
    dist[1] = 0
    node_refs[1] = fheap.insert(1, 0)  # Start with vertex 1
    
    res = 0  # Total weight of the MST

    try:
        while fheap.count > 0:
            min_node = fheap.extract_min()
            if min_node is None:
                break
            u = min_node.vertex
            
            if visited[u]:
                continue
            
            visited[u] = True
            res += min_node.key

            # Process all adjacent vertices
            for v, weight in g[u]:
                if not visited[v] and weight < dist[v]:
                    dist[v] = weight
                    parent[v] = u
                    if node_refs[v]:
                        fheap.decrease_key(node_refs[v], weight)
                    else:
                        node_refs[v] = fheap.insert(v, weight)

        # Check if all vertices are connected
        if sum(visited) != vertexNum:
            return -1  # Graph is disconnected
        return res
    except Exception as e:
        print(f"An error occurred during Prim's algorithm: {e}")
        return -1

def main():
    global vertexNum, edgeNum, g

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

    lines = input_data.split('\n')
    vertexNum, edgeNum = map(int, lines[0].split())
    print(f"Number of villages: {vertexNum}")
    print(f"Number of roads: {edgeNum}")

    print("\nReading edges:")
    for line in lines[1:]:
        a, b, c = map(int, line.split())
        g[a].append((b, c))
        g[b].append((a, c))
        print(f"Edge: {a}-{b}, Weight: {c}")

    print("\nRunning Prim's algorithm with Fibonacci Heap...")
    res = prim()

    print("\nFinal result:")
    if res == -1:
        print("orz (Not all villages can be connected)")
    else:
        print(f"Minimum cost to connect all villages: {res}")

        print("\nEdges in the Minimum Spanning Tree:")
        for i in range(2, vertexNum + 1):
            print(f"{parent[i]}-{i}: {next(w for v, w in g[i] if v == parent[i])}")

if __name__ == "__main__":
    main()