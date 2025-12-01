from collections import deque

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
    
    def scc_dag(self, components:list):
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
    
    def topological_sort(self, dag:list):
        n = len(dag)
        topological_dag = []

        # 入次数
        indgrees = [0] * n
        for u in dag:
            for v in u:
                indgrees[v] += 1
        
        # 入次数が0である頂点をdeqに追加
        deq = deque()
        for i in range(n):
            if indgrees[i] == 0:
                deq.append(i)
        
        while deq:
            v = deq.popleft()

            for nei in dag[v]:
                indgrees[nei] -= 1
                if indgrees[nei] == 0:
                    deq.append(nei)
            
            topological_dag.append(v)

        return topological_dag
    
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
        
        # 連結成分ごとのDAGを取得
        dag = self.scc_dag(components)

        topological_dag = self.topological_sort(dag)

        return components, dag, topological_dag

    def strongly_connected_components(self):
        scc, dag, topological_dag = self.decompose()
        return scc, dag, topological_dag