from graphillion import DiGraphSet as DGS

class ZddAllMinStCuts:

    def __init__(self):
        self.gs = None

    def build_zdd(self, scc: list[list[int]], dag: list[list[int]], topological_dag: list[int]):

        # DAGのすべての頂点に自己ループを追加
        for i, adj in enumerate(dag):
            adj.append(i)
        
        #gsにトポロジカルソート順に、sccの辺を追加
        universe = []
        for order in topological_dag:
            for v in dag[order]:
                universe.add((order, v))
        
        # universe = [(i, j) for i, adj in enumerate(dag) for j in adj]
        gs = DiGraphSet(universe)
    
    # すべての最小カットを求める
    def all_min_st_cuts(self, ):
        # u = intersect(sを含む連結成分)
        # v = diff(tを含む連結成分)

        # dagの辺に対して、uを含みかつvを含まないような連結成分の組み合わせ
        # includeとexcludeを使って上手くやる
         
        # return すべての最小カットの具体例
        return
    
    def closure():
        # build_zdd()
        # all_min_st_cuts()
        return