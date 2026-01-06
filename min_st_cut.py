from collections import deque

class MinStCut:

    # 構造体　Edge(to,cap,rev,fwd)
    def __init__(self, after_res_g):
        self.after_res_g = after_res_g # 最大流計算後の残余グラフ
        self.fwd_g = [[] for _ in range(len(self.after_res_g))]

    def build_forward_graph(self):
        # 残余グラフの順辺からなる、部分グラフfwd_gを構築
        for i,v in enumerate(self.after_res_g):
            for e in v:
                if e.fwd:
                    self.fwd_g[i].append((e.to, e.cap))
        
        return self.fwd_g
    
    # sから到達可能頂点集合をS、そうでない頂点集合をTとし、それを返す関数
    def recursive_dfs(self, cur:int, visited:list, s:int, S:set):
        visited[cur] = True
        for nxt,cap in self.fwd_g[cur]:
            if not visited[nxt] and cap > 0:
                visited[nxt] = True
                S.add(nxt)
                self.recursive_dfs(nxt,visited,s,S)
        
        if cur == s:
            n = len(self.fwd_g)
            T = set(range(n)) - S
            return S,T
        
        return
    
    def stack_dfs(self, s:int):
        S,T = {s}, set()
        stack = [s]
        n = len(self.fwd_g)
        visited = [False] * n
        visited[s] = True
        
        while stack:
            cur = stack.pop()
            for nxt,cap in self.fwd_g[cur]:
                if not visited[nxt] and cap > 0:
                    visited[nxt] = True
                    stack.append(nxt)
                    S.add(nxt)
        T = set(range(n)) - S
        
        return S,T

    def bfs(self, s:int):
        S,T ={s}, set()
        deq = deque([s])
        n = len(self.fwd_g)
        visited = [False] * n
        visited[s] = True
        
        while deq:
            cur = deq.popleft()
            for nxt,cap in self.fwd_g[cur]:
                if not visited[nxt] and cap > 0:
                    visited[nxt] = True
                    deq.append(nxt)
                    S.add(nxt)
        T = set(range(n)) - S
        
        return S,T
    
    # 最小カット辺集合
    def min_st_cut_edges(self, s:int):

        self.build_forward_graph()

        S,T = self.bfs(s)

        min_st_cut_edges = set()        
        for v in S:
            for edge in self.fwd_g[v]:
                to,cap = edge
                if to in T and cap == 0:
                    min_st_cut_edges.add((v, to))

        return min_st_cut_edges