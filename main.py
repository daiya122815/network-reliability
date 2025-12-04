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

# def zdd_max_flow(n:int, edges:list):

#     zmf = ZddMaxFlow(n)

#     universe = set()
#     for a,b,c in edges:
#         zmf.add_edge(a,b,c)

#         universe.add((a,b))
#         universe.add((b,a))

#     # 有向グラフセット生成
#     DGS.set_universe(universe)
    
#     # stパスを列挙（増加道）
#     s,t = 0, n-1
#     st_paths = DGS.directed_st_paths(s,t)
    
#     mf = zmf.max_flow(st_paths)
#     return mf,st_paths

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

def decompose_scc(g):
    scc = Scc(g)
    scc, dag, topological_dag = scc.decompose()
    return scc, dag, topological_dag

def main():
    # 入力
    # 固定グラフ
    # n,m = map(int,input().split()) # 頂点数、辺数
    # edges = set()
    # for _ in range(m):
    #     a,b,c = map(int,input().split())
    #     a -= 1
    #     b -= 1
    #     edges.add((a,b,c))
    # 0-index
    # edges = [
    #     (0,6,1),
    #     (1,0,1),
    #     (1,17,1),
    #     (2,1,1),
    #     (3,13,1),
    #     (3,4,1),
    #     (4,14,1),
    #     (4,22,1),
    #     (5,15,1),
    #     (6,5,1),
    #     (6,16,1),
    #     (7,18,1),
    #     (8,7,1),
    #     (9,2,1),
    #     (9,3,1),
    #     (9,11,1),
    #     (9,13,1),
    #     (10,8,1),
    #     (10,19,1),
    #     (11,10,1),
    #     (11,12,1),
    #     (12,13,1),
    #     (12,20,1),
    #     (13,14,1),
    #     (13,26,1),
    #     (14,21,1),
    #     (15,55,1),
    #     (16,15,1),
    #     (16,23,1),
    #     (17,16,1),
    #     (18,17,1),
    #     (18,19,1),
    #     (19,28,1),
    #     (20,19,1),
    #     (20,25,1),
    #     (21,22,1),
    #     (21,31,1),
    #     (22,36,1),
    #     (23,32,1),
    #     (23,45,1),
    #     (24,23,1),
    #     (25,28,1),
    #     (25,29,1),
    #     (26,25,1),
    #     (27,24,1),
    #     (28,33,1),
    #     (29,30,1),
    #     (29,39,1),
    #     (30,31,1),
    #     (30,39,1),
    #     (31,35,1),
    #     (32,37,1),
    #     (33,32,1),
    #     (34,30,1),
    #     (34,40,1),
    #     (35,34,1),
    #     (35,44,1),
    #     (36,35,1),
    #     (36,61,1),
    #     (37,38,1),
    #     (37,46,1),
    #     (38,41,1),
    #     (39,38,1),
    #     (39,42,1),
    #     (39,43,1),
    #     (40,39,1),
    #     (41,42,1),
    #     (41,46,1),
    #     (42,51,1),
    #     (43,48,1),
    #     (44,43,1),
    #     (44,54,1),
    #     (45,46,1),
    #     (46,50,1),
    #     (46,51,1),
    #     (47,51,1),
    #     (47,58,1),
    #     (48,47,1),
    #     (49,56,1),
    #     (50,49,1),
    #     (50,57,1),
    #     (52,59,1),
    #     (53,48,1),
    #     (53,52,1),
    #     (54,53,1),
    #     (55,56,1),
    #     (56,57,1),
    #     (57,51,1),
    #     (57,58,1),
    #     (58,51,1),
    #     (59,58,1),
    #     (60,53,1),
    #     (61,60,1)
    # ]
    # n = 62
    # m = len(edges)
    
    # ランダムグラフ
    n = 100
    g = generate_random_graph(n)
    m = g.number_of_edges()
    edges =  [(a,b,data["weight"]) for a,b,data in g.edges(data=True)]
    edges = [(a,b,weight) for a,b,weight in g.edges(data="weight")]

    # n = 14
    # m = len(edges)
    # # 容量付きグラフを作成
    # g = nx.DiGraph()
    # for a,b,capacity in edges :
    #     g.add_edge(a,b,capacity=capacity)

    s, t = 0, len(g)-1

    mf, before_res_g, after_res_g = ff_max_flow(n, edges, s, t)
    print("max_flow =", mf)
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

    # edges = [
    #     (0,1),
    #     (1,2),
    #     (2,0),
    #     (2,3),
    #     (3,4),
    #     (4,3),
    #     (4,5),
    #     (4,6)
    # ]
    # n = 7
    # g = [[] for _ in range(n)]
    # for edge in edges:
    #     u,v = edge
    #     g[u].append(v)
    
    scc, dag, topological_dag = decompose_scc(g)
    print("scc =", len(scc), scc)
    print(dag)
    print(topological_dag)
    
    # draw_graph(g)

if __name__ == "__main__":
    main()