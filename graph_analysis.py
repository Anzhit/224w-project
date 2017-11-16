import snap
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
# complete graph
graph = snap.LoadEdgeList(snap.PNGraph, 'newedges.txt', 0, 1)
graph_n, graph_e = graph.GetNodes(), graph.GetEdges()

scc = snap.LoadEdgeList(snap.PNGraph, 'sccedges.txt', 0, 1)
scc_n, scc_e = scc.GetNodes(), scc.GetEdges()

print graph_n, graph_e
print scc_n, scc_e
print "graph loaded"
#  in degree and clustering coeff, avg and plotted against degree
#  clustering coeff against category and uploader
#
def degree_analysis():
  deg_to_count = snap.TIntPrV()
  snap.GetInDegCnt(scc, deg_to_count)
  deg_scc = [i.GetVal1() for i in deg_to_count]
  cnt_scc = [i.GetVal2()/float(scc_n) for i in deg_to_count]

  # # plt.loglog(deg_graph, cnt_graph, label = 'entire graph')
  matplotlib.rcParams.update({'font.size': 13})
  plt.loglog(deg_scc, cnt_scc, label = 'SCC')
  plt.xlabel('in-degree')
  plt.ylabel('proportion of nodes')
  plt.legend()
  plt.grid(True)
  plt.title('in-degree distribution')
  plt.show()

  deg_to_count = snap.TIntPrV()
  snap.GetOutDegCnt(graph, deg_to_count)
  deg_graph = [i.GetVal1() for i in deg_to_count]
  cnt_graph = [i.GetVal2()/float(graph_n) for i in deg_to_count]
  cdf_graph = []
  cnt = 0
  for i in range(len(cnt_graph)):
    cnt += cnt_graph[i]
    cdf_graph.append(cnt)
  # ccdf_graph = [1- cdf_graph[i] + cnt_graph[i] for i in range(len(cdf_graph))]
  
  eg_to_count = snap.TIntPrV()
  snap.GetOutDegCnt(scc, deg_to_count)
  deg_scc = [i.GetVal1() for i in deg_to_count]
  cnt_scc = [i.GetVal2()/float(scc_n) for i in deg_to_count]
  cdf_scc = [0]
  cnt = 0
  for i in range(len(cnt_scc)):
    cnt += cnt_scc[i]
    cdf_scc.append(cnt)
  # ccdf_scc = [1- cdf_scc[i] + cnt_scc[i] for i in range(len(cdf_scc))]
  
  print "0", cdf_graph[0], cdf_scc[0]
  print "1-5", cdf_graph[5] - cdf_graph[0], cdf_scc[5] - cdf_scc[0]
  print "6-10", cdf_graph[10] - cdf_graph[5], cdf_scc[10] - cdf_scc[5]
  print "11-15", cdf_graph[15] - cdf_graph[10], cdf_scc[15] - cdf_scc[10]
  print "16-20", cdf_graph[20] - cdf_graph[15], cdf_scc[20] - cdf_scc[15]


def clustering_coefficient():
  print "Entire graph", snap.GetClustCf(graph, -1)
  print "SCC", snap.GetClustCf(scc, -1)

  snap.PlotClustCf(graph, "entire_graph", "Entire graph - clustering coefficient")
  snap.PlotClustCf(scc, "scc", "SCC - clustering coefficient")


def category_analysis():
  inFile = open("newattribs.txt", 'r')
  category_set = set()
  category_nodes = dict()
  for line in inFile.readlines():
    fields = line.split('\t')
    l = len(fields)
    if l > 4:
      category = fields[4]
      node = fields[0]
      category_set.add(category)
      if category in category_nodes:
        category_nodes[category].add(node)
      else:
        category_nodes[category] = set(node)

  x = ['overall']
  y = [snap.GetClustCf(scc, -1)]
  for category in category_nodes:
    print category
    nodes = category_nodes[category]
    category_graph = snap.TNGraph.New()
    for node in nodes:
      if scc.IsNode(int(node)):
        category_graph.AddNode(int(node))

    for edge in scc.Edges():
      src, dst = edge.GetSrcNId(), edge.GetDstNId()
      if str(src) in nodes and str(dst) in nodes:
        category_graph.AddEdge(src, dst)
    if category_graph.GetNodes() > 0:
      x.append(category)
      y.append(snap.GetClustCf(category_graph, -1))
    # print category, len(nodes) 
    # print category_graph.GetNodes(), category_graph.GetEdges()
    # print snap.GetClustCf(category_graph, -1) 
    # print
  
  xticks = np.arange(len(x))
  matplotlib.rcParams.update({'font.size': 13})
  bars = plt.barh(xticks, y, align='center')
  bars[0].set_color('r')
  plt.yticks(xticks, x)
  plt.xlabel('Clusetering Coefficient')
  plt.ylabel('Category')
  plt.show()

# degree_analysis()
# clustering_coefficient()
category_analysis()
