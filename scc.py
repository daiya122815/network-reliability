class Scc():
    def __init__(self,g,rev_g):
        self.g = g
        self.rev_g = rev_g
    
    def label_dfs(self,g,cur,visited,label,cnt):
        visited[cur] = True
        for nxt in g[cur]:
            if not visited[nxt]:
                self.dfs(g,nxt,visited,label,cnt)
        label[nxt] = cnt
        cnt += 1
        return
    
    def scc_dfs(self,g,cur,visited,component):
        visited[cur] = True
        component.add(cur)
        for nxt in g[cur]:
            if not visited[nxt]:
                self.dfs(g,cur,nxt,component)
        return component
    
    def decompose(self):
        return
    
    def strongly_connected_components(self):
        return
    