class AllMinStCuts:

    def __init__(self, s_order: int, t_order: int, dag: list[list[int]], inv_dag: list[list[int]]):
        self.s_order = s_order
        self.t_order = t_order
        self.dag = dag
        self.inv_dag = inv_dag
        
        self.sol_set = [] # 入力が重複することがなく、順序を保持したいため　リスト 
        self.include = set()
        self.exclude = set()

    def stack_dfs(self, s: int, g: list[list[int]]):
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

        # s_order sを含むscc連結成分のインデックス t_orderも同様
        # s_visited s_orderから到達可能頂点
        s_visited = self.stack_dfs(self.s_order, self.dag)
        t_visited = self.stack_dfs(self.t_order, self.inv_dag)

        # sから到達可能頂点は、必ず解に含む
        # tから到達可能頂点は、含んではならない。
        self.include = {v for v, ok in enumerate(s_visited) if ok}
        self.exclude = {v for v, ok in enumerate(t_visited) if ok}
        for v, (s, t) in enumerate(zip(s_visited, t_visited)):
            if not (s or t):
                self.sol_set.append(v)
    
    def _is_closed(self, nodes: set[int]) -> bool:
        for v in nodes:
            for nxt in self.dag[v]:
                if nxt not in nodes:
                    return False
        return True
    
    # すべての最小カットを求める
    def solver(self):
        self.get_cand_vtx()

        ans = []
        # bit全探索なので、nが小さい場合のみ有効
        n = len(self.sol_set)
        for mask in range(1 << n):
            new = set(self.include)
            for bit in range(n):
                if (mask>>bit) & 1:
                    new.add(self.sol_set[bit])
            
            if new & self.exclude: # 新たな解とexcludeに共通部分がある場合は追加しない
                continue
            if self._is_closed(new): # 新たな解が閉包を満たすかどうか
                ans.append(new)
                
        return ans
