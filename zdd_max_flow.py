from dataclasses import dataclass

from graphillion import DiGraphSet as DGS

@dataclass
class Edge:
    to : int
    cap : int
    rev : int

class ZddMaxFlow:
    def __init__(self,n):
        self.g = [[] for _ in range(n)]
        self.edge_map = {} # 辺をキーとする構造体Edge参照辞書
    
    def add_edge(self,a,b,c):
        rev_index = len(self.g[b])
        index = len(self.g[a])
        self.g[a].append(Edge(b,c,rev_index))
        self.g[b].append(Edge(a,0,index))
        
        struct = self.g[a][-1]
        rev_struct = self.g[b][-1]
        self.edge_map[(a,b)] = struct
        self.edge_map[(b,a)] = rev_struct
    
    # graphillionで得たstパスを用いて、残余グラフを更新
    def max_flow(self, paths):
        mf = 0
        while True:
            # 更新不可能な辺を取る（フローを戻した場合に、更新可能になる辺が出てくる場合がある）
            available_edges = [edge for edge,v in self.edge_map.items() if v.cap > 0]
            if not available_edges:
                break

            # stパスグラフセットから、更新可能辺のみを含む新たなグラフセット（増加道）を作成
            augmenting_paths = paths.included(available_edges)
            if augmenting_paths.len() == 0:
                break

            # 更新可能パスの中で長さが最小なものを選ぶ
            path = next(augmenting_paths.min_iter())

            # その1つのパスの最小のcapを取得
            min_cap = min(self.edge_map[(a,b)].cap for a,b in path)
            if min_cap == 0:
                break

            for a,b in path:
                struct = self.edge_map[(a,b)]
                rev_struct = self.edge_map[(b,a)]
                struct.cap -= min_cap
                rev_struct.cap += min_cap

            mf += min_cap
        return mf