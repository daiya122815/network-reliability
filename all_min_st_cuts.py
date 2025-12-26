class AllMinStCuts:

    def __init__(self, s_idx: int, t_idx: int, dag: list[list[int]], inv_dag: list[list[int]]):
        self.s_idx = s_idx
        self.t_idx = t_idx
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

        # s_idx sを含むscc連結成分のインデックス t_idxも同様
        # s_visited s_idxから到達可能頂点
        s_visited = self.stack_dfs(self.s_idx, self.dag)
        t_visited = self.stack_dfs(self.t_idx, self.inv_dag)

        # sから到達可能頂点は、必ず解に含む
        # tから到達可能頂点は、含んではならない。
        self.include = {v for v, ok in enumerate(s_visited) if ok}
        self.exclude = {v for v, ok in enumerate(t_visited) if ok}

        # sとtの両方から到達不可能である頂点を取り出す。
        for v, (s, t) in enumerate(zip(s_visited, t_visited)):
            if not (s or t):
                self.sol_set.append(v)
    
    def is_closed(self, nodes: set[int]) -> bool:

        stack = list(nodes)
        flag = False
        while stack:
            cur = stack.pop()
            for nxt in self.dag[cur]:
                if nxt not in nodes:
                    flag = True
                    break
                else:
                    stack.append(nxt)
            if flag:
                return False
        return True

    
    # すべての最小カットを求める
    def solver(self):
        self.get_cand_vtx()

        all_min_st_cuts = []
        # bit全探索なので、nが小さい場合のみ有効
        n = len(self.sol_set)
        for mask in range(1<<n):
            new = set(self.include)
            for bit in range(n):
                if (mask>>bit) & 1:
                    new.add(self.sol_set[bit])
            
            if new & self.exclude: # 新たな解とexcludeに共通部分がある場合は新たな解でない
                continue
            if self.is_closed(new): # 新たな解が閉包を満たすかどうか
                all_min_st_cuts.append((new,set(range(len(self.dag)))-new))
                
        return all_min_st_cuts
