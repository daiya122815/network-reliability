from dataclasses import dataclass
from copy import deepcopy
from collections import deque

@dataclass
class Edge:
    # 隣接頂点番号、辺の容量、逆辺のインデックス、辺の向き
    to : int
    cap : int
    rev : int
    fwd : bool

class Dinic:
    # 残余グラフの隣接リストと各頂点のリストイテレータ（インスタンス変数）
    def __init__(self, n:int):
        # residual_graph
        self.res_g = [[] for _ in range(n)]
        self.itr = [0] * n
    
    # 辺の追加
    def add_edge(self, a:int, b:int, c:int):
        # 正辺に逆辺のインデックス、逆辺に正辺のインデックスを追加
        rev_idx = len(self.res_g[b])
        idx = len(self.res_g[a])
        self.res_g[a].append(Edge(b, c, rev_idx, True))
        self.res_g[b].append(Edge(a, 0, idx, False))
    
    # 残余グラフを返す
    def return_residual_graph(self):
        return self.res_g

    # s,tまでのパスを探索し、流せる分だけフローを流す
    def dfs(self, dist:list[int], cur:int, t:int, f:int):
        if cur == t:
            return f
        
        # itrで、同レベルグラフで、前に探索した辺をdfsで再度探索しないようにする
        while self.itr[cur] < len(self.res_g[cur]):
            e = self.res_g[cur][self.itr[cur]]
            self.itr[cur] += 1

            # 距離の差が1である辺のみを通り、tまでの最短経路を探索
            if dist[e.to] == dist[cur]+1 and dist[e.to] <= dist[t] and e.cap > 0:
                flow = self.dfs(dist, e.to, t, min(f,e.cap))
                
                # cur == tで更新するフローが確定されたのちに実行される
                if flow == 0:
                    continue
                e.cap -= flow
                self.res_g[e.to][e.rev].cap += flow
                return flow
        
        # 更新可能フロー（すべての頂点を辿り、更新フローが0）が見つからなくなった場合の返り値
        return 0

    def bfs(self, s:int):
        n = len(self.res_g)
        deq = deque([s])
        dist = [-1] * n
        dist[s] = 0
        
        while deq:
            cur = deq.popleft()
            
            for e in self.res_g[cur]:
                if dist[e.to] == -1 and e.cap > 0:
                    dist[e.to] = dist[cur] + 1
                    deq.append(e.to)
        
        return dist

    # 最大流
    def max_flow(self, n:int, edges:list, s:int, t:int):
       
        # 各辺の入力
        for u,v,c in edges:
            self.add_edge(u,v,c) # 逆辺も追加し、各頂点は、構造体（num,cap,rev）を持つ
        
        before_res_g = deepcopy(self.return_residual_graph()) # オブジェクトを新たな変数にコピー

        mf = 0
        INF = float("inf")
        
        # 更新可能フローが見つからなくなるまで実行
        while True:
            flow = 0
            # bfsで各頂点の距離をラベル付けし、距離グラフを構築
            dist = self.bfs(s)
            if dist[t] == -1: # tに到達不可能であれば、終了
                break
            
            self.itr = [0] * n

            while True:
                flow = self.dfs(dist, s, t, INF)
                if flow == 0:
                    break
                mf += flow
        
        after_res_g = deepcopy(self.return_residual_graph())
        
        return mf, before_res_g, after_res_g