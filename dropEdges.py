import numpy as np
import snap
from scipy.spatial.distance import cosine
Rnd = snap.TRnd(42)
Rnd.Randomize()
G=snap.LoadEdgeList(snap.PNGraph, "edges.txt", 0, 1)
G1=snap.LoadEdgeList(snap.PNGraph, "droppedEdges.txt", 0, 1)
# for n in G.Nodes():
# 	if n.GetOutDeg()>=15 :
# 		d=np.random.choice(list(n.GetOutEdges()),n.GetOutDeg()-15, replace=False)
# 		for e in d:
# 			G.DelEdge(n.GetId(),e)


# snap.SaveEdgeList(G, 'droppedEdges.txt')

f = open("vecdropped.emd","r")
x=f.readline()
dim=int(x.split()[1])
numNodes=int(x.split()[0])
print dim
print numNodes
dic={}
for _ in range(numNodes):
	t=f.readline().split()
	if len(t)==0:
		break
	dic[int(t[0])]=np.array(map(float,t[1:]))

cnt=0.0
den=0
cnt2=0.0
den2=0
for e in G.Edges():
	if (e.GetSrcNId() in dic and e.GetDstNId() in dic): 
		if G1.IsEdge(e.GetSrcNId(),e.GetDstNId()):
			cnt+=np.linalg.norm(dic[e.GetSrcNId()]-dic[e.GetDstNId()])
			den+=1
		else:
			cnt2+=np.linalg.norm(dic[e.GetSrcNId()]-dic[e.GetDstNId()])
			den2+=1

print cnt/den
print cnt2/den2