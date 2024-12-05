# Idk if we even need, but it is on the proposal doc for visuals. 
# Best to probably implement it like an adjacency matrix.

class Graph:
    """
    A graph data structure represented using an adjacency matrix.
    Supports both directed and undirected graphs.

    Attributes:
        num_vertices (int): The number of vertices in the graph.
        is_directed (bool): Indicates whether the graph is directed.
        matrix (list[list[int]]): The adjacency matrix storing edge weights.
    """

    def __init__(self, num_vertices, is_directed=False):
        """
        Initializes a new instance of the Graph class.

        Args:
            num_vertices (int): The number of vertices in the graph.
            is_directed (bool, optional): If True, the graph is directed. Defaults to False.
        """
        self._num_vertices = num_vertices
        self._is_directed = is_directed
        self._matrix = [[0] * num_vertices for _ in range(num_vertices)]

    def add_edge(self, src, dest, weight=1):
        """
        Adds an edge to the graph.

        Args:
            src (int): The source vertex.
            dest (int): The destination vertex.
            weight (int, optional): The weight of the edge. Defaults to 1.
        
        Raises:
            ValueError: If src or dest is out of bounds.
        """
        if not (0 <= src < self._num_vertices and 0 <= dest < self._num_vertices):
            raise ValueError("Source and destination vertices must be within bounds.")
        
        self._matrix[src][dest] = weight
        if not self._is_directed:
            self._matrix[dest][src] = weight

    def remove_edge(self, src, dest):
        """
        Removes an edge from the graph.

        Args:
            src (int): The source vertex.
            dest (int): The destination vertex.
        
        Raises:
            ValueError: If src or dest is out of bounds.
        """
        if not (0 <= src < self._num_vertices and 0 <= dest < self._num_vertices):
            raise ValueError("Source and destination vertices must be within bounds.")
        
        self._matrix[src][dest] = 0
        if not self._is_directed:
            self._matrix[dest][src] = 0

    def get_neighbors(self, vertex):
        """
        Returns the neighbors of a given vertex.

        Args:
            vertex (int): The vertex whose neighbors are to be returned.

        Returns:
            list[tuple[int, int]]: A list of tuples representing neighbors 
            and their edge weights (neighbor, weight).
        
        Raises:
            ValueError: If vertex is out of bounds.
        """
        if not (0 <= vertex < self._num_vertices):
            raise ValueError("Vertex must be within bounds.")
        
        neighbors = []
        for i in range(self._num_vertices):
            if self._matrix[vertex][i] != 0:
                neighbors.append((i, self._matrix[vertex][i]))
        
        return neighbors

    def display(self):
        """
        Displays the adjacency matrix of the graph.
        """
        for row in self._matrix:
            print(" ".join(map(str, row)))

    def has_edge(self, src, dest):
        """
        Checks if there is an edge between two vertices.

        Args:
            src (int): The source vertex.
            dest (int): The destination vertex.

        Returns:
            bool: True if there is an edge, False otherwise.

        Raises:
            ValueError: If src or dest is out of bounds.
        """
        if not (0 <= src < self._num_vertices and 0 <= dest < self._num_vertices):
            raise ValueError("Source and destination vertices must be within bounds.")
        
        return self._matrix[src][dest] != 0

    def size(self):
        """
        Returns the number of vertices in the graph.

        Returns:
            int: The number of vertices.
        """
        return self._num_vertices