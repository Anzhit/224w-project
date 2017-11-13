import numpy as np
import snap
Rnd = snap.TRnd(42)
Rnd.Randomize()
G=snap.LoadEdgeList(snap.PNGraph, "edges.txt", 0, 1)
f = open("vec.emd","r")
x=f.readline()
dim=int(x.split()[1])
numNodes=int(x.split()[0])
print dim
print numNodes
dic={}
for _ in range(numNodes):
	t=f.readline().split()
	dic[int(t[0])]=np.array(map(float,t[1:]))
cnt=0.0
den=0
for e in G.Edges():
	cnt+=np.linalg.norm(dic[e.GetSrcNId()]-dic[e.GetDstNId()])
	den+=1

print cnt/den
cnt=0.0
den=0
for _ in range(10000):
	a=G.GetRndNId(Rnd)
	b=G.GetRndNId(Rnd)
	if(not G.IsEdge(a,b)):
		cnt+=np.linalg.norm(dic[a]-dic[b])
		den+=1
print cnt/den

