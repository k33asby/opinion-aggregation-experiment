# 意見集約法の比較

## 概要
研究で行なったシュミレーションのコードである。jupyter notebookを用いて実験を行なった。精度と時間のトレードオフ関係において最適な意見集約法を決定する。~~コードが荒れまくってるのでもう見たくもない。~~
[Python3でLRUキャッシュを用いてプログラムを高速化
](https://qiita.com/k33asby/items/4d471932e299edd08b24)
[Python3でポアソン分布、ガンマ分布](https://qiita.com/k33asby/items/cb5857c7d96dae6832c6)
## 主な構成
* py/opinion-aggregation-experiment.ipynb
メインで用いたjupyter notebookのファイル
* py/theory.py
py/opinion-aggregation-experiment.ipynbの元となる理論のファイル
* rb/
最初はrubyで書いていたが途中からpythonに変えた
こちらでは理論ではなく実際に何度も試行を繰り返すことによって数値を得ている

## 一部の結果
こんな感じのものを出力した。         

<img src="https://user-images.githubusercontent.com/31947384/36298766-0db7d2f6-133d-11e8-909b-700693dfd76a.png" width="70%">          

<img src="https://user-images.githubusercontent.com/31947384/36298751-ffa832aa-133c-11e8-8f46-a50c39ac40f3.png" width="70%">
