# django-docker-boilerplate

[Docker](https://www.docker.com/) コンテナ上で [Django](https://www.djangoproject.com/) アプリケーションを開発するためのテンプレートプロジェクトです。

_筆者の環境が macOS であるため、本ドキュメントは macOS 前提での記述となっています。Windows や Linux を使用する場合には適宜読み替えてください。_

## 全体概要

![Django on Docker Container](/docs/assets/Django-on-Docker-Container.png)

## 事前に必要なもの

- [Docker Desktop Community](https://www.docker.com/products/docker-desktop) Version 2.0.0.2 (30215)
  - Engine: 18.09.1
  - Compose: 1.23.2

## 新規に Django プロジェクトおよびアプリケーションを作成する

Django プロジェクトおよびアプリケーションを開始する方法は[オフィシャルドキュメント](https://docs.djangoproject.com/ja/2.1/intro/tutorial01/)に記載されています。ただし、このテンプレートプロジェクトから開始する Django プロジェクトおよびアプリケーションではは `docker-compose run` や `docker-compose exec` を通じてコマンド実行する必要があります。

初期段階では次のようなディレクトリ・ファイル構成になっています。

```text
.
├── README.md               # このファイル
├── django
│   ├── Dockerfile          # Django コンテナの定義
│   ├── project_template    # Django プロジェクト作成時に使用するテンプレート
│   └── requirements.txt    # Django コンテナに pip install する外部ライブラリ定義
└── docker-compose.yml      # 複数の Docker コンテナと関連を定義
```

### 新規 Django プロジェクトの作成

```sh
docker-compose run --rm django django-admin startproject --template project_template {PROJECT_NAME} .
```

- `PROJECT_NAME`: 任意のプロジェクト名を指定します

例えば "djangoproject" という名前のプロジェクトを作成するときには次のようにします。コマンドの最後に指定している `.` (ドット) は Docker コンテナ上におけるカレントディレクトリを示しており、ホスト OS 上では `docker` ディレクトリです。

_MySQL の接続情報であるデータベース名、ユーザ名、パスワードはいずれも "djangoproject" という文字列で固定しています。これらを変更する場合にはあらかじめ `container.env` を変更した上で `docker-compose` コマンドを実行します。また、 Django プロジェクト内の `settings.py` もあわせて変更します。_

```sh
docker-compose run --rm django django-admin startproject --template project_template djangoproject .
```

コマンドを実行すると "djangoproject" というディレクトリといくつかのファイルがが作成されます。

```text
.
├── README.md
├── container.env
├── django
│   ├── Dockerfile
│   ├── djangoproject       # 作成される
│   │   ├── __init__.py     # 作成される
│   │   ├── settings.py     # 作成される
│   │   ├── urls.py         # 作成される
│   │   └── wsgi.py         # 作成される
│   ├── manage.py           # 作成される
│   ├── project_template
│   └── requirements.txt
└── docker-compose.yml
```

Django の初期データをセットアップします。

```sh
docker-compose run --rm django python3 manage.py migrate
```

次に、管理者ユーザを作成します。次のコマンドでは `admin` というユーザを作成しています。メールアドレスは任意で指定します。

```sh
docker-compose run --rm django python3 manage.py createsuperuser --username admin --email admin@example.com
```

管理者ユーザが作成されたら `docker-compose up` によって Django サーバを起動します。 `docker-compose.yml` で `manage.py runserver` を実行するように設定済みです。

```sh
docker-compose up -d
```

Django サーバのログを確認するときは次のコマンドを実行します。 `-f` オプションをつけることで `tail -f` のような挙動となります。

```sh
docker-compose logs -f django
```

### 新規アプリの作成

```sh
docker-compose run --rm django python3 manage.py startapp sample
```

このコマンドによって `django` ディレクトリ直下に `sample` というディレクトリおよびファイルが作成されます。ここから先は Django の作法に則ってルーティングを設定します。

## FAQ

### ホスト OS 上で開発環境を整えたい

_手元の環境が macOS であるため、以下に示している内容は macOS の場合の手順です。また、開発に使用しているエディタは Visual Studio Code です。_

本ドキュメントでは、Docker コンテナ上で Python Django アプリケーションを動作させるための手順を示しています。しかし、実際にはホスト OS でコーディングをすることになるため、開発利便性を向上させるためにもいくつかのセットアップをしておく必要があります (必須ではないですが、やっておいたほうが効率があがります)。

#### Python3 を導入する

ホスト OS にも Python が導入されている必要があります。macOS の場合には Homebrew を介して容易に Python3 をインストールすることができます。

もし Homebrew を導入していないのであれば、[ここ](https://brew.sh/)を参考にしましょう。

```sh
brew install python3
```

#### venv で仮想環境を作成する

この手順は任意ですが、ホスト OS のグローバル領域を汚さないためにも仮想化することをおすすめします。

```sh
python3 -m venv venv
```

#### venv を有効にする

直前の手順で作成した仮想環境を有効にします。これは、開いている**ターミナルセッションごとに有効化**する必要があります。有効化を忘れてしまうとグローバル領域に対する操作になってしまうことに注意しましょう。

```sh
source venv/bin/activate
```

`which` コマンドなどでパスの場所を確認すると

```sh
$ which python3
{PATH_TO_PROJECT}/venv/bin/python3

$ which pip3
{PATH_TO_PROJECT}/venv/bin/pip3
```

のように表示されます。

#### venv にもライブラリをインストールする

ホスト OS で利用するエディタにもライブラリを認識させる必要があるため、ホスト OS 側の仮想環境にもライブラリをインストールしておきます。

```sh
# 念のため venv 有効化
source venv/bin/activate
pip3 install -r django/requirements.txt
```

#### Visual Studio Code を使えるようにする

`.vscode/settings.json` を作成し、次のような設定を記述します。

```json
{
    "python.venvPath": "venv",
    "python.pythonPath": "venv/bin/python3",
    "python.linting.enabled": true,
    "files.trimTrailingWhitespace": true
}
```

_`python.linting.enabled` と `files.trimTrailingWhitespace` は好みによります。_

Visual Studio Code を再起動して設定を読み直します。エディタ上で linting やコード補完が有効になります。

### Python のライブラリを追加したい

Python ライブラリは [`requirements.txt`](https://pip.pypa.io/en/stable/user_guide/#requirements-files) で管理しています。追加したいライブラリの名称とバージョンを適切なフォーマットで `requirements.txt` に記載し、Django 用コンテナを再ビルドすることで有効化できます。

```sh
docker-compose build
docker-compose up -d
```

または `up` するときにビルドを同時に実行することもできます。

```sh
docker-compose up --build -d
```

### Django のコマンドやアプリから MySQL につながらない

```sh
django.db.utils.OperationalError: (2003, "Can't connect to MySQL server on 'mysql' (111)")
```

このようなエラーが表示される場合、MySQL への接続に失敗しています。これはおおよそ、MySQL コンテナが起動完了していないことが多いです。少し時間をおいて再度試してみましょう。

### 全てをクリアしたい

Docker コンテナを全て停止した状態で、ディレクトリ・ファイルの削除および Docker が使用しているボリュームの削除を実行します。

```sh
docker-compose down
rm django/{manage.py,djangoproject,sample}
docker volume rm $(docker volume ls -q)
```
