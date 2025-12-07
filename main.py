import sys # 入力と再帰回数上限

# グラフ描画
import networkx as nx 
import matplotlib.pyplot as plt

import numpy as np # 重みのランダム生成

from copy import deepcopy # オブジェクトのコピー

# 同階層のファイルの読み込み
from ford_fulkerson import *
from zdd_max_flow import *
from min_st_cut import *
from scc import *
from all_min_st_cuts import *
from zdd_all_min_st_cuts import *

# sys.setrecursionlimit(n+m) # 再帰の回数上限を変更（デフォルトは1000）

# ランダムグラフ生成
def generate_random_graph(n):
    # 有向連結単純グラフの生成
    while True:
        # ランダムなグラフを生成（頂点数、任意の2頂点に辺が生える確率、有向か）
        # random_graph
        rnd_g = nx.fast_gnp_random_graph(n, 0.025, directed=True)
        if nx.is_connected(rnd_g.to_undirected()):
            break
    
    # 辺に重みをつける
    rng = np.random.default_rng()
    for a,b in rnd_g.edges():
        rnd_g[a][b]["weight"] = rng.integers(1,50,dtype=np.int64)
    print(rnd_g)
    return rnd_g

# グラフ描画
def draw_graph(g):
    pos = nx.spring_layout(g,seed=42) # sl_seed
    # node_labels = {node:node+1 for node in g.nodes()} # ノードラベルを1-indexに
    node_labels = {node:node for node in g.nodes()} # ノードラベルを0-indexに
    nx.draw(g,pos=pos,with_labels=True,labels=node_labels,arrows=True) # ノード描画

    edge_labels = nx.get_edge_attributes(g,"weight")
    nx.draw_networkx_edge_labels(g,pos=pos,edge_labels=edge_labels) # 辺描画

    plt.show()

# 最大流
def ff_max_flow(n:int, edges:list, s:int, t:int):
    ff = FordFulkerson(n) # インスタンス生成
    max_flow, before_res_g, after_res_g = ff.max_flow(n, edges, s, t)
    return max_flow, before_res_g, after_res_g

def zdd_max_flow(n:int, edges:list, s:int, t:int):

    zmf = ZddMaxFlow(n)

    universe = set()
    for a,b,c in edges:
        zmf.add_edge(a,b,c)

        universe.add((a,b))
        universe.add((b,a))

    # 有向グラフセット生成
    DGS.set_universe(universe)
    
    # stパスを列挙（増加道）
    st_paths = DGS.directed_st_paths(s,t)
    
    max_flow = zmf.max_flow(st_paths)
    return max_flow, st_paths

# 1つの最小カット辺集合
def min_st_cut(after_res_g:list, s:int):
    # msc = MinStCut(max_flow, after_residual_g)
    # fw_edges = msc.forward_edges(after_residual_g)
    # fw_graph = msc.forward_graph(fw_edges)

    # S,T = smc.recursive_dfs()
    # S,T = smc.stack.dfs()
    # S,T = smc.bfs()

    # min_st_cut_edges = smc.min_st_cut_edges()
    # return min_st_cut_edges

    # 以下は動く
    # msc = MinStCut(max_flow, after_residual_g)
    # forward_edges = msc.forward_edges(after_residual_g)
    # forward_g = msc.build_forward_graph(forward_edges)
    # print("forward_graph =", forward_g)
    # visited = [False]*len(g)
    # S = {s}
    # print(msc.recursive_dfs(0,visited,s,S))
    # print(msc.stack_dfs(s))
    # print(msc.bfs(s))
    # print(msc.min_st_cut_edges(s))

    msc = MinStCut(after_res_g)
    min_st_cut_edges = msc.min_st_cut_edges(s)
    return min_st_cut_edges

def decompose_scc(after_res_g):
    scc = Scc(after_res_g)
    scc, dag, topological_dag = scc.decompose()
    return scc, dag, topological_dag

def all_min_st_cuts(s_order, t_order, dag, inv_dag):
    amsc = AllMinStCuts(s_order, t_order, dag, inv_dag)
    all_min_st_cuts = amsc.solver()
    return all_min_st_cuts

def zdd_all_min_st_cuts():
    zamsc = ZddAllMinStCuts()
    zamsc.closure()
    return

def main():
    # 入力
    # 固定グラフ
    edges = [
    (0,1,3),
    (0,2,10),
    (0,3,16),
    (0,4,6),
    (1,5,5),
    (2,1,2),
    (2,5,3),
    (2,9,4),
    (2,7,2),
    (2,3,1),
    (3,7,3),
    (4,3,1),
    (4,7,5),
    (4,8,6),
    (5,9,9),
    (6,5,2),
    (6,7,4),
    (6,11,2),
    (7,3,3),
    (8,7,4),
    (8,12,3),
    (8,13,4),
    (9,13,12),
    (10,6,7),
    (10,9,2),
    (10,13,4),
    (11,8,3),
    (11,10,1),
    (11,12,2),
    (11,13,11),
    (12,13,3)
    ]
    
    # ランダムグラフ
    # n = 100
    # g = generate_random_graph(n)
    # m = g.number_of_edges()
    # edges =  [(a,b,data["weight"]) for a,b,data in g.edges(data=True)]
    # edges = [(a,b,weight) for a,b,weight in g.edges(data="weight")]

    # n = 14
    # m = len(edges)
    # # 容量付きグラフを作成
    # g = nx.DiGraph()
    # for a,b,capacity in edges :
    #     g.add_edge(a,b,capacity=capacity)

    n = 14
    s, t = 0, n-1

    mf, before_res_g, after_res_g = ff_max_flow(n, edges, s, t)
    print("max_flow =", mf)
    # print("after_res_g =", after_res_g)
    # mf,st_paths = zdd_max_flow(n,edges)
    # print("st_paths.len() =",st_paths.len())

    min_st_cut_edges = min_st_cut(after_res_g, s)
    print("min_st_cut_edges =", min_st_cut_edges)
    
    # stパスの各辺の出現回数
    # d = {}
    # for path in st_paths:
    #     # print(path)
    #     for a,b in path:
    #         if (a,b) not in d:
    #             d[(a,b)] = 1
    #         else:
    #             d[(a,b)] += 1
    # print(d)

    sub_arg = [[] for _ in range(n)]
    for i,v in enumerate(after_res_g):
        for edge in v:
            if edge.cap == 0:
                continue
            sub_arg[i].append(edge.to)
    print("sub_arg =", sub_arg)

    scc, dag, topological_dag = decompose_scc(sub_arg)
    print("scc =", len(scc), scc)
    print("dag = ", dag)
    print("topological_dag =", topological_dag)


    zddmf, st_paths = zdd_max_flow(n, edges, s, t)
    print("zddmf =", zddmf, st_paths)

    s_order = -1; t_order = -1
    for i, adj in enumerate(scc):
        if s in set(adj):
            s_order = i
        if t in set(adj):
            t_order = i
    print(s_order, t_order)

    inv_dag = [[] for _ in range(len(dag))]
    for i, adj in enumerate(dag):
        for j in adj:
            inv_dag[j].append(i)
    
    ans = all_min_st_cuts(s_order, t_order, dag, inv_dag)
    print("ans =", ans)

    # s_visitedがTrueである頂点は必ず解に含まれる
    # t_visitedがTrueである頂点は必ず除く

    # zdd_all_st_min_cuts = zdd_all_min_st_cuts()
    # print(zdd_all_st_min_cuts)
    # draw_graph(g)

if __name__ == "__main__":
    main()