
# AI-Searching-Algorithms 


## Overview

Search is an integral part of AI. It helps in problem solving across a wide variety of domains where a solution isn’t immediately clear.  You will implement several graph search algorithms with the goal of solving bi-directional search. Your task is to implement several informed search algorithms that will calculate a driving route between two points in Romania with a minimal time and space cost.



## Resources

* [R&N slides on Uninformed Search](https://www.cc.gatech.edu/~thad/6601-gradAI-fall2015/chapter03-clean.pdf)
* [Informed Search](https://www.cc.gatech.edu/~thad/6601-gradAI-fall2015/chapter04a.pdf)
* [Comparing BFS and DFS](https://cs.stanford.edu/people/abisee/tutorial/bfsdfs.html)
* [A* Search](https://cs.stanford.edu/people/abisee/tutorial/astar.html)


Resources for bi-directional searches
* [A Star meets Graph Theory](https://github.gatech.edu/omscs6601/assignment_1/raw/master/resources/A%20Star%20meets%20Graph%20Theory.pdf)
* [Bi Directional A Star - Slides](https://github.gatech.edu/omscs6601/assignment_1/raw/master/resources/Bi%20Directional%20A%20Star%20-%20Slides.pdf)
* [Bi Directional A Star with Additive Approx Bounds](https://github.gatech.edu/omscs6601/assignment_1/raw/master/resources/Bi%20Directional%20A%20Star%20with%20Additive%20Approx%20Bounds.pdf)
* [Bi Directional A Star](https://github.gatech.edu/omscs6601/assignment_1/raw/master/resources/Bi%20Directional%20A%20Star.pdf)
* [Search Algorithms Slide Deck](https://github.gatech.edu/omscs6601/assignment_1/raw/master/resources/Search%20Algorithms%20Slide%20Deck.pdf)
* [Bi Directional Stopping Conditions, Piazza '17](https://docs.google.com/document/d/14Wr2SeRKDXFGdD-qNrBpXjW8INCGIfiAoJ0UkZaLWto/pub)
* [Bi Directional Search Visualizations](https://docs.google.com/document/d/13ssrkqauVf6Nk696fA0sh-w9EB3iSYwiv25UsAEMqK4/edit?usp=sharing)
* [Piazza: Landmark Example](https://docs.google.com/document/d/1YEptGbSYUtu180MfvmrmA4B6X9ImdI4oOmLaaMRHiCA/pub)


### Warmups
We'll start by implementing some simpler optimization and search algorithms before the real exercises.

#### Warmup 1: Priority queue

_[5 points]_

In all searches that involve calculating path cost or heuristic (e.g. uniform-cost), we have to order our search frontier. It turns out the way that we do this can impact our overall search runtime.

To show this, you'll implement a priority queue which will help you in understanding its performance benefits. For large graphs, sorting all input to a priority queue is impractical. As such, the data structure you implement should have an amortized O(1) insertion and O(lg n) removal time. It should do better than the naive implementation in our tests (InsertionSortQueue), which sorts the entire list after every insertion.

In this implementation of priority queue, if two elements have the same priority, they should be served according to the order in which they were enqueued (see Hint 3).  

> **Notes**:
> 1. Please note that the algorithm runtime is not the focus of this assignment. The already-imported heapq library should achieve the desired runtime.
> 2. The local tests provided are used to test the correctness of your implementation of the Priority Queue. To verify that your implementation consistently beats the naive implementation, you might want to test it with a large number of elements.
> 3. If you use the heapq library, keep in mind that the queue will sort entries as a whole upon being enqueued, not just on the first element. This means you need to figure out a way to keep elements with the same priority in FIFO order.
> 4. You may enqueue nodes however you like, but when your Priority Queue is tested, we feed node in the form (priority, value).

#### Warmup 2: BFS

_[5 pts]_

To get you started with handling graphs, implement and test breadth-first search over the test network.

You'll complete this by writing the `breadth_first_search()` method. This returns a path of nodes from a given start node to a given end node, as a list.

For this part, it is optional to use the PriorityQueue as your frontier. You will require it from the next question onwards. You can use it here too if you want to be consistent.

> **Notes**:
> 1. You need to include start and goal in the path.
> 2. **If your start and goal are the same then just return [].**
> 3. You can access all the neighbors of a given node by calling `graph[node]`, or `graph.neighbors(node)` ONLY. 
> 4. You are not allowed to maintain a cache of the neighbors for any node. You need to use the above mentioned methods to get the neighbors.
> 5. To measure your search performance, the `explorable_graph.py` provided keeps track of which nodes you have accessed in this way (this is referred to as the set of 'Explored' nodes). To retrieve the set of nodes you've explored in this way, call `graph.explored_nodes`. If you wish to perform multiple searches on the same graph instance, call `graph.reset_search()` to clear out the current set of 'Explored' nodes. **WARNING**, these functions are intended for debugging purposes only. Calls to these functions will fail on Gradescope.
> 6. In BFS, make sure you process the neighbors in alphabetical order. Because networkx uses dictionaries, the order that it returns the neighbors is not fixed. This can cause differences in the number of explored nodes from run to run. If you sort the neighbors alphabetically before processing them, you should return the same number of explored nodes each time.
> 7. For BFS only, the autograder requires implementing an optimization trick which fully explores fewer nodes. You may find it useful to re-watch the Canvas videos for this.


#### Warmup 3: Uniform-cost search

_[10 points]_

Implement uniform-cost search, using PriorityQueue as your frontier. From now on, PriorityQueue should be your default frontier.

`uniform_cost_search()` should return the same arguments as breadth-first search: the path to the goal node (as a list of nodes).

> **Notes**:
> 1. You need to include start and goal in the path.
> 2. **If your start and goal are the same then just return [].**
> 3. The above are just to keep your results consistent with our test cases.
> 4. You can access all the neighbors of a given node by calling `graph[node]`, or `graph.neighbors(node)` ONLY. 
> 5. You can access the weight of an edge using: `graph.get_edge_weight(node_1, node_2)`. Not using this method will result in your explored nodes count being higher than it should be.
> 6. You are not allowed to maintain a cache of the neighbors for any node. You need to use the above mentioned methods to get the neighbors and corresponding weights.
> 7. We will provide some margin of error in grading the size of your 'Explored' set, but it should be close to the results provided by our reference implementation.

#### Warmup 4: A* search

_[10 points]_

Implement A* search using Euclidean distance as your heuristic. You'll need to implement `euclidean_dist_heuristic()` then pass that function to `a_star()` as the heuristic parameter. We provide `null_heuristic()` as a baseline heuristic to test against when calling a_star tests.

> **Hint**:
> You can find a node's position by calling the following to check if the key is available: `graph.nodes[n]['pos']`

> **Notes**:
> 1. You need to include start and goal in the path.
> 2. **If your start and goal are the same then just return [].**
> 3. The above are just to keep your results consistent with our test cases.
> 4. You can access all the neighbors of a given node by calling `graph[node]`, or `graph.neighbors(node)` ONLY. 
> 5. You can access the weight of an edge using: `graph.get_edge_weight(node_1, node_2)`. Not using this method will result in your explored nodes count being higher than it should be.
> 6. You are not allowed to maintain a cache of the neighbors for any node. You need to use the above mentioned methods to get the neighbors and corresponding weights.
> 7. You can access the (x, y) position of a node using: `graph.nodes[n]['pos']`. You will need this for calculating the heuristic distance.
> 8. We will provide some margin of error in grading the size of your 'Explored' set, but it should be close to the results provided by our reference implementation.

---
### Exercises
The following exercises will require you to implement several kinds of bidirectional searches. The benefits of these algorithms over uninformed or unidirectional search are more clearly seen on larger graphs. As such, during grading, we will evaluate your performance on the map of Romania included in this assignment.

For these exercises, we recommend you take a look at the resources mentioned earlier.

#### Exercise 1: Bidirectional uniform-cost search

_[20 points]_

Implement bidirectional uniform-cost search. Remember that this requires starting your search at both the start and end states.

`bidirectional_ucs()` should return the path from the start node to the goal node (as a list of nodes).

> **Notes**:
> 1. You need to include start and goal in the path. Make sure the path returned is from start to goal and not in the reverse order.
> 2. **If your start and goal are the same then just return [].**
> 3. The above are just to keep your results consistent with our test cases.
> 4. You can access all the neighbors of a given node by calling `graph[node]`, or `graph.neighbors(node)` ONLY. 
> 5. You can access the weight of an edge using: `graph.get_edge_weight(node_1, node_2)`. Not using this method will result in your explored nodes count being higher than it should be.
> 6. You are not allowed to maintain a cache of the neighbors for any node. You need to use the above mentioned methods to get the neighbors and corresponding weights.
> 7. We will provide some margin of error in grading the size of your 'Explored' set, but it should be close to the results provided by our reference implementation.

#### Exercise 2: Bidirectional A* search

_[29 points]_

Implement bidirectional A* search. Remember that you need to calculate a heuristic for both the start-to-goal search and the goal-to-start search.

To test this function, as well as using the provided tests, you can compare the path computed by bidirectional A* to bidirectional UCS search above.
`bidirectional_a_star()` should return the path from the start node to the goal node, as a list of nodes.

> **Notes**:
> 1. You need to include start and goal in the path.
> 2. **If your start and goal are the same then just return [].**
> 3. The above are just to keep your results consistent with our test cases.
> 4. You can access all the neighbors of a given node by calling `graph[node]`, or `graph.neighbors(node)` ONLY. 
> 5. You can access the weight of an edge using: `graph.get_edge_weight(node_1, node_2)`. Not using this method will result in your explored nodes count being higher than it should be.
> 6. You are not allowed to maintain a cache of the neighbors for any node. You need to use the above mentioned methods to get the neighbors and corresponding weights.
> 7. You can access the (x, y) position of a node using: `graph.nodes[n]['pos']`. You will need this for calculating the heuristic distance.
> 8. We will provide some margin of error in grading the size of your 'Explored' set, but it should be close to the results provided by our reference implementation.

