import sys # 入力と再帰回数

"""グラフ描画"""
import networkx as nx 
import matplotlib.pyplot as plt

import numpy as np # 重みのランダム生成

"""同階層のファイルの読み込み"""
from ford_fulkerson import *
from zdd_max_flow import *
from min_st_cut import*

# class Graph():
#     def generate_graph():
#     def generate_random_graph():

# グラフ生成
# def generate_graph(n):

# ランダムグラフ生成
# def generate_random_graph(n):
#     # 有向連結単純グラフの生成
#     while True:
#         # ランダムなグラフを生成（頂点数、任意の2頂点に辺が生える確率、有向か）
#         rg = nx.fast_gnp_random_graph(n,0.5,directed=True)
#         if nx.is_connected(rg.to_undirected()):
#             break
    
#     # 辺に重みをつける
#     rng = np.random.default_rng()
#     for a,b in rg.edges():
#         rg[a][b]["weight"] = rng.integers(1,11,dtype=np.int64)
#     print(rg)
#     return rg

# グラフ描画
# def draw_graph(g):
#     pos = nx.spring_layout(g,seed=42) # sl_seed
#     # node_labels = {node:node+1 for node in g.nodes()} # ノードラベルを1-indexに
#     node_labels = {node:node for node in g.nodes()} # ノードラベルを0-indexに
#     nx.draw(g,pos=pos,with_labels=True,labels=node_labels,arrows=True) # ノード描画

#     edge_labels = nx.get_edge_attributes(g,"weight")
#     nx.draw_networkx_edge_labels(g,pos=pos,edge_labels=edge_labels) # 辺描画

#     plt.show()

"""最大流"""
def ford_fulkerson():
    # 頂点数、辺数
    n,m = map(int,input().split())

    # 再帰の回数上限を変更（デフォルトは1000）
    sys.setrecursionlimit(n+m)
    
    # インスタンス生成
    ff = FordFulkerson(n)
    
    # 各辺の入力
    for _ in range(m):
        a,b,c = map(int,input().split())
        a -= 1
        b -= 1
        # 辺の追加（逆辺も）
        ff.add_edge(a,b,c) # 各頂点は、構造体（num,cap,rev）からなる
    
    # グラフの表示
    # print(vars(ff))
    
    s,t = 0, n-1
    mf = ff.max_flow(s,t)
    
    return mf

def zdd_max_flow(n,edges):

    zmf = ZddMaxFlow(n)

    universe = set()
    for a,b,c in edges:
        zmf.add_edge(a,b,c)

        universe.add((a,b))
        universe.add((b,a))

    # 有向グラフセット生成
    DGS.set_universe(universe)
    
    # stパスを列挙（増加道）
    s,t = 0, n-1
    st_paths = DGS.directed_st_paths(s,t)
    
    mf = zmf.max_flow(st_paths)
    return mf,st_paths

"""1つの最小カット辺集合"""
def min_st_cut():
    smc = min_st_cut()
    return 0

def main():

    # n = int(input())
    # g = generate_random_graph(n)
    # m = g.number_of_edges()
    # # edges =  [(a,b,data["weight"]) for a,b,data in g.edges(data=True)]
    # edges = [(a,b,weight) for a,b,weight in g.edges(data="weight")]

    edges = {(0,1,1),
             (1,2,1),
             (2,3,1),
             (3,4,1),
             (4,5,1),
             (5,6,1),
             (6,7,1), 
             (8,7,1), 
             (0,8,1), 
             (7,13,1),
             (2,9,1),
             (9,10,1),
             (10,11,1),
             (11,12,1),
             (12,13,1)
    }

    n = 14
    m = len(edges)
    # 容量付きグラフを作成
    g = nx.DiGraph()
    for a,b,capacity in edges :
        g. add_edge (a,b,capacity=capacity)

    print("n =",n)
    print("m =",m)

    # mf = ford_fulkerson()
    mf,st_paths = zdd_max_flow(n,edges)
    print("max_flow =",mf)
    print("st_paths.len() =",st_paths.len())
    
    # stパスの各辺の出現回数
    d = {}
    for path in st_paths:
        # print(path)
        for a,b in path:
            if (a,b) not in d:
                d[(a,b)] = 1
            else:
                d[(a,b)] += 1
    print(d)
    
    # set_min_cut(mf,st_paths)
    
    # draw_graph(g)

if __name__ == "__main__":
    main()