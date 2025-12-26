from graphillion import Universe
from graphillion import VertexSetSet

class ZddAllMinStCuts:

    def __init__(self, s_idx:int, t_idx:int, dag:list[list[int]], inv_dag:list[list[int]]):

        self.s_idx = s_idx
        self.t_idx = t_idx
        self.dag = dag
        self.inv_dag = inv_dag
        
        self.cand_vtx_set = [] # 入力が重複することがなく、順序を保持したいため　リスト
        self.include = set()
        self.exclude = set()
        self.family = None
    
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

        # s_idx sを含むscc連結成分のインデックス t_idxも同様
        # s_visited s_idxから到達可能頂点
        s_visited = self.stack_dfs(self.s_idx, self.dag)
        t_visited = self.stack_dfs(self.t_idx, self.inv_dag)

        # sから到達可能頂点は、必ず解に含む
        # tから到達可能頂点は、含んではならない。
        self.include = {v for v, ok in enumerate(s_visited) if ok}
        self.exclude = {v for v, ok in enumerate(t_visited) if ok}

        # sとtの両方から到達不可能である頂点を取り出す。
        for v, (s,t) in enumerate(zip(s_visited, t_visited)):
            if not (s or t):
                self.cand_vtx_set.append(v)
    
    def build_zdd(self, dag:list[list[int]], topological_order:list[int]):

        self.get_cand_vtx()

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
        visited = [False] * len(dag)
        for u,adj in enumerate(dag):
            for v in adj:
                visited[u] = True
                visited[v] = True
        
        flag = True
        dammy = 0
        for i, bool in enumerate(visited):
            if not bool:
                iso.append(i)
            elif flag:
                dammy = i
                flag = False

        dag_edges = [(u, v) for u in topological_order for v in dag[u]]
        dag_edges += [(dammy, v) for v in iso] # ダミー辺を追加

        Universe.set_universe(dag_edges) # 台集合のおまじない
        print("VSS =", VertexSetSet.universe())

        family = VertexSetSet([[]]) # 空集合からスタート
        for v in reversed(topological_order):
            # 逆トポ順で、zddを構築
            # excludeに含まれる頂点は、0,1のどちらの分岐にも進まないよう枝刈り
            if v in self.exclude:
                family = family.excluding(v)
                continue
            # includeに含まれる頂点は、それらの子を追加する
            if v in self.include:
                family = family.join(VertexSetSet([list(children[v])]))
                continue
            
            skip = family.excluding(v)
            take = family.join(VertexSetSet([list(children[v])]))
            family = skip | take
        
        # family = family.including(list(self.include)).excluding(list(self.exclude))
        
        return family