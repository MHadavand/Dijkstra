from __future__ import absolute_import, division, print_function
import collections as CS

__author__ = 'Mosatafa Hadavand'
__date__ = 'April 2017'
__version__ = '1.000'


class Dijkstra:

    '''
    This is a class to implement dijkstra algorithm 
    '''
    
    def __init__(self  ):
        self.Nodes = set()
        self.Edges = CS.defaultdict(list)
        self.Distances = {}

    def AddNode(self, value):
        self.Nodes.add(value)

    def AddEdge(self, From, To, distance):
        self.Edges[From].append(To)
        self.Edges[To].append(From)
        self.Distances[(From, To)] = distance
        self.Distances[(To,From)] = distance


    def Find_Path(self,initial):

        visited = {initial: 0}
        path = {}
        Path_All=CS.defaultdict(list)
        Path_All[initial].append(initial)


        # Sort unvisted Nodes
        #--------------------------
        unvisited = set(self.Nodes)

        while unvisited:

            min_node = None
            # Identifying the node with minmum distance in current loop
            for node in unvisited:
                if node in visited:
                    if min_node is None:
                        min_node = node
                    elif visited[node] < visited[min_node]:
                        min_node = node

            if min_node is None:
                break

            unvisited.remove(min_node)
            Current_Dist = visited[min_node]

            # Calculating the distance for each unvisted node or replace 
            # the visited node distance if a shorter distance is found
            for edge in self.Edges[min_node]:
                weight = Current_Dist + self.Distances[(min_node, edge)]
                if edge not in visited or weight < visited[edge]:
                    visited[edge] = weight
                    path[edge] = min_node

        

        for node in path:
            Path_All[node].append(node)
            Connection=path[node]
            Path_All[node].append(Connection)
            while Connection is not initial:
                Connection=path[Connection]
                Path_All[node].append(Connection)

        self.Path_All=Path_All

        return visited, path, Path_All


    def Path_Plot(self, Nodes_All, Node, Path_All=None, figsize=(10,10), Offset=[8,8], Grid=True,
              Xlabel='X (m)', Ylabel='Y(m)', lw=3, Arrow_width=20,Arrow_length=10,
              ax=None):
    
        '''
            A post-processing function to plot the results of Dijkstra algorithm
            
            Parameters:
            Nodes_All (defaultdict with list arguments):  Contains each point lable and the corresponding
            Node (str): The node from which the shortest path is considered to the target node
            
            X and Y Coordinates
            figsize (tuple): Figure size (width, height)
            ax (mpl.axis): Existing matplotlib axis to plot the figure onto
            Offset (list): Offset to plot name of each node
            Path_All (defaultdict with list arguments): Report of the shortest path for each point
            Grid (bool): Add grid to the plot
            lw(float): line width for the plot

        '''
        
        import matplotlib.pyplot as plt
        

        if Path_All is None:
            Path_All=self.Path_All
        
        for i, node in enumerate(Nodes_All):
            if node not in Path_All:
                string='The node %s is in the original list but not in the Dijkstra path!'%node
                raise ValueError(string)
                
        if Node not in Path_All:
            raise ValueError('The specified Node is not in the provide Dijkstra path dictionary!')
        
        if ax is None:
            fig, ax = plt.subplots(1, figsize=figsize)          
        
        
        if (len(Path_All[Node])>1):
            for i in range (len(Path_All[Node])-1):
                node1=Path_All[Node][i]
                node2=Path_All[Node][i+1]
                ax.plot([Nodes_All[node1][0],Nodes_All[node2][0]],
                    [Nodes_All[node1][1],Nodes_All[node2][1]],c='k',lw=lw)
                dx=Nodes_All[node2][0]-Nodes_All[node1][0]
                dy=Nodes_All[node2][1]-Nodes_All[node1][1]
                ax.arrow(Nodes_All[node1][0]+dx/2, Nodes_All[node1][1]+dy/2, dx*0.01, dy*0.01, head_width=Arrow_width,  fc='k', ec='k',
                         head_length=Arrow_length, shape='full', lw=1, length_includes_head=True)

        for i, node in enumerate(Nodes_All):
            ax.scatter(Nodes_All[node][0],Nodes_All[node][1], s=300,c='r',edgecolor='k')
            ax.annotate(node, xy=(Nodes_All[node][0]+Offset[0], Nodes_All[node][1]+Offset[1]),color='b')

        if Grid:
            ax.grid(axis='both')
        ax.set_xlabel(Xlabel)
        ax.set_ylabel(Ylabel)   
