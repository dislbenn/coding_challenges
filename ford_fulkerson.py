#!/usr/bin/python2.7
"""Ford Fulkerson Algorithm
    Longest Path: Find the longest path from the source node to the sink node.
"""
import os
from random import choice # Used for selecting edge path in the path finder.
import networkx as nx # Used for directed graph.
import matplotlib.pyplot as plt # Used to plot the graph.

class Graph:
    """Graph containing the nodes and edges.
    """
    def __init__(self, graph=None, pos=None, source=None, sink=None):
        """Graph Class
            Param
                graph: None - Type of graph the class object will be assigned.
                pos: None - Position of the nodes in the image of the graph.
        """
        # If graph is None, the graph will be set to the default graph value.
        self.graph = nx.DiGraph() if graph is None else graph

        # If pos is None, the node's position will be set to the default pos value.
        self.pos = {
            'S': [0, 1], 'A': [1, 2], 'B': [1, 0],
            'C': [2, 2], 'D': [2, 0], 'T': [3, 1],
        } if pos is None else pos

        self.source = 'S' if source is None else source # Set the source node to S
        self.sink = 'T' if sink is None else sink # Set the sink node to T

        self.val = {}

    def add_sample_nodes_edges(self):
        """Adding Sample Nodes & Edges.
            Return:
                True: bool - Success when adding nodes & edges.
                False: bool - Error when adding nodes & edges.
            Example:
                >>> graph = Graph()
                >>> graph.add_sample_nodes_edges()
        """
        # Default sample node edges
        try:
            self.graph.add_edges_from([("S", "A", {'capacity': 9, 'flow': 0, 'residual':9}),
                                       ("S", "B", {'capacity': 9, 'flow': 0, 'residual':9}),
                                       ("A", "B", {'capacity': 10, 'flow': 0, 'residual':10}),
                                       ("A", "C", {'capacity': 8, 'flow': 0, 'residual':8}),
                                       ("B", "C", {'capacity': 1, 'flow': 0, 'residual':1}),
                                       ("B", "D", {'capacity': 3, 'flow': 0, 'residual':3}),
                                       ("C", "T", {'capacity': 10, 'flow': 0, 'residual':10}),
                                       ("D", "C", {'capacity': 8, 'flow': 0, 'residual':8}),
                                       ("D", "T", {'capacity': 7, 'flow': 0, 'residual':7})
                                       ])
        except TypeError as error:
            print(error)
            return False
        return True

    def display(self):
        """Display a graph of the nodes with it's connected edge(s).
            Example:
                >>> graph = Graph()
                >>> plt = graph.display()
        """

        # Get the color values for the nodes
        _ = self.graph.number_of_nodes()
        node_colors = range(2, _ + 2)

        # Set the size of the image to be displayed
        plt.figure(figsize=(8, 4))
        plt.axis('off')

        # Draw the nodes
        nx.draw_networkx_nodes(self.graph, self.pos, node_color=node_colors, node_size=600)

        # Draw the edges that are linking the nodes
        nx.draw_networkx_edges(self.graph, self.pos, edge_color='gray', width=3)

        # Draw the nodes label
        nx.draw_networkx_labels(self.graph, self.pos, font_color='white')

        for u, v, edge in self.graph.edges(data=True):
            label = "%d/%d" % (edge['flow'], edge['capacity']) # labels for each
            color = 'green' if edge['flow'] < edge['capacity'] else 'red'
            x = self.pos[u][0] * .6 + self.pos[v][0] * .4
            y = self.pos[u][1] * .6 + self.pos[v][1] * .4
            t = plt.text(x, y, label, size=16, color=color,
                         horizontalalignment='center', verticalalignment='center')

        i = 0
        while os.path.exists("sample_%d.png" % i):
            i += 1
        
        plt.savefig("sample_%d.png" % i) # save the displaying figure as a png file
        plt.show() # display the plot data

