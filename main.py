import sys

# 同階層のファイルの読み込み
from ford_fulkerson import *
from zdd_max_flow import *

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
    ans = ff.max_flow(s,t)
    print(ans)

def zdd_max_flow():
    n,m = map(int,input().split())
    zmf = ZddMaxFlow(n)

    universe = []
    for _ in range(m):
        a,b,c = map(int,input().split())
        a -= 1
        b -= 1
        zmf.add_edge(a,b,c)

        universe.append((a,b))
        universe.append((b,a))

    # universeが辺（v1,v2）でないといけないから、今のedge(a,b,c)の形から変形して渡したい
    # 有向グラフセット生成
    DGS.set_universe(universe)
    
    # stパスを列挙（増加道）
    s,t = 0, n-1
    paths = DGS.directed_st_paths(s,t)
        
    ans = zmf.max_flow(paths)
    print(ans)

def main():
    # ford_fulkerson()
    zdd_max_flow()

if __name__ == "__main__":
    main()