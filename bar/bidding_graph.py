import random
import time
from collections import defaultdict

import pandas as pd
import datetime
import timeit
import networkx as nx

# GLOBAL VARIABLE
edges = []
nodes = []
G = nx.DiGraph()
class BiddingNode:
    def __init__(self, ID, pickup_time, delivery_time, price, source_location, destination_location, isSource, isTarget,
                 segment, distance_to_target):
        self.ID = ID
        self.pickup_time = pickup_time
        self.delivery_time = delivery_time
        self.price = price
        self.source_location = source_location
        self.destination_location = destination_location
        self.isSource = isSource
        self.isTarget = isTarget
        self.neighbors = []
        self.segment = segment
        self.distance_to_target = distance_to_target

    def addNeighbors(self, neighbor):
        self.neighbors.append(neighbor)

    def getNeighborsByID(self):
        negID = []
        for neg in self.neighbors:
            negID.append(neg.ID)
        return negID


def create_nodes(bidding):
    nodes_by_source = defaultdict(list)  # Dictionary to store nodes by source_location
    for index, row in bidding.iterrows():
        node = BiddingNode(row["carrier id"], row['pickup time'], row['delivery time'], row["price"], row["origin"],
                           row["dest"], row["source?"], row["target?"], row['Segment'],row['distance_to_target'])
        nodes.append(node)
        nodes_by_source[node.source_location].append(node)  # Add node to the list corresponding to its source_location
        # Add the node to the graph
        G.add_node(node.ID)
        G.nodes[node.ID]['ID'] = node.ID
        G.nodes[node.ID]['pickup_time'] = node.pickup_time
        G.nodes[node.ID]['delivery_time'] = node.delivery_time
        G.nodes[node.ID]['price'] = node.price
        G.nodes[node.ID]['source_location'] = node.source_location
        G.nodes[node.ID]['destination_location'] = node.destination_location
        G.nodes[node.ID]['isSource'] = node.isSource
        G.nodes[node.ID]['isTarget'] = node.isTarget
        G.nodes[node.ID]['segment'] = node.segment
        G.nodes[node.ID]['distance_to_target'] = node.distance_to_target

    node = BiddingNode('start', '00:00:00', '00:00:00', 0, 'start', 'start', False, False, 'start',0)
    nodes.append(node)
    nodes_by_source[node.source_location].append(node)
    G.add_node(node.ID)
    G.nodes[node.ID]['ID'] = node.ID
    G.nodes[node.ID]['pickup_time'] = node.pickup_time
    G.nodes[node.ID]['delivery_time'] = node.delivery_time
    G.nodes[node.ID]['price'] = node.price
    G.nodes[node.ID]['source_location'] = node.source_location
    G.nodes[node.ID]['destination_location'] = node.destination_location
    G.nodes[node.ID]['isSource'] = node.isSource
    G.nodes[node.ID]['isTarget'] = node.isTarget
    G.nodes[node.ID]['segment'] = node.segment
    G.nodes[node.ID]['distance_to_target'] = node.distance_to_target
    
    node = BiddingNode('target', '00:00:00', '00:00:00', 0, 'target', 'target', False, False, 'target',0)
    nodes_by_source[node.source_location].append(node)
    nodes.append(node)
    G.add_node(node.ID)
    G.nodes[node.ID]['ID'] = node.ID
    G.nodes[node.ID]['pickup_time'] = node.pickup_time
    G.nodes[node.ID]['delivery_time'] = node.delivery_time
    G.nodes[node.ID]['price'] = node.price
    G.nodes[node.ID]['source_location'] = node.source_location
    G.nodes[node.ID]['destination_location'] = node.destination_location
    G.nodes[node.ID]['isSource'] = node.isSource
    G.nodes[node.ID]['isTarget'] = node.isTarget
    G.nodes[node.ID]['segment'] = node.segment
    G.nodes[node.ID]['distance_to_target'] = node.distance_to_target

    return nodes_by_source
    
def create_edges(bidding):
    for index, row in bidding.iterrows():
        for index, row2 in bidding.iterrows():
            if row["dest"] == row2["origin"] and row["delivery time"] <= row2["pickup time"]:
                edges.append((row["carrier id"], row2["carrier id"]))
                G.add_edge(row["carrier id"], row2["carrier id"])
    for node in nodes:
        # add edges from the dummy node 'start' to all sources nodes
        if node.isSource:
            edges.append(('start', node.ID, node.price))
            G.add_edge('start', node.ID)
        # add edges from the dummy node 'target' to all target nodes
        if node.isTarget:
            edges.append([node.ID, 'target', 0])
            G.add_edge(node.ID, 'target')


def create_bidding_graph(bidding):

    nodes_by_source = create_nodes(bidding)
    create_edges(bidding)

    #add nneighbors to each node
    n = {node.ID: node for node in nodes}

    # add neighbors to all nodes
    for e in edges:
        if e[1] not in n[e[0]].neighbors:
            n[e[0]].addNeighbors(n[e[1]])
    print("edges: ",len(edges))
    return nodes, edges, G , nodes_by_source
