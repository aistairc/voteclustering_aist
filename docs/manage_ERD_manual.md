# ER図の作成

### テーブル定義関連のファイル群

| ディレクトリ | ファイル名           | 説明                                            |
|-----------|----------------------|-------------------------------------------------|
| docs/ | table_definition.md  | テーブル定義書本体                              |
| django/manage_ERD/ | generate_ERD.py      | table_definition.erからER図を生成するスクリプト |
| django/manage_ERD/ | table_definition.er  | ER図生成用設定ファイル                          |
| django/manage_ERD/ | table_definition.png | スクリプトによって生成されたER図の画像          |

### 作成手順

-  Dockerを起動
```sh
$ make up-dev
```

- スクリプトを実行し，ER図の画像を出力
```sh
$ make generate-ERD
```
