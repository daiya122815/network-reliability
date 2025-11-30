from dataclasses import dataclass

@dataclass
class Edge:
    # 隣接頂点番号、辺の容量、逆辺のインデックス、辺の向き
    to : int
    cap : int
    rev : int
    forward : bool

class FordFulkerson:
    # 残余グラフの隣接リスト（インスタンス変数）
    def __init__(self, n:int):
        self.rg = [[] for _ in range(n)]
    
    # 辺の追加
    def add_edge(self, a:int, b:int, c:int):
        # 正辺に逆辺のインデックス、逆辺に正辺のインデックスを追加
        rev_idx = len(self.rg[b])
        idx = len(self.rg[a])
        self.rg[a].append(Edge(b, c, rev_idx, True))
        self.rg[b].append(Edge(a, 0, idx, False))

    # s,tまでのパスを探索し、流せる分だけフローを流す
    def dfs(self, visited:list, cur:int, t:int, f:int):
        visited[cur] = True
        if cur == t:
            return f
        
        for nxt in self.rg[cur]:
            if not visited[nxt.to] and nxt.cap > 0:
                flow = self.dfs(visited, nxt.to, t, min(f,nxt.cap))
                
                # cur == tで更新するフローが確定されたのちに実行される
                if flow == 0:
                    continue
                nxt.cap -= flow
                self.rg[nxt.to][nxt.rev].cap += flow
                return flow
        
        # 更新可能フロー（すべての頂点を辿り、更新フローが0）が見つからなくなった場合の返り値
        return 0
    
    # 最大流
    def max_flow(self, s:int, t:int):
        n = len(self.rg)
        mf = 0
        INF = float("inf")
        
        # 更新可能フローが見つからなくなるまで実行
        while True:
            visited = [False] * n
            flow = self.dfs(visited, s, t, INF)
            if flow == 0:
                break
            mf += flow
        
        return mf
    
    def return_residual_graph(self):
        return self.rg