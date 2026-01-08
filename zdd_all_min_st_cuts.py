from graphillion import Universe, VertexSetSet

class ZddAllMinStCuts:

    def __init__(self, s_idx:int, t_idx:int, dag:list[list[int]], rev_dag:list[list[int]]):
        self.s_idx = s_idx
        self.t_idx = t_idx
        self.dag = dag
        self.rev_dag = rev_dag
    
    def stack_dfs(self, s:int, g:list[list[int]]):
        stack = [s]
        visited = [False] * len(g)
        visited[s] = True

        while stack:
            cur = stack.pop()
            for nxt in g[cur]:
                if not visited[nxt]:
                    visited[nxt] = True
                    stack.append(nxt)
        
        return visited
    
    def get_cand_vtx(self):

        # s_idx sを含むscc連結成分のインデックス
        # s_visited s_idxから到達可能頂点
        # tも同様
        s_visited = self.stack_dfs(self.s_idx, self.dag)
        t_visited = self.stack_dfs(self.t_idx, self.rev_dag)

        # sから到達可能頂点は、必ず解に含む
        # tから到達可能頂点は、含んではならない。
        include = {v for v, ok in enumerate(s_visited) if ok}
        exclude = {v for v, ok in enumerate(t_visited) if ok}

        # sとtの両方から到達不可能である頂点を取り出す。
        sol_cand_vtx = []
        for v, (s,t) in enumerate(zip(s_visited, t_visited)):
            if not (s or t):
                sol_cand_vtx.append(v)
        
        return include, exclude, sol_cand_vtx
    
    def build_zdd(self, dag:list[list[int]], topological_order:list[int]):

        include, exclude, sol_cand_vtx = self.get_cand_vtx()
        print("include =",include)
        print("exclude =",exclude)
        n = len(dag)

        # 各頂点の自身の子となる頂点関係を列挙
        children = [set() for _ in range(n)]
        for v in reversed(topological_order):      # 逆トポ順によって子から伝播させる
            child = {v}
            for nxt in dag[v]:
                child |= children[nxt]
            children[v] = child
        print("children =", children)
        
        iso = [] # 孤立したした頂点集合
        for u,adj in enumerate(dag):
            if not adj:
                iso.append(u)
        print(iso)

        dag_edges = [(u,v) for u in topological_order for v in dag[u]]
        dammy_edges = [(topological_order[-1], v) for v in iso] # ダミー辺を追加
        dag_edges += dammy_edges
        
        Universe.set_universe(dag_edges) # 台集合のおまじない
        VSS = VertexSetSet.universe() # VSSに変換

        family = VertexSetSet([[]]) # 空集合からスタート
        for v in reversed(topological_order):
            # 逆トポ順で、zddを構築
            
            # excludeに含まれる頂点は、0,1のどちらの分岐にも進まないよう枝刈り
            if v in exclude:
                family = family.excluding(v)
                continue
            
            # includeに含まれる頂点は、それらの子を追加する
            if v in include:
                family = family.join(VertexSetSet([list(children[v])]))
                continue
            
            # それ以外の解の候補となる頂点
            skip = family.excluding(v)
            take = family.join(VertexSetSet([list(children[v])]))
            family = skip | take
        
        # family = family.including(list(self.include)).excluding(list(self.exclude))
        
        return family