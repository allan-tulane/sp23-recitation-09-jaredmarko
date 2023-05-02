from collections import deque
from heapq import heappush, heappop 

def shortest_shortest_path(graph, source):
    """
    Params: 
      graph.....a graph represented as a dict where each key is a vertex
                and the value is a set of (vertex, weight) tuples (as in the test case)
      source....the source node
      
    Returns:
      a dict where each key is a vertex and the value is a tuple of
      (shortest path weight, shortest path number of edges). See test case for example.
    """
    # Initialize S and U.
    S = set([source])
    U = set(graph.keys()) - S

    # Initialize D.
    D = {}
    for v in graph:
        D[v] = (float("inf"), float("inf"))
    D[source] = (0, 0)

    # While U is not empty:
    while U:
        # Let v be the vertex in U with the smallest value of D[v][0].
        v = min(U, key=lambda x: D[x][0])

        # Remove v from U.
        U.remove(v)

        # For each neighbor w of v:
        for w in graph[v]:
            # If D[w][0] is greater than D[v][0] + w:
            if D[w][0] > D[v][0] + w:
                # Update D[w][0] to D[v][0] + w.
                D[w][0] = D[v][0] + w
                # Update D[w][1] to D[v][1] + 1.
                D[w][1] = D[v][1] + 1

    # Return D.
    return D

    
def test_shortest_shortest_path():

    graph = {
                's': {('a', 1), ('c', 4)},
                'a': {('b', 2)}, # 'a': {'b'},
                'b': {('c', 1), ('d', 4)}, 
                'c': {('d', 3)},
                'd': {},
                'e': {('d', 0)}
            }
    result = shortest_shortest_path(graph, 's')
    # result has both the weight and number of edges in the shortest shortest path
    assert result['s'] == (0,0)
    assert result['a'] == (1,1)
    assert result['b'] == (3,2)
    assert result['c'] == (4,1)
    assert result['d'] == (7,2)
    
    
def bfs_path(graph, source):
    """
    Returns:
      a dict where each key is a vertex and the value is the parent of 
      that vertex in the shortest path tree.
    """
    # Initialize a queue and a set.
    queue = [source]
    visited = set([source])

    # Initialize a dictionary to store the parent of each vertex.
    parent = {}
    for v in graph:
        parent[v] = None

    # While the queue is not empty:
    while queue:
        # Let v be the vertex at the front of the queue.
        v = queue.pop(0)

        # For each neighbor w of v:
        for w in graph[v]:
            # If w is not visited:
            if w not in visited:
                # Mark w as visited.
                visited.add(w)

                # Add w to the queue.
                queue.append(w)

                # Set the parent of w to v.
                parent[w] = v

    # Return the dictionary parent.
    return parent

def get_sample_graph():
     return {'s': {'a', 'b'},
            'a': {'b'},
            'b': {'c'},
            'c': {'a', 'd'},
            'd': {}
            }

def test_bfs_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    assert parents['a'] == 's'
    assert parents['b'] == 's'    
    assert parents['c'] == 'b'
    assert parents['d'] == 'c'
    
def get_path(parents, destination):
    """
    Returns:
      The shortest path from the source node to this destination node 
      (excluding the destination node itself). See test_get_path for an example.
    """
    # Initialize a list to store the path.
    path = []

    # Start at the destination node.
    v = destination

    # While v is not the source node:
    while v != parents[v]:
        # Add v's parent to the path.
        path.append(v)

        # Set v to v's parent.
        v = parents[v]

    # Reverse the path.
    path.reverse()

    # Return the path.
    return path

def test_get_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    assert get_path(parents, 'd') == 'sbc'
