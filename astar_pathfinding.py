from heapq import *


class PathFinding:
    def __init__(self, game):
        self.game = game
        self.map = game.map.mini_map
        self.graph = {}
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        self.get_graph()

    def get_path(self, start, goal):
        # Requests the cheapest path from start to goal from a_star() function
        self.visited = self.a_star(start, goal, self.graph)
        # Creates a list starting from the goal
        path = [goal]
        # Creates another list of coordinates from the populated dictionary
        step = self.visited.get(goal, start)

        # Iterates through the steps until it reaches the start, omitting the start from the list
        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1]  # Returns the neighbor node to move to until it reaches the goal

    def a_star(self, start, goal, graph):
        open_list = []
        # Places the starting node into open_list using a heap to manage its priority
        heappush(open_list, (0, start))
        cost_visited = {start: 0}
        visited = {start: None}

        # Loop iterates until open_list is empty
        while open_list:
            # Removes from open and saves values to cur_cost and cur_node
            cur_cost, cur_node = heappop(open_list)
            # If cur_node is the goal, clears the open_list and exits with success
            if cur_node == goal:
                open_list = []
                continue

            # Obtains neighbor nodes to the current node and their costs from map graph
            next_nodes = graph[cur_node]
            # Iterates through each neighbor node
            for next_node in next_nodes:
                # Sets two variables for the node to examine
                neighbor_cost, neighbor = next_node
                # Calculates the new cost for traveling to the examined node
                new_cost = cost_visited[cur_node] + neighbor_cost

                # If the neighbor node has not been visited before or the new cost is smaller than
                # the previous neighbor node, it gives that node higher priority and saves it to the visited
                # node list
                if neighbor not in cost_visited or new_cost < cost_visited[neighbor]:
                    priority = new_cost + self.heuristic(neighbor, goal)
                    heappush(open_list, (priority, neighbor))
                    cost_visited[neighbor] = new_cost
                    visited[neighbor] = cur_node
                # Continues iterating through the lists until only the cheapest node path remains

        return visited  # Returns the visited path to the get_path() function

    def heuristic(self, a, b):  # Manhattan Distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def check_next_node(self, x, y):
        if 0 <= x < 19 and 0 <= y < 22:
            return True
        else:
            return False

    def get_next_nodes(self, x, y):
        """ Function returns neighbors cells and their movement cost """
        return [(self.game.map.world_map[(x, y)], (x + dx, y + dy))
                for dx, dy in self.ways if self.check_next_node(x + dx, y + dy)]

    def get_graph(self):
        """ Function generates the node neighbor graph from map """
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)
