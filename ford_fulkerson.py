from dataclasses import dataclass

@dataclass
class Edge:
    # 隣接頂点番号、辺の容量、逆辺のインデックス
    to : int
    cap : int
    rev : int

class FordFulkerson:
    # グラフの隣接リスト（インスタンス変数）
    def __init__(self,n):
        self.g = [[] for _ in range(n)]
    
    # 辺の追加
    def add_edge(self,a,b,c):
        # 正辺に逆辺のインデックス、逆辺に正辺のインデックスを追加
        rev_index = len(self.g[b])
        index = len(self.g[a])
        self.g[a].append(Edge(b,c,rev_index))
        self.g[b].append(Edge(a,0,index))

    # s,tまでのパスを探索し、流せる分だけフローを流す
    def dfs(self,visited,cur,t,f):
        visited[cur] = True
        if cur == t:
            return f
        
        for nxt in self.g[cur]:
            if not visited[nxt.to] and nxt.cap > 0:
                flow = self.dfs(visited,nxt.to,t,min(f,nxt.cap))
                # cur == tで更新するフローが確定されたのちに実行される
                if flow == 0:
                    continue
                nxt.cap -= flow
                self.g[nxt.to][nxt.rev].cap += flow
                return flow
        # 更新可能フロー（すべての頂点を辿り、更新フローが0）が見つからなくなった場合の返り値
        return 0
    
    # 最大流
    def max_flow(self,s,t):
        mf = 0
        INF = float("inf")
        n = len(self.g)
        # 更新可能フローが見つからなくなるまで実行
        while True:
            visited = [False]*n
            flow = self.dfs(visited,s,t,INF)
            if flow == 0:
                break
            mf += flow
        return mf