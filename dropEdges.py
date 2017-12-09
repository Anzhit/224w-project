import numpy as np
import snap
from scipy.spatial.distance import cosine

Rnd = snap.TRnd(42)
Rnd.Randomize()
G=snap.LoadEdgeList(snap.PNGraph, "sccedges.txt", 0, 1)

f = open("vec.emd","r")
x=f.readline()
dim=int(x.split()[1])
numNodes=int(x.split()[0])
dic={}
for _ in range(numNodes):
	t=f.readline().split()
	if len(t)==0:
		break
	dic[int(t[0])]=np.array(map(float,t[1:]))
edges=[]
for E in G.Edges():
	edges+=[(E.GetSrcNId(), E.GetDstNId())]
edges=np.random.permutation(edges)

X=np.zeros((100000,63))
cnt=0
for i in range(25000):
	X[cnt]=np.append(np.append(dic[edges[i][0]]-dic[edges[i][1]],cosine(dic[edges[i][0]],dic[edges[i][1]])),[1,0])
	X[cnt+1]=np.append(np.append(dic[edges[i][1]]-dic[edges[i][0]],cosine(dic[edges[i][0]],dic[edges[i][1]])),[1,0])
	cnt+=2

for i in range(25000):
	u=G.GetRndNId()
	v=G.GetRndNId()
	if(not G.IsEdge(u,v)):
		X[cnt]=np.append(np.append(dic[u]-dic[v],cosine(dic[u],dic[v])),[0,1])
		X[cnt+1]=np.append(np.append(dic[v]-dic[u],cosine(dic[u],dic[v])),[0,1])
		cnt+=2
	i-=1
np.save('neuralData.txt',X)
# cnt=0.0
# den=0
# cnt2=0.0
# den2=0
# for e in G.Edges():
# 	if (e.GetSrcNId() in dic and e.GetDstNId() in dic): 
# 		if G1.IsEdge(e.GetSrcNId(),e.GetDstNId()):
# 			cnt+=np.linalg.norm(dic[e.GetSrcNId()]-dic[e.GetDstNId()])
# 			den+=1
# 		else:
# 			cnt2+=np.linalg.norm(dic[e.GetSrcNId()]-dic[e.GetDstNId()])
# 			den2+=1

# print cnt/den
# print cnt2/den2