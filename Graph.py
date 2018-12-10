class Graph:
    """ Class represents a graph for Dijkstra pathfinding """

    # Utility function that looks for the lowest cost from the nodes in the queue
    def minDistance(self, dist, queue):
        minimum = float("Inf")  # Set minimum distance to infinity before we begin as they are all max distances
        min_index = -1          # Set minimum index to -1 before we begin

        # From the nodelist, identify which has the lowest cost and is still available
        for i in range(len(dist)):
            if dist[i] < minimum and i in queue:
                minimum = dist[i]
                min_index = i
        return min_index

    # Function that finds shortest path for given graph from source
    def dijkstra(self, graph, src, dest):

        row = len(graph)                # Get number of rows
        col = len(graph[0])             # Get number of columns
        currentpath = list()            # Stores the path to the destination
        dist = [float("Inf")] * row     # Result array for shortest distances; initialized to infinite
        parent = [-1] * row             # Parent array stores shortest path tree
        dist[src] = 0                   # Distance of source vertex from itself is always 0
        currentpath.append(dist[src])   # Source is always the first item added

        # Add all nodes from the graph into the queue
        queue = []
        for i in range(row):
            queue.append(i)

        # While there are nodes that we have not yet visited
        while queue:

            # Pick the node with the lowest cost from the nodes still in the queue
            u = self.minDistance(dist, queue)

            # If we are back at -1 we have visited all of the nodes, therefore break out of hte loop
            if u == -1:
                break

            queue.remove(u) # Remove this element from the queue as it has now been visited

            # Update result array value and parent index of the adjacent nodes of
            # the node that was picked (only looking at nodes still in the queue)
            for i in range(col):
                # If the node is still in the queue
                if graph[u][i] and i in queue:
                    # If the total cost of the graph with the new node is shorter
                    # than what ewe had previously
                    if dist[u] + graph[u][i] < dist[i]:
                        dist[i] = dist[u] + graph[u][i]
                        parent[i] = u
                        currentpath.append(i)
                # If we are at our destination, break from the loop
                if i == dest:
                    break

        #print("path: ", currentpath)
        return currentpath

    def convertpath(self, resultpath, nodearray):
        pathinnodes = list()
        for item in resultpath:
            pathinnodes.append(nodearray[item])

        return pathinnodes