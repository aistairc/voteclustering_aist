 Sankey Diagram
pickleされた回答データを自動で集計し、D3 Sankey Diagramを表示するプログラムです。

## ファイル構成
| ファイル                         | 説明                                                                                         |
| -------------------------------- | -------------------------------------------------------------------------------------------- |
| index.html                       | D3 SankeyDiagramを表示するHTMLファイルです。sankey-diagram-data-structure.jsを読みます。     |
| shukei.py                        | pickleファイルを読み込み、sankey-diagram-data-structure.jsを出力します。                     |
| sankey-diagram-data-structure.js | index.htmlでD3 SnakeyDiagramを表示するために読み込む回答集計したデータ構造を定義しています。shukei.pyによって自動生成されます。 |
| d3-sankey-diagram/               | D3 SankeyDiagram本体。index.htmlで読み込みます。                                                                         |

## 使用方法
1. 事前準備：pickleした回答データ用意。
2. `shukei.py`を実行する。
    *  実行時に1.のファイルのパスを入力します。
    * 完了すると`sankey-diagram-data-structure.js`が自動生成されます。
4. index.htmlを表示するとD3 SankyDiagram形式で集計結果が表示されます。
    * 図を保存する際は、ファイル形式を選択し保存ボタンを押してください。
