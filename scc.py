class Scc:
    
    def __init__(self,g):
        # 更新後残余グラフ
        self.g = g
    
    def order_dfs(self, cur:int, visited:list, order:list):
        # 各頂点を帰りがけ順で順位付け
        visited[cur] = True
        
        for nxt in self.g[cur]:
            if not visited[nxt]:
                self.order_dfs(nxt,visited,order)
        
        order.append(cur)
    
    def scc_dfs(self, rev_g:list, cur:int, visited:list, component:list):
        visited[cur] = True
        component.append(cur)
        
        for nxt in rev_g[cur]:
            if not visited[nxt]:
                self.scc_dfs(rev_g, nxt, visited, component)
        
        return component
    
    def scc_dag(self,components):
        n = len(self.g)

        # 各頂点に連結成分ごとのidを付与
        comp_id = [-1] * n
        for i, comp in enumerate(components):
            for v in comp:
                comp_id[v] = i        
        
        # すべての辺を見て、連結成分が異なる場合、連結成分の隣接リストを更新
        comp_sets = [set() for _ in range(len(components))]
        for u in range(n):
            for v in self.g[u]:
                cu, cv = comp_id[u], comp_id[v]
                if cu != cv:
                    comp_sets[cu].add(cv)
        scc_dag = [sorted(comp) for comp in comp_sets]
        return scc_dag
    
    def decompose(self):
        n = len(self.g)
        rev_g = [[] for _ in range(n)] # 逆辺からなるグラフ
        for u in range(n):
            for v in self.g[u]:
                rev_g[v].append(u)
        
        order = []
        visited = [False] * n
        for v in range(n):
            if not visited[v]:
                self.order_dfs(v, visited, order)
        
        components = []
        visited = [False] * n
        # 順序付けと逆順で、逆辺グラフを探索
        for v in reversed(order):
            if visited[v]:
                continue
            component = self.scc_dfs(rev_g, v, visited, [])
            components.append(component)
        
        # 連結成分ごとのdagを取得
        dag = self.scc_dag(components)

        return components, dag

    def strongly_connected_components(self):
        scc, dag = self.decompose()
        return scc, dag