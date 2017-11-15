import numpy as np
import snap
import matplotlib.pyplot as plt
from scipy.spatial.distance import cosine
Rnd = snap.TRnd(42)
Rnd.Randomize()
G=snap.LoadEdgeList(snap.PUNGraph, "sccedges.txt", 0, 1)
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
# cnt=0.0
# den=0
# for e in G.Edges():
# 	cnt+=cosine(dic[e.GetSrcNId()],dic[e.GetDstNId()])
# 	den+=1

# print cnt/den
# cnt=0.0
# den=0
# for _ in range(10000):
# 	a=G.GetRndNId(Rnd)
# 	b=G.GetRndNId(Rnd)
# 	if(not (G.IsEdge(a,b) and G.IsEdge(b,a))):
# 		cnt+=cosine(dic[a],dic[b])
# 		den+=1
# print cnt/den

deg2dist ={}

for _ in range(20000):
	n=G.GetNI(G.GetRndNId(Rnd))
	d=n.GetOutDeg()
	if not d in deg2dist:
		deg2dist[d]=[0.0,0.0,0.0,0.0]
	for i in n.GetOutEdges():
		deg2dist[d][1]+=1
		deg2dist[d][0]+=cosine(dic[n.GetId()],dic[i])
	for _ in range(200):
		a=G.GetRndNId(Rnd)
		if(not G.IsEdge(a,n.GetId()) ):
			deg2dist[d][2]+=cosine(dic[n.GetId()],dic[a])
			deg2dist[d][3]+=1

X=[]
Yn=[]
Ynn=[]
for d in deg2dist:
	X+=[d]
	Yn+=[(deg2dist[d][2]/deg2dist[d][3])/(deg2dist[d][0]/deg2dist[d][1])]

plt.plot(X,Yn,'r')
plt.show()





