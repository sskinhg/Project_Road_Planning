Project Centric:
This project addresses a fundamental challenge in civil engineering and urban planning: how to link two or more villages or towns with roads infrastructure that will call for less construction costs yet ensure that all locations within the areas are connected. This is a problem well known in graph theory as the Minimum Spanning Tree (MST) problem, this optimization is more critical in the developing nations where resources and funds are limited and the benefit that comes with proper planning displayed. 

Designed Hands on problem for this:
Background & Goal:
A statistical data table of existing inter-village roads lists the cost of roads that have the potential to be constructed as standard, finds the minimum cost required to make each village connected by a road.
Input Format:
The input data consists of the number of towns as positive integers N (≤1000) and the number of candidate roads M (≤3N) (first row as i.e. 6 15 means 6 towns and 15 candidates roads ); the subsequent(starting row No.2) M rows correspond to the M roads, and each row gives three positive integers, the numbers of the two towns to which the road is directly connected, and the budgeted cost of reconstructing the road.(i.e. 1 2 3 means road connecting town/village 1 and 2 has a cost of 3 ) For simplicity, towns/villages are numbered from 1 to N.
Sample input:
![image](https://github.com/sskinhg/Project_Road_Planning/assets/53120023/758da051-8d5d-459c-8796-2b6bc8303dcf)
  	First row No. of total villages and No. of roads candidates
  	From Second row to M row: each row indicates villages number the road connects (Column 1 and 2) and building cost(Column 3)
Output Format:
Output the minimum cost required for village access. If the input data is not enough to ensure access, output -1, indicating that more roads need to be built.

Two implementations for this project.
1.Prim’s Algorithm with Fibonacci Heap Enhancement:
My implementation of Prim's algorithm for the road planning problem leverages a Fibonacci Heap to achieve superior theoretical performance. The algorithm starts by representing the network as an adjacency list g, where each entry g[i] contains the neighboring villages and road costs for village i.
The base of this implementation is the FibonacciHeap class, a complex data structure that supports efficient decrease-key operations. The heap maintains a collection of trees, with the minimum element always accessible at the root of one tree. Key operations include insert, extract_min, and decrease_key, all implemented with amortized time complexities that outperform binary heaps for large inputs. Also much better performance than the time complexity O(n^2) with adjacency matrix
The prim function orchestrates the algorithm. It initializes distance and visited arrays, and creates a Fibonacci Heap with the starting village. The main loop continues until the heap is empty, each iteration extracting the minimum-distance village, marking it as visited, and processing its adjacent unvisited villages.
For each adjacent village, if a cheaper road is found, the algorithm updates the distance and parent information. The decrease_key operation of the Fibonacci Heap is crucial here, allowing for efficient updates of village distances in the heap.
A significant optimization is the use of node references (node_refs array) to keep track of each village's node in the heap. This allows for O(1) access when performing decrease-key operations, contributing to the algorithm's efficiency.
The implementation achieves a remarkable time complexity of O(E + log V), where E is the number of edges and V the number of vertices. This efficiency stems from the Fibonacci Heap's amortized O(1) time for decrease-key operations and O(log V) for a single extract-min operation over the course of the algorithm.
Error handling is implemented with a try-except block in the prim function, ensuring robustness against unexpected issues during execution. The algorithm concludes by checking if all villages are connected and returns either the total weight(cost) of the MST or -1 if full connectivity isn't achieved.

2.Kruskal’s Algorithm Implementation:
This implementation of Kruskal's algorithm efficiently solves the road planning problem by constructing a minimum spanning tree (MST). The algorithm uses a global array edges to store all potential roads, each represented as an Edge object containing two vertices and a weight (cost).
I implemented quicksort, which sorts the edges by weight(cost) in ascending order. This sorting is crucial as it allows the algorithm to consider cheaper roads first. The search function implements a disjoint-set data structure with path compression, used for cycle detection.
The main algorithm starts by initializing each village as a separate set. It then iterates through the sorted edges, using the search function to check if the two vertices of an edge are already in the same set (connected component). If they're not, the edge is added to the MST, and the sets are merged using union by rank (implemented implicitly in the search function).
A key optimization is the use of path compression in the search function. When finding the root of a set, it updates the parent of each node along the path to point directly to the root, flattening the tree structure and speeding up future searches.
The algorithm's efficiency is evident in its time complexity of O(E log E), where E is the number of edges. This comes from the sorting step, as the disjoint-set operations are nearly constant time due to path compression. The space complexity is O(E + V), with E space for the edge list and V for the disjoint-set structure.
One notable aspect is the use of a global pred array to track the parent of each vertex in the disjoint-set, allowing for efficient set operations without additional memory allocation during the algorithm's execution.
The implementation concludes by checking if all villages are connected (by counting unique roots) and either returning the total weight of the MST or 'orz' if not all villages can be connected. This final check ensures the solution meets the problem's requirement of full connectivity.
Overall, this implementation of Kruskal's algorithm provides an efficient and memory-conscious solution to the road planning problem, particularly effective for sparse networks where the number of potential roads is not significantly larger than the number of villages.

