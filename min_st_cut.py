# from graphillion import DiGraphSet as DGS
from collections import deque

class MinStCut:

    def __init__(self,mf,arg):
        self.arg = arg # 残余グラフ
        self.mf = mf # max_flowの値
        # self.st_paths = st_paths # stパス集合
        self.forward_graph = [[] for _ in range(len(arg))]
    
    def forward_edges(self,arg):
        # 残余グラフから、正辺のみを取り出す
        forward_edges = []
        for i,v in enumerate(arg):
            for edge in v:
                # Edge(to,cap,rev,forward)
                if edge.forward:
                    forward_edges.append((i,edge.to,edge.cap))
        return forward_edges
    
    def build_forward_graph(self,forward_edges):
        for a,b,c in forward_edges:
            self.forward_graph[a].append((b,c))
        return self.forward_graph


    # sからと到達可能頂点集合をS、そうでない頂点集合をTとし、それを返す関数
    def recursive_dfs(self,cur,visited,s,S):
        visited[cur] = True
        for nxt,cap in self.forward_graph[cur]:
            if not visited[nxt] and cap > 0:
                visited[nxt] = True
                S.add(nxt)
                self.recursive_dfs(nxt,visited,s,S)
        if cur == s:
            n = len(self.forward_graph)
            T = set(range(n)) - S
            return S,T
        return
    
    def stack_dfs(self,s):
        S,T = {s},set()
        n = len(self.forward_graph)
        stack = [s]
        visited = [False]*n
        visited[s] = True
        while stack:
            cur = stack.pop()
            for nxt,cap in self.forward_graph[cur]:
                if not visited[nxt] and cap > 0:
                    visited[nxt] = True
                    stack.append(nxt)
                    S.add(nxt)
        T = set(range(n)) - S
        return S,T

    def bfs(self,s):
        S,T ={s},set()
        n = len(self.forward_graph)
        deq = deque([s])
        visited = [False]*n
        visited[s] = True
        while deq:
            cur = deq.popleft()
            for nxt,cap in self.forward_graph[cur]:
                if not visited[nxt] and cap > 0:
                    visited[nxt] = True
                    deq.append(nxt)
                    S.add(nxt)
        T = set(range(n)) - S
        return S,T
    
    # 最小カット辺集合
    # def min_st_cut_edges(self,s):
        
    #     min_st_cut_edges = set()
    #     # S,T = self.recursive_dfs(self.forward_graph,cur,visited)
    #     S,T = self.stack_dfs(s)
    #     # S,T = self.bfs(s)

    #     # これ心配
    #     S_edges,T_edges = set(),set()
    #     S_edges += [(v,nei) for v in S for nei in v]
    #     T_edges += [(v,nei) for v in T for nei in v]

    #     if sum(S_edges) <= sum(T_edges):
    #         for a,b in S_edges:
    #             if b in T:
    #                 min_st_cut_edges.add((a,b))
    #     else:
    #         for a,b in T_edges:
    #             if b in S:
    #                 min_st_cut_edges.add((a,b))
    #     return min_st_cut_edges
    def min_st_cut_edges(self, s):
        S, T = self.stack_dfs(s)
        cut_edges = set()
        for u in S:
            for edge in self.arg[u]:
                if edge.forward and edge.to in T and edge.cap == 0:
                    cut_edges.add((u, edge.to))
        return cut_edges