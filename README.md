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
    ├── api/                        # webAPI用アプリケーション
    ├── dashboard/                  # アンケートの集計結果を表示するアプリケーション 
    └── make_enquete_setting/       # 新規アンケートを作成するためのアプリケーション
```

## ブランチ
git flowに従ってブランチを作成する
- `master`: 本番環境に適用するさいにマージされるブランチ
- `develop`: 開発を進めるためのメインとなるブランチ
- `feature/*`: 機能開発を進める際に利用するブランチ（対応するissueが存在する場合はprefixとしてissue番号を付けること）
- `hotfix/*`: 緊急のバグ対応を行う際にmasterから切るブランチ（対応するissueが存在する場合はprefixとしてissue番号を付けること）
- `release/*`: リリース作業を行うブランチ　現在は特に作業は存在しない（ブランチ名にはバージョンを用いること）

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

## 簡単セットアップ

環境を容易にセットアップするツールの利用方法について説明します。

### 前提条件

[Get Started with Docker | Docker](https://www.docker.com/get-started) より、各自の OS にあった Docker Desktop をインストールしておく必要があります。

### 事前準備

`docs/development_manual.md` にも記載があるとおり、あらかじめ 2 つの環境ファイルを用意しておく必要があります。

- `/django/.env`
- `/container.env`

.envの内容

```
DEBUG=
ALLOWED_HOSTS=
SECRET_KEY=
DATABASES_NAME=
DATABASES_PASSWORD=
DATABASES_USER=
```

container.envの内容

```
MYSQL_ROOT_PASSWORD=
MYSQL_DATABASE=
MYSQL_USER=
MYSQL_PASSWORD=
```

設定ファイルとして提供されるサンプルを参考に、適宜設定値を変更します。

### ツールの構成

ルートディレクトリにはツールの本体となるバイナリファイルが置かれています。

- cli-darwin-amd64 — macOS 用の CLI ツール
- cli-linux-amd64 — Linux 用の CLI ツール
- cli-windows-amd64 — Windows 用の CLI ツール

いずれも、64 bit OS 用のバイナリです。32 bit 環境では動作しないことに注意してください。

そして `tools` ディレクトリ以下に OS ごとのバッチファイルを用意しています。

```
tools
├── linux
├── mac
└── windows
```

OS ごとのディレクトリには、次のようなファイルが置かれています (Windows の例)。

```
tools
└── windows
    ├── collectstatic.bat
    ├── compilemessages.bat
    ├── createsu.bat
    ├── generateerd.bat
    ├── logall.bat
    ├── logdjango.bat
    ├── makemessages.bat
    ├── migrate.bat
    ├── restart.bat
    ├── setup.bat
    ├── start-dev.bat
    ├── start-prod.bat
    └── stop.bat
```

### ツールの使い方

#### 初めて起動する

`start-dev.bat` (Windows の場合) を起動します。初回起動時は、Docker コンテナをゼロから構築するため、20分〜30分程度の時間を要します (ネットワーク環境や端末による)。正常に完了すると、ターミナル画面には Django、MySQL そして phpMyAdmin が起動したことを示すログが出力されます。この画面は停止せず、そのままの状態を保ってください。

次に、環境の初期セットアップのために `setup.bat` を起動します。途中で、管理者の名前とメールアドレスの入力が求められます。これは、Django の管理画面にログインする管理者となります。

```
username: admin
email: admin@example.com
```

上のように設定します。パスワードは一律固定で `admin` としていますので、環境構築後すぐに管理画面よりパスワード変更を行ってください。

管理者作成を完了すると、ブラウザから管理画面にアクセスすることができます。

http://localhost/admin/

にアクセスしてみましょう。

#### 起動中のコンテナを停止する

`stop.bat` を起動します。

#### 次回以降の起動

`start-dev.bat` を起動するだけで、前回終了時と同じ状態で利用を始めることができます。

#### すべてのバッチファイルの説明

- collectstatic.bat — 静的コンテンツを収集する
- createsu.bat — 管理者ユーザを作成する
- generateerd.bat — ERD を作成する
- logall.bat — Django, MySQL, phpMyAdmin のログを一括で表示する
- logdjango.bat — Django のみのログを表示する
- makemessages.bat — 翻訳用テキストファイルを作成する
- compilemessages.bat — 翻訳用テキストファイルをコンパイルする
- migrate.bat — Django のマイグレーションファイルに基づいてデータベースを更新する
- restart.bat — コンテナを再起動する
- setup.bat — 起動したコンテナの初期セットアップを実行する
- start-dev.bat — `docker-compose.development.yml` を利用してコンテナを起動する
- start-prod.bat — `docker-compose.production.yml` を利用してコンテナを起動する
- stop.bat — 起動中のコンテナを停止する
