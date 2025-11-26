class Scc:
    
    def __init__(self,g):
        self.g = g
    
    def order_dfs(self,cur,visited,order):
        visited[cur] = True
        for nxt in self.g[cur]:
            if not visited[nxt]:
                self.order_dfs(nxt,visited,order)
        order.append(cur)
    
    def scc_dfs(self,rev_g,cur,visited,component):
        visited[cur] = True
        component.add(cur)
        for nxt in rev_g[cur]:
            if not visited[nxt]:
                self.scc_dfs(rev_g,nxt,visited,component)
        return frozenset(component)
    
    def decompose(self):
        n = len(self.g)
        rev_g = [[] for _ in range(n)]
        for u in range(n):
            for v in self.g[u]:
                rev_g[v].append(u)
        
        order = []
        visited = [False] * n
        for v in range(n):
            if not visited[v]:
                self.order_dfs(v,visited,order)
        
        components = set()
        visited = [False] * n
        for v in reversed(order):
            if visited[v]:
                continue
            component = self.scc_dfs(rev_g,v,visited,set())
            components.add(component)

        return components

    def strongly_connected_components(self):
        scc = self.decompose()
        return scc
    