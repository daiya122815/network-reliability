from dataclasses import dataclass

from graphillion import DiGraphSet as DGS

@dataclass
class Edge:
    to : int    
    cap : int
    rdx : int # rev_index

class ZddMaxFlow:
    def __init__(self,n):
        self.g = [[] for _ in range(n)]
    
    def add_edge(self,a,b,c):
        rev_index = len(self.g[b])
        index = len(self.g[a])
        self.g[a].append(Edge(b,c,rev_index))
        self.g[b].append(Edge(a,0,index))
    
    # graphillionで得たstパスを用いて、残余グラフを更新
    def max_flow(self, paths):
        mf = 0
        while True:
            # 更新不可能な辺を取る（フローを戻した場合に、更新可能になる辺が出てくる場合がある）
            available_edges = []
            for v,adj in enumerate(self.g): # 頂点番号とその隣接リスト
                for nxt in adj:
                    if nxt.cap > 0:
                        available_edges.append((v,nxt.to))
            if not available_edges:
                break

            # stパスグラフセットから、更新可能辺のみを含む新たなグラフセット（増加道）を作成
            augmenting_paths = paths.included(available_edges)
            if augmenting_paths.len() == 0:
                break

            # 更新可能パスの中で長さが最小なものを選ぶ
            path = next(augmenting_paths.min_iter())

            # そのパスの最小のcapを取得
            min_cap = float("inf")
            nxt_Edge_list = []
            for a,b in path:
                for nxt in self.g[a]:
                    if nxt.to == b:
                        break
                min_cap = min(min_cap,nxt.cap)
                nxt_Edge_list.append(nxt)
            if min_cap == 0:
                break

            for nxt in nxt_Edge_list:
                nxt.cap -= min_cap
                self.g[nxt.to][nxt.rdx].cap += min_cap
            mf += min_cap
        return mf