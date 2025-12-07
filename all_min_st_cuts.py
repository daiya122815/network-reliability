class AllMinStCuts:

    def __init__(self):
        a = 0

    def build_zdd(self, scc: list[list[int]], s_order: int, t_order: int, dag: list[list[int]], topological_dag: list[int]):

        # s_order = sを含むscc成分のインデックス t_orderも同じ
        stack = [s_order]
        s_visited = [False] * len(dag)
        s_visited[s_order] = True
        while stack:
            cur = stack.pop()
            for nxt in dag[cur]:
                if not s_visited[nxt]:
                    s_visited[nxt] = True
                    stack.append(nxt)
        
        stack = [t_order]
        t_visited = [False] * len(dag)
        t_visited[t_order] = True
        while stack:
            cur = stack.pop()
            t_visited[cur] = True
            for nxt in dag[cur]:
                if not t_visited[nxt]:
                    t_visited[nxt] = True
                    stack.append(nxt)

    def closure():
        # build_zdd()
        # all_min_st_cuts()
        return    
    
    # すべての最小カットを求める
    def all_min_st_cuts(self, ):
        return