class FordFulkerson:
    """Ford Fulkerson Class
    """
    def __init__(self, graph=None):
        """Ford Fulkerson Class Attributes
            Param
                graph: None - Type of graph the class object will be assigned.
            Features
                nodes: List - list of nodes being used in the graph.
                source: String - source node.
                sink: String - sink node.
                edges: List - edge connecting a target and destination node.
                visited: List - list of node paths that were visited during the path finder.
                path: String - the path that was found from the path finder.
                retry: int - number of time to retry the path finder.
        """
        self.graph = graph if graph else None
        self.nodes = graph.graph.nodes if graph else None # Graph Nodes
        self.source = graph.source if graph else None # Source Node
        self.sink = graph.sink if graph else None # Sink Node
        self.edges = graph.graph.edges if graph else None # Graph Edges

        self.visited = [] # Visited Path List
        self.path = "" # Path String

        self.retry = 30 # Retry Logic

    def path_finder(self, source, sink):
        """Path Finder
        """
        if not source or not sink:
            print("[\033[1;31mERROR\033[0m] Source or Sink is missing within FordFulkerson class!")
            exit()

        self.path += "".join(source) # Store source node 'S'
        while self.retry > 0 and source != sink and len(self.visited) != 7: # While the source is not equal to sink
            try: # Returns edges with the source in them
                possible = [edge for edge in self.edges if source in edge[0]]
                test = choice(possible) # Select an edge from the return list
                source = test[1]

                if source == sink: # If you have reached the end
                    self.path += "".join(source) # Add final node

                    if self.path not in self.visited: # If this path has not been visited then add.
                        print(u'[\u2713]\033[1;32m Found\033[0m: \033[1;35m%s\033[0m' % self.path)
                        self.visited.append(self.path)
                        print(self, "\n")

                    self.path = "" # Reset the path
                    self.path_finder(self.source, self.sink) # Recurssion

                self.path += "".join(source)

            except IndexError:
                break

    def flow_network(self):
        visit = {}
        maxflow = []
        filled = []

        for path in self.visited:
            visit[path] = []
            for i, node in enumerate(path):
                if path[i] == path[-1]:
                    break
                else:
                    visit[path].append((path[i], path[i+1]))

        for path in visit:
            residual_capacity = 0 # Reset residual capacity
            r_edges = []

            for node in visit[path]:
                temp = [edge for edge in self.edges(data=True) if node[0] in edge and node[1] in edge]
                r_edges.append(temp)

                if residual_capacity == 0:
                    residual_capacity = temp[0][2]['capacity']

                elif residual_capacity > temp[0][2]['capacity']:
                    residual_capacity = temp[0][2]['capacity']
                    _ = (temp[0][0], temp[0][1])

                else:
                    pass

            print("Checking current path: ", path)
            print("Residual Capacity: %d\n" % residual_capacity)

            if residual_capacity not in maxflow:
                maxflow.append(residual_capacity)

            else:
                print("[\033[1;31mFULL\033[0m] Edge: ", _, "is already full\n")
                continue

            for edge in r_edges:
                if edge[0][2]['flow'] != edge[0][2]['capacity'] : # If the edge can stil receive
                    if edge[0][2]['flow'] + residual_capacity > edge[0][2]['capacity']:
                        print("Ill over flow!")
                        break
                    else:
                        edge[0][2]['flow'] += residual_capacity
                        print("Added residual capacity to the edge flow", edge)
                        edge[0][2]['residual'] -= residual_capacity
                        print("Subtracting residual capacity from remaining residual", edge, "\n")
                else:
                    break

                if edge[0][2]['capacity'] == edge[0][2]['flow']:
                    print("[\033[1;31mFULL\033[0m] - Edge:(%s, %s)\n" % (edge[0][0], edge[0][1]))

            self.graph.display()
        print(sum(maxflow))

    def __str__(self):
        output = []
        for node in self.visited[len(self.visited)-1]:
            output.append(node)
        return " -> ".join(output)

def main():
    """Implementation of the Ford Fulkerson Algorithm
    """
    graph = Graph() # Create graph object

    if graph.add_sample_nodes_edges(): # Adding Sample Data
        print("[\033[1;32mSUCCESS\033[0m] - Sample Node Added: ", graph.graph.nodes())
        print("[\033[1;32mSUCCESS\033[0m] - Sample Edges Added: ", graph.graph.edges(), "\n")

    else: # Exit the program if sample data could not be loaded.
        print("[\033[1;31mFAILED\033[0m] - Sample Data Failed To Be Added")
        exit()

    graph.display() # Display the graph

    ford = FordFulkerson(graph) # Passing graph class object to the ford fulkerson class
    ford.path_finder(ford.source, ford.sink)
    print("Path Found: ", ford.visited, "\n")

    ford.flow_network()

    try:
        path = os.getcwd()
        path += "".join("/images")
        
        if os.path.isdir(path):
            os.system("mv *.png %s" % path)
        else:
            os.mkdir(path)
            os.system("mv *.png %s" % path)

    except FileNotFoundError as error:
        print(error)

if __name__ == "__main__":
    main()
