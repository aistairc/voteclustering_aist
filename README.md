# voteclustering_aist
A version of voteclustering that is developed and maintained by AIST.

## 環境
- [Docker Desktop Community](https://www.docker.com/products/docker-desktop) Version `2.0.0.2` (30215)
  - Engine: `18.09.1`
  - Compose: `1.23.2`
- python 3.7

## ディレクトリ構成
```
.
├── README.md                       # 本ファイル
├── Makefile                        # 各種操作実行用コマンドが記述されたMakefile (コマンドの一覧は`$ Make help`で確認可能)
├── PULL_REQUEST_TEMPLATE.md
├── .gitignore
├── docker-compose.yml              # 開発環境・本番環境共通のdocker-compose用設定が記述されたファイル
├── docker-compose.development.yml  # 開発環境用のdocker-compose用設定が記述されたファイル
├── docker-compose.production.yml   # 本番環境用のdocker-compose用設定が記述されたファイル
├── container.env
├── nginx/
├── docs
│   ├── assets/                     # ドキュメントのための画像など
│   ├── api_document_src/           # API blueprint形式で記述されたwebAPIのドキュメント
│   ├── webAPI.html                 # api_document_src/の内容をレンダラーによりHTMLに変換したファイル
│   ├── development_manual.md       # 開発環境に関するマニュアル
│   ├── production_manual.md        # 本番環境に関するマニュアル
│   ├── manage_ERD_manual.md        # テーブル定義書の編集・更新に関するマニュアル
│   ├── docker_manual.md            # Dockerに関するマニュアル
│   ├── makefile_manual.md          # Makefileに記述されているコマンドの使い方に関するマニュアル
│   ├── translate_manual.md         # 多言語対応作業の手順に関するマニュアル
│   └── table_definition.md         # データベースのテーブル定義書
└── django
    ├── manage.py
    ├── requirements.txt
    ├── Dockerfile
    ├── .editorconfig
    ├── media/                      # メディアファイルの保存先
    ├── config/                     # Djangoの設定ファイル群
    ├── manage_ERD/                 # ER図を作成するためのファイル群
    ├── AIST_survey/                # アンケートアプリケーション本体
    ├── dashboard/                  # アンケートの集計結果を表示するアプリケーション 
    └── make_enquete_setting/       # 新規アンケートを作成するためのアプリケーション
```

## ウェブサイトURL
- `.../admin`
  - Adminページ
- `.../enquete/{unique_url}`
  - アンケートアプリ
- `.../make_enquete_setting`
  - アンケート作成アプリ
- `.../dashboard`
  - アンケートの集計結果を表示するアプリ
- `...:9000/` (開発環境のみ)
  - phpMyAdmin

----

## セットアップ手順

### 前提条件

[Get Started with Docker | Docker](https://www.docker.com/get-started) より、各自の OS にあった Docker Desktop をインストールしておく必要があります。

### リポジトリのクローン
```sh
$ git clone https://github.com/aistairc/voteclustering_aist.git
$ cd voteclustering_aist
```
### 環境設定用ファイルである`/django/.env`, `/container.env`の内容を変更

初めは`/django/.env`と`/container.env`には仮の設定値が入っているので、適宜設定値を変更します。

/django/.envの初めの内容

```
DEBUG=True
ALLOWED_HOSTS=localhost
SECRET_KEY=admin_secret_key
DATABASES_NAME=admin_database
DATABASES_PASSWORD=admin_password
DATABASES_USER=admin_user

```

/container.envの初めの内容

```
MYSQL_ROOT_PASSWORD=admin_root_password
MYSQL_DATABASE=admin_database
MYSQL_USER=admin_user
MYSQL_PASSWORD=admin_password

```

- 本番環境ではDEBUGをFalseに設定してください。

- ALLOWED_HOSTSには公開するドメイン名やIPアドレスを設定してください。

- 「DATABASES_NAMEとMYSQL_DATABASE」、「DATABASES_PASSWORDとMYSQL_PASSWORD」、「DATABASES_USERとMYSQL_USER」の組み合わせには同じ値を設定してください。

- SECRET_KEY、MYSQL_ROOT_PASSWORD、MYSQL_PASSWORDには第三者に推測されにくい値（ランダムな文字列など）を設定してください。

### Dockerの起動
```sh
$ make up-prod
```

### `django/package.json`内に記述した`all`コマンドを実行
```sh
$ make yarn-all
```

### データベースの構築
```sh
$ make migrate
```

### 翻訳テキストの反映
```sh
$ make compilemessages
$ make restart-prod
```

### スーパーユーザーの設定（Adminページに入る際に必要）
```sh
$ make create-superuser username=admin email=admin@example.com
```

### 起動中のコンテナを停止する
```sh
$ docker-compose down
```

### 次回以降の起動

`make up-prod` を実行するだけで、前回終了時と同じ状態で利用を始めることができます。

### Makeコマンドの詳細
[docs/makefile_manual.md](docs/makefile_manual.md) を参照
