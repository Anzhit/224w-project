import numpy as np
import time
from sklearn.neighbors import LSHForest
import snap
import math
import pickle

f = open("vec.emd","r")
x=f.readline()
dim=int(x.split()[1])
numNodes=int(x.split()[0])

print dim
print numNodes

node2vec = {}
vec2node = {}
vec_list = []
node_list = []
for _ in range(numNodes):
  t=f.readline().split()
  node2vec[int(t[0])]=np.array(map(float,t[1:]))
  vec_list.append(np.array(map(float,t[1:])))
  node_list.append(int(t[0]))
  # vec2node[np.array_str(np.array(map(float,t[1:])))] = int(t[0])

print "node2vec read"

lshf = LSHForest()
lshf.fit(vec_list)

print "lsh indexing done"

graph = snap.LoadEdgeList(snap.PNGraph, 'sccedges.txt', 0, 1)

print "graph loaded"

count_deg = {}
overlap_deg = {}
count = 0

chosen_indices = np.random.choice(len(node_list), len(node_list)/100, replace=False)
print len(chosen_indices)

print time.time()
tuple_list = []
while count <= len(chosen_indices):
  query_input = []
  for i in range(count, min(count+1000, len(chosen_indices))):
    query_input.append(vec_list[chosen_indices[i]])

  _, B = lshf.kneighbors(query_input, n_neighbors = 30)
  for i in range(len(B)):
    lsh_neighbours = []
    for index in B[i]:
      lsh_neighbours.append(node_list[index])

    node = node_list[chosen_indices[count+i]]
    ni = graph.GetNI(node)
    deg = ni.GetOutDeg()
    graph_neighbours = []  
    for neighbours in ni.GetOutEdges():
      graph_neighbours.append(neighbours)
    
    graph_neighbours_vec = []
    for neighbour in graph_neighbours:
      graph_neighbours_vec.append(node2vec[neighbour])
    
    lsh_neighbours_vec = []
    lsh_neighbours = lsh_neighbours[:int(math.ceil(1.5*deg))]
    for neighbour in lsh_neighbours:
      lsh_neighbours_vec.append(node2vec[neighbour])
    
    tup = node2vec[node], graph_neighbours, graph_neighbours_vec, lsh_neighbours, lsh_neighbours_vec
    tuple_list.append(tup)

    lsh_neighbours = set(lsh_neighbours)
    graph_neighbours = set(graph_neighbours)

    overlap = lsh_neighbours & graph_neighbours
    if deg not in count_deg:
      count_deg[deg] = 1
      overlap_deg[deg] = len(overlap)
    else:
      count_deg[deg] += 1
      overlap_deg[deg] += len(overlap) 

  count += 1000
  if count % 10000 == 0:
    print count, time.time()

pickle.dump(tuple_list, open('neighbour_data.pkl', 'wb'))

sum_deg = 0
for deg in count_deg:
  sum_deg += count_deg[deg]
  print deg, count_deg[deg], float(overlap_deg[deg])/count_deg[deg]
print sum_deg

# WITH ONE HOT VECTOR FOR CATEGORY
inFile = open("newattribs.txt", 'r')
node_category = dict()
categories = set()
for line in inFile.readlines():
  fields = line.split('\t')
  l = len(fields)
  if l > 4:
    category = fields[4]
    node = int(fields[0])
    node_category[node] = category
    categories.add(category)

category_map = {}
count = 0
for category in categories:
  category_map[category] = count
  count += 1

updated_vec_list = []
for index in range(len(node_list)):
  node = node_list[index]
  one_hot = [0 for i in range(len(categories))]
  one_hot[category_map[node_category[node]]] = 1
  new_vec = vec_list[index].tolist() + one_hot
  updated_vec_list.append(new_vec)

lshf = LSHForest()
lshf.fit(updated_vec_list)

print "lsh indexing done"

up_count_deg = {}
up_overlap_deg = {}
count = 0

chosen_indices = np.random.choice(len(node_list), len(node_list)/10, replace=False)
print len(chosen_indices)

print time.time()
while count <= len(chosen_indices):
  query_input = []
  for i in range(count, min(count+1000, len(chosen_indices))):
    query_input.append(updated_vec_list[chosen_indices[i]])

  _, B = lshf.kneighbors(query_input, n_neighbors = 30)
  for i in range(len(B)):
    lsh_neighbours = []
    for index in B[i]:
      lsh_neighbours.append(node_list[index])

    node = node_list[chosen_indices[count+i]]
    ni = graph.GetNI(node)
    deg = ni.GetOutDeg()
    graph_neighbours = set()  
    for neighbours in ni.GetOutEdges():
      graph_neighbours.add(neighbours)
    

    lsh_neighbours = set(lsh_neighbours[:int(math.ceil(1.5*deg))])
    overlap = lsh_neighbours & graph_neighbours
    if deg not in up_count_deg:
      up_count_deg[deg] = 1
      up_overlap_deg[deg] = len(overlap)
    else:
      up_count_deg[deg] += 1
      up_overlap_deg[deg] += len(overlap) 

  count += 1000
  if count % 10000 == 0:
    print count, time.time()

sum_deg = 0
for deg in up_count_deg:
  sum_deg += up_count_deg[deg]
  print deg, up_count_deg[deg], float(up_overlap_deg[deg])/up_count_deg[deg]

print sum_deg