from dataclasses import dataclass
from copy import deepcopy

@dataclass
class Edge:
    # 隣接頂点番号、辺の容量、逆辺のインデックス、辺の向き
    to : int
    cap : int
    rev : int
    fwd : bool

class FordFulkerson:
    # 残余グラフの隣接リスト（インスタンス変数）
    def __init__(self, n:int):
        # residual_graph
        self.res_g = [[] for _ in range(n)]
    
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
    def dfs(self, visited:list, cur:int, t:int, f:int):
        visited[cur] = True
        if cur == t:
            return f
        
        for nxt in self.res_g[cur]:
            if not visited[nxt.to] and nxt.cap > 0:
                flow = self.dfs(visited, nxt.to, t, min(f,nxt.cap))
                
                # cur == tで更新するフローが確定されたのちに実行される
                if flow == 0:
                    continue
                nxt.cap -= flow
                self.res_g[nxt.to][nxt.rev].cap += flow
                return flow
        
        # 更新可能フロー（すべての頂点を辿り、更新フローが0）が見つからなくなった場合の返り値
        return 0
    
    # 最大流
    def max_flow(self, n:int, edges:list, s:int, t:int):
       
        # 各辺の入力
        for a,b,c in edges:
            self.add_edge(a,b,c) # 逆辺も追加し、各頂点は、構造体（num,cap,rev）を持つ
        
        before_res_g = deepcopy(self.return_residual_graph()) # オブジェクトを新たな変数にコピー

        mf = 0
        INF = float("inf")
        
        # 更新可能フローが見つからなくなるまで実行
        while True:
            visited = [False] * n
            flow = self.dfs(visited, s, t, INF)
            if flow == 0:
                break
            mf += flow
        
        after_res_g = deepcopy(self.return_residual_graph())
        
        return mf, before_res_g, after_res_g