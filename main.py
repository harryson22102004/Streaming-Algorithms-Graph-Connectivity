import random
from collections import defaultdict
 
class StreamingConnectivity:
    """Semi-streaming connectivity using union-find."""
    def __init__(self, n):
        self.n = n
        self.parent = list(range(n))
        self.rank = [0]*n
        self.edges_processed = 0
 
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
 
    def union(self, u, v):
        pu, pv = self.find(u), self.find(v)
        if pu == pv: return False
        if self.rank[pu] < self.rank[pv]: pu, pv = pv, pu
        self.parent[pv] = pu
        if self.rank[pu] == self.rank[pv]: self.rank[pu] += 1
        return True
 
    def process_edge(self, u, v):
        self.edges_processed += 1
        return self.union(u, v)
 
    def n_components(self):
        return sum(1 for i in range(self.n) if self.find(i) == i)
 
    def are_connected(self, u, v):
        return self.find(u) == self.find(v)
 
class SpannerConstruction:
    """Build a (2k-1)-spanner in streaming model."""
    def __init__(self, n, k=2):
        self.n = n; self.k = k
        self.spanner_edges = []
        self.uf = StreamingConnectivity(n)
 
    def process(self, u, v, w=1):
        if self.uf.find(u) != self.uf.find(v):
            self.spanner_edges.append((u, v, w))
            self.uf.union(u, v)
          n = 10
stream = [(random.randint(0,n-1), random.randint(0,n-1)) for _ in range(50)]
sc = StreamingConnectivity(n)
for u, v in stream:
    sc.process_edge(u, v)
print(f"Nodes: {n}, Edges processed: {sc.edges_processed}")
print(f"Connected components: {sc.n_components()}")
print(f"0 and 5 connected: {sc.are_connected(0,5)}")
sp = SpannerConstruction(n, k=2)
for u,v in stream: sp.process(u,v)
print(f"Spanner edges (spanning forest): {len(sp.spanner_edges)}")
