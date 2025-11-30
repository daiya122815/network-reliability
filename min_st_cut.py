# from graphillion import DiGraphSet as DGS
from collections import deque

class MinStCut:

    def __init__(self, mf:int ,arg:list):
        self.arg = arg # 更新後の残余グラフ
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
    def recursive_dfs(self, cur:int, visited:list, s:int, S:set):
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
    
    def stack_dfs(self, s:int):
        S,T = {s},set()
        stack = [s]
        n = len(self.forward_graph)
        visited = [False] * n
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

    def bfs(self, s:int):
        S,T ={s},set()
        deq = deque([s])
        n = len(self.forward_graph)
        visited = [False] * n
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
    def min_st_cut_edges(self, s:int):
        S,T = self.bfs(s)
        min_st_cut_edges = set()
        
        # S_edges, T_edges = [], []
        # S_edges += [edges for v in S for edges in self.forward_graph[v]]
        # print(S_edges, len(S_edges))
        # if len(S_edges) <= len(T_edges):
        for v in S:
            # for edge in self.arg[v]:
            #     if edge.forward and edge.to in T and edge.cap == 0:
            #         min_st_cut_edges.add((v,edge.to))
            for edge in self.forward_graph[v]:
                # edge[0],edge[1]
                if edge[0] in T and edge[1] == 0:
                    min_st_cut_edges.add((edge[0], edge[1]))
        # else:

        return min_st_cut_edges