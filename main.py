import sys

# 同階層のファイルの読み込み
from ford_fulkerson import *

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

def main():
    ford_fulkerson()
if __name__ == "__main__":
    main()