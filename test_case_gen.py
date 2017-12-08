import numpy

f = open("sccedges.txt","r")
edges = []
for line in f.readlines():
  edge = line.split()
  edges.append(edge)

for i in range(5):
  edge_file = 'test/edge_file_' + str(i) + '.txt'
  removed_edge_file = 'test/removed_edge_file_' + str(i) + '.txt'

  edges = numpy.random.permutation(edges)
  ef = open(edge_file, 'w') 
  ref = open(removed_edge_file, 'w') 
  r_edges = edges[:len(edges)/100]
  k_edges = edges[len(edges)/100:]

  for edge in r_edges:
    ref.write(edge[0] + ' ' + edge[1] + '\n')

  ref.flush()

  for edge in k_edges:
    ef.write(edge[0] + ' ' + edge[1] + '\n')
  ef.flush()