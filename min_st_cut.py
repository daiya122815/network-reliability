from graphillion import DiGraphSet as DGS
from collections import deque

class MinSTCut:

    def __init__(self,rg,mf):
        self.rg = rg # 残余グラフ
        self.mf = mf # max_flowの値
        # self.st_paths = st_paths # stパス集合
    
    """sからと到達可能頂点集合をSそうでない頂点集合をTとし、それを返す関数"""
    def recursive_dfs(self,rg,cur,visited):
        nxt = rg[cur]
        if not visited[nxt] and rg[cur][nxt].cap > 0:
            visited[nxt] = True
            self.recursive_dfs(rg,nxt,visited)
        return
    
    def stack_dfs(rg,s):
        S,T = set([s]),set()
        stack = []
        stack.append(s)
        n = len(rg)
        visited = [False]*n
        while stack:
            cur = stack.pop()
            for nxt in rg[cur].to:
                if not visited[nxt] and iter(rg[cur][nxt]).cap > 0: #イテレータで管理
                    visited[nxt] = True
                    stack.append(nxt)
                    S.add(nxt)
        T = set(list(range(n))) - S
        return S,T

    def bfs(rg,s):
        S,T = set([s]),set()
        deq = []
        deq.append(s)
        n = len(rg)
        visited = [False]*n
        while deq:
            cur = deq.leftpop()
            for nxt in rg[cur].to:
                if not visited[nxt] and iter(rg[cur][nxt]).cap > 0: #イテレータで管理
                    visited[nxt] = True
                    deq.append(nxt)
                    S.add(nxt)
        T = set(list(range(n))) - S
        return S,T
    
    """最小カット辺集合"""
    def min_st_cut_edges(self,rg,s,cur,visited):
        
        min_st_cut_edges = set()
        S,T = self.recursive_dfs(self,rg,cur,visited)
        S,T = self.stack_dfs(rg,s)
        S,T = self.bfs(rg,s)

        S_edges += [(v,nei) for v in S for nei in v]
        T_edges += [(v,nei) for v in T for nei in v]

        if sum(S_edges) <= sum(T_edges):
            for a,b in S_edges:
                if b in T:
                    min_st_cut_edges.add((a,b))
        else:
            for a,b in T_edges:
                if b in S:
                    min_st_cut_edges.add((a,b))
        return min_st_cut_edges