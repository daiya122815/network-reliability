import sys # 入力と再帰回数

# グラフ描画
import networkx as nx 
import matplotlib.pyplot as plt

import numpy as np # 重みのランダム生成

# 同階層のファイルの読み込み
from ford_fulkerson import *
from zdd_max_flow import *
from set_min_cut import*

# グラフ生成
def generate_graph(n):
    # 有向連結単純グラフの生成
    while True:
        # ランダムなグラフを生成（頂点数、任意の2頂点に辺が生える確率、有向か）
        g = nx.fast_gnp_random_graph(n,0.1,directed=True)
        if nx.is_connected(g.to_undirected()):
            break
    
    # 辺に重みをつける
    rng = np.random.default_rng()
    for a,b in g.edges():
        g[a][b]["weight"] = rng.integers(1,11,dtype=np.int64)
    
    return g

# グラフ描画
def draw_graph(g):
    pos = nx.spring_layout(g,seed=42) # sl_seed
    node_labels = {node:node+1 for node in g.nodes()} # ノードラベルを1-indexに
    nx.draw(g,pos=pos,with_labels=True,labels=node_labels,arrows=True) # ノード描画

    edge_labels = nx.get_edge_attributes(g,"weight")
    nx.draw_networkx_edge_labels(g,pos=pos,edge_labels=edge_labels) # 辺描画

    plt.show()

# 実行
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

def main():

    n = int(input())
    g = generate_graph(n)
    m = g.number_of_edges()
    # edges =  [(a,b,data["weight"]) for a,b,data in g.edges(data=True)]
    edges = [(a,b,weight) for a,b,weight in g.edges(data="weight")]


    """
    n,m = map(int,input().split())
    edges = []
    for _ in range(m):
        a,b,c = map(int,input().split())
        a -= 1
        b -= 1
        edges.append((a,b,c))
    """
        
    # mf = ford_fulkerson()
    mf,st_paths = zdd_max_flow(n,edges)
    print(mf,st_paths)
    # set_min_cut(mf,st_paths)
    
    draw_graph(g)

if __name__ == "__main__":
    main()