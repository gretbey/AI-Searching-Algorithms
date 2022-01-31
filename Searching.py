# coding=utf-8

import heapq
import math


class PriorityQueue(object):
    """
    A queue structure where each element is served in order of priority,
    implemented with heapq module.
    Elements in the queue are popped based on the priority with higher priority
    elements being served before lower priority elements.  If two elements have
    the same priority, they will be served in the order they were added to the
    queue.
    Attributes: queue (list): Nodes added to the priority queue.
    """

    def __init__(self):
        self.queue = []
        self.index = 0

    def pop(self):
        """
        Pop top priority node from queue.
        Returns: The node with the highest priority.
        """
        return heapq.heappop(self.queue)[-1]

    def remove(self, node):
        """Remove a node from the queue."""
        self.queue.pop(node)
        heapq.heapify(self.queue)

    def append(self, node):
        """Append a node to the queue."""
        heapq.heappush(self.queue, (node[0], self.index, node))
        self.index += 1

    def size(self):
        """
        Get the current size of the queue.
        Returns: Integer of number of items in queue.
        """
        return len(self.queue)

    def clear(self):
        """Reset queue to empty (no nodes)."""
        self.queue = []

    def top(self):
        """
        Get the top item in the queue.
        Returns: The first item stored in the queue.
        """
        return self.queue[0] if self.queue else [0]

    def __iter__(self):
        """Queue iterator."""
        return iter(sorted(self.queue))

    def __str__(self):
        """Priority Queue to string."""
        return 'PQ:%s' % self.queue

    def __contains__(self, key):
        """
        Containment Check operator for 'in'
        Args: key: The key to check for in the queue.
        Returns: True if key is found in queue, False otherwise.
        """
        return key in [n[-1] for n in self.queue]

    def __eq__(self, other):
        """
        Compare this Priority Queue with another Priority Queue.
        Args: other (PriorityQueue): Priority Queue to compare against.
        Returns: True if the two priority queues are equivalent.
        """
        return self.queue == other.queue


def breadth_first_search(graph, start, goal):
    """
    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start (str): Key for the start node.
        goal (str): Key for the end node.
    Returns:
        The best path as a list from the start and goal nodes (including both).
    """
    if start == goal:
        return []

    frontier = [start] # node
    explored = []
    path = {start: [start]}
    while len(frontier) > 0:
        current = frontier.pop(0)
        explored.append(current)
        children = sorted(graph[current])
        for child in children:
            if (child not in frontier) and (child not in explored):
                path[child] = path[current] + [child]
                if child == goal:
                    return path[goal]
                frontier.append(child)


def uniform_cost_search(graph, start, goal):
    """
    Dijkstra's Algorithm
    Returns: The best path as a list from the start and goal nodes (including both).
    """
    if start == goal:
        return []

    frontier = PriorityQueue()
    frontier.append((0, start)) # cost, node
    explored = []
    path = {start: [start]}
    weights = {start: 0}

    while frontier.size() > 0:
        cost, curr_node = frontier.pop()
        if curr_node == goal:
            return path[goal]
        explored.append(curr_node)
        weights[curr_node] = cost
        children = graph[curr_node]
        for child in children:
            if (child not in explored) and (child not in frontier):
                weight = graph.get_edge_weight(curr_node, child)
                new_cost = weight + cost
                min_cost = float('inf')
                if weights.get(child, min_cost) > new_cost:
                    weights[child] = new_cost
                    path[child] = path[curr_node] + [child]
                    frontier.append((new_cost, child))


def null_heuristic(graph, v, goal):
    """
    Null heuristic used as a base line..
    Returns: 0
    """
    return 0


def euclidean_dist_heuristic(graph, v, goal):
    """
    Returns: Euclidean distance between `v` node and `goal` node
    """
    x1, y1 = graph.nodes[v]['pos']
    x2, y2 = graph.nodes[goal]['pos']
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def a_star(graph, start, goal, heuristic=euclidean_dist_heuristic):
    """
    A* Algorithm: f(n) = g(n) + h(n)
    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start (str): Key for the start node.
        goal (str): Key for the end node.
        heuristic: Function to determine distance heuristic.
            Default: euclidean_dist_heuristic.
    Returns:
        The best path as a list from the start and goal nodes (including both).
    """
    if start == goal:
        return []

    frontier = PriorityQueue()
    # f = g + h, g is actual cost, h is estimated cost
    frontier.append((0 + heuristic(graph, start, goal), 0, start)) # f, g, node
    explored = []
    path = {start: [start]}
    weights = {start: 0}

    while frontier.size() > 0:
        f, g, curr_node = frontier.pop()
        if curr_node == goal:
            return path[goal]
        explored.append(curr_node)
        weights[curr_node] = f
        children = graph[curr_node]
        for child in children:
            if (child not in explored) and (child not in frontier):
                weight = graph.get_edge_weight(curr_node, child)
                new_g = weight + g
                new_h = heuristic(graph, child, goal)
                new_f = new_g + new_h
                min_cost = float('inf')
                if weights.get(child, min_cost) > new_f:
                    weights[child] = new_f
                    path[child] = path[curr_node] + [child]
                    frontier.append((new_f, new_g, child))


def bidirectional_ucs(graph, start, goal):
    """
    Bidirectional uniform-cost-search
    Returns: The best path as a list from the start and goal nodes (including both).
    """
    if start == goal:
        return []

    frontier1, frontier2 = PriorityQueue(), PriorityQueue()
    frontier1.append((0, start))  # cost, start_node: from start to goal
    frontier2.append((0, goal))  # cost, goal_node: from goal to start
    explored1, explored2 = [], []
    path1, path2 = {start: []}, {goal: []}
    weights1, weights2 = {start: 0}, {goal: 0}
    best_path = []
    mu = float('inf') # leaset path length from start to goal

    while frontier1.size() > 0 and frontier2.size() > 0:
        cost1, node1 = frontier1.pop()
        cost2, node2 = frontier2.pop()
        weights1[node1], weights2[node2] = cost1, cost2
        explored1.append(node1)
        explored2.append(node2)

        if node1 in path2.keys() and weights1[node1] + weights2[node1] < mu:
            best_path = path1[node1] + [node1] + path2[node1]
            mu = weights1[node1] + weights2[node1]
        for child in graph[node1]:
            if child not in explored1:
                weight1 = graph.get_edge_weight(node1, child)
                if weights1.get(child, float('inf')) > weight1 + cost1:
                    weights1[child] = weight1 + cost1
                    path1[child] = path1[node1] + [node1]
                    frontier1.append((weight1 + cost1, child))

        if node2 in path1.keys() and weights1[node2] + weights2[node2] < mu:
            best_path = path1[node2] + [node2] + path2[node2]
            mu = weights1[node2] + weights2[node2]
        for child in graph[node2]:
            if child not in explored2:
                weight2 = graph.get_edge_weight(node2, child)
                if weights2.get(child, float('inf')) > weight2 + cost2:
                    weights2[child] = weight2 + cost2
                    path2[child] = [node2] + path2[node2]
                    frontier2.append((weight2 + cost2, child))

        top1, top2 = frontier1.top()[0], frontier2.top()[0]
        if top1 + top2 >= mu:
            return best_path


def bidirectional_a_star(graph, start, goal, heuristic=euclidean_dist_heuristic):
    """
    Bidirectional A*
    Returns: The best path as a list from the start and goal nodes (including both).
    """
    if start == goal:
        return []

    frontier1, frontier2 = PriorityQueue(), PriorityQueue()
    frontier1.append((0, 0, start))  # f, g, start_node: from start to goal
    frontier2.append((0, 0, goal))  # f, g, goal_node: from goal to start
    explored1, explored2 = [], []
    path1, path2 = {start: []}, {goal: []}
    weights1, weights2 = {start: 0}, {goal: 0}
    best_path = []
    mu = float('inf') # leaset path length from start to goal

    while frontier1.size() > 0 and frontier2.size() > 0:
        f1, g1, node1 = frontier1.pop()
        f2, g2, node2 = frontier2.pop()
        explored1.append(node1)
        explored2.append(node2)

        if node1 in path2.keys() and weights1[node1] + weights2[node1] < mu:
            best_path = path1[node1] + [node1] + path2[node1]
            mu = weights1[node1] + weights2[node1]
        for child in graph[node1]:
            if child not in explored1:
                weight1 = graph.get_edge_weight(node1, child)
                new_g1 = weight1 + g1
                new_h1 = heuristic(graph, child, goal)
                new_f1 = new_g1 + new_h1
                if weights1.get(child, float('inf')) > new_f1:
                    weights1[child] = new_f1
                    path1[child] = path1[node1] + [node1]
                    frontier1.append((new_f1, new_g1, child))

        if node2 in path1.keys() and weights1[node2] + weights2[node2] < mu:
            best_path = path1[node2] + [node2] + path2[node2]
            mu = weights1[node2] + weights2[node2]
        for child in graph[node2]:
            if child not in explored2:
                weight2 = graph.get_edge_weight(node2, child)
                new_g2 = weight2 + g2
                new_h2 = heuristic(graph, child, start)
                new_f2 = new_g2 + new_h2
                if weights2.get(child, float('inf')) > new_f2:
                    weights2[child] = new_f2
                    path2[child] = [node2] + path2[node2]
                    frontier2.append((new_f2, new_g2, child))

        top1, top2 = frontier1.top()[0], frontier2.top()[0]
        if top1 + top2 >= mu:
            return best_path
        