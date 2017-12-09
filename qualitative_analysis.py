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

inFile = open("newattribs.txt", 'r')
node_category = dict()
node_uploader = dict()
categories = set()
for line in inFile.readlines():
  fields = line.split('\t')
  l = len(fields)
  if l > 4:
    uploader = fields[2]
    category = fields[4]
    node = int(fields[0])
    node_category[node] = category
    node_uploader[node] = uploader
    categories.add(category)


collegehumor_videos = [
  576570,
  634213,
  231480,
  884068,
  276590,
]

music_videos = [
  1284130,
  1349741,
  1115470,
  156635,
  444916,
]

nba_videos = [
  722508,
  1132387,
  1748344,
  968769,
  1158560,
]

all_node2vec = np.array([node2vec[node] for node in collegehumor_videos])
# print all_node2vec

avg_node2vec = np.mean(all_node2vec, axis=0)
# print avg_node2vec
A, B = lshf.kneighbors([avg_node2vec], n_neighbors = 30)
lsh_neighbours = []
for index in B[0]:
  lsh_neighbours.append(node_list[index])

new_predictions = set(lsh_neighbours) & set(collegehumor_videos)
print lsh_neighbours
for node in new_predictions:
  print node, node_uploader[node], node_category