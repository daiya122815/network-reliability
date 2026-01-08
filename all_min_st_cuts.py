class AllMinStCuts:

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
        t_visited = self.stack_dfs(self.t_idx, self.rev_dag) # rev_dag（dagと逆方向）

        # sから到達可能頂点は、必ず解に含む
        # tから到達可能頂点は、含んではならない
        include = {v for v, ok in enumerate(s_visited) if ok}
        exclude = {v for v, ok in enumerate(t_visited) if ok}

        # sとtの両方から到達不可能である頂点を取り出す
        sol_cand_vtx = []
        for v, (s,t) in enumerate(zip(s_visited, t_visited)):
            if not (s or t):
                sol_cand_vtx.append(v)
        
        return include,exclude,sol_cand_vtx
    
    def is_closed(self, vtx:set[int]) -> bool:
        stack = list(vtx)
        flag = False
        while stack:
            cur = stack.pop()
            for nxt in self.dag[cur]:
                if nxt not in vtx:
                    flag = True
                    break
                else:
                    stack.append(nxt)
            if flag:
                return False
        return True
    
    # すべての最小カットを求める
    def solver(self):
        include,exclude,sol_cand_vtx = self.get_cand_vtx()

        all_min_st_cuts = []
        # bit全探索なので、nが小さい場合のみ有効
        n = len(sol_cand_vtx)
        for mask in range(1<<n):
            new = set(include)
            for bit in range(n):
                if (mask>>bit) & 1:
                    new.add(sol_cand_vtx[bit])
            
            if new & exclude: # 新たな解とexcludeに共通部分がある場合は新たな解でない
                continue
            if self.is_closed(new): # 新たな解が閉包を満たすかどうか
                all_min_st_cuts.append((new,set(range(len(self.dag)))-new))
                
        return all_min_st_cuts
