# from graphillion import DiGraphSet as DGS
from collections import deque

class MinStCut:

    def __init__(self, arg:list):
        # self.mf = mf # max_flowの値
        self.after_res_g = arg # 更新後の残余グラフ
        # self.st_paths = st_paths # stパス集合
        self.fwd_g = [[] for _ in range(len(self.after_res_g))]
    
    def forward_edges(self):
        # 残余グラフから、正辺のみを取り出す
        fwd_edges = []
        
        for i,v in enumerate(self.after_res_g):
            for edge in v:
                # Edge(to,cap,rev,fwd)
                if edge.fwd:
                    fwd_edges.append((i, edge.to, edge.cap))
        
        return fwd_edges
    
    def build_forward_graph(self, fwd_edges:list):
        for a,b,c in fwd_edges:
            self.fwd_g[a].append((b,c))
        return self.fwd_g


    # sからと到達可能頂点集合をS、そうでない頂点集合をTとし、それを返す関数
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
        S, T = {s}, set()
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
        
        return S, T

    def bfs(self, s:int):
        S, T ={s}, set()
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
        
        return S, T
    
    # 最小カット辺集合
    def min_st_cut_edges(self, s:int):

        fwd_edges = self.forward_edges()
        self.build_forward_graph(fwd_edges)

        S, T = self.bfs(s)
        min_st_cut_edges = set()

        # S_edges, T_edges = [], []
        # S_edges += [edges for v in S for edges in self.fwd_g[v]]
        # print(S_edges, len(S_edges))
        # if len(S_edges) <= len(T_edges):
        for v in S:
            # for edge in self.arg[v]:
            #     if edge.fwd and edge.to in T and edge.cap == 0:
            #         min_st_cut_edges.add((v,edge.to))
            for edge in self.fwd_g[v]:
                # edge[0],edge[1]
                if edge[0] in T and edge[1] == 0:
                    min_st_cut_edges.add((v, edge[0]))
        # else:

        return min_st_cut_edges