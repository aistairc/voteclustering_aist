# Makefileの各コマンドの使い方

### make help

各コマンドの一覧と説明を表示します。
このコマンドはMac, Linux環境でしか動作しないので、Windows環境では`wsl make help`とWSL上でコマンドを実行させてください。

### make build

Dockerのimageの構築を行います。
主にDockerfileに変更を加えた時などに実行してください。

また、pythonのパッケージ（pip）のインストールはimageの構築時に`requirement.txt`を読み込む形で行っています。
よって、pythonパッケージのインストールを反映させたい場合にも`make build`を実行してください。

デフォルトだとキャッシュを使用して構築を行いますが、キャッシュを使用せずにimageの構築を行いたい場合は、
`make build options="--no-cache"`でキャッシュを使用しないようオプションを指定してください。

### make up-dev

開発環境でコンテナを起動します。

### make up-prod

本番環境でコンテナを起動します。

### make restart-dev

開発環境でコンテナを再起動します。
`manage.py`に変更を加えたときなど、djangoを再起動したい際に使用してください。

### make restart-prod

本番環境でコンテナを再起動します。

### make makemigrations

Modelの変更情報をもとにmigrationファイルを作成します。
DjangoのModelの中でフィールドを追加したり、フィールドの属性を変更した場合に実行してください。

### make migrate

`make makemigrations`によって作成されたmigrationファイルを実際にMySQLに反映させます。
新たにmigrationファイルに変更が生じた場合に実行してください。
例えば開発環境でmigrationファイルを更新した場合には、本番環境でmigrationファイルの変更をpullした後に実行する必要があります。

### make create-superuser

DjangoのAdmin画面に管理者権限でログインできるスーパーユーザーを作成します。

### make collect-static

`manage.py`において指定されたstaticディレクトリ内のファイルを収集します。
staticディレクトリ内の変更（javascriptやcssなど）をブラウザに反映させるために必ず実行する必要があります。

### make django-log

Djangoアプリケーションのログを表示します。
主にDjangoのバックエンドでエラーが発生した際に原因箇所を突き止めるために使用します。

Djangoのログの出力方法については以下のURLを参考にしてください。
https://qiita.com/okoppe8/items/3e8ab77c5801a7d21991

### make makemessages

[多言語対応作業](translate_manual.md)時にtransタグが設定された文章から翻訳用テキストファイルを生成するために使用します。

### make compilemessages

[多言語対応作業](translate_manual.md)時に翻訳用テキストファイルから翻訳バイナリを生成するために使用します。

### make generate-ERD

`django/manage_ERD/table_definition.er`内の記述をもとにER図(`django/manage_ERD/table_definition.png`)を生成します。
詳しくはリポジトリ内の`docs/develpment_manual.md`, `docs/manage_ERD_manual.md`を参照してください。

### make run-dev service="service" command="command"

開発環境においてオプションで指定したサービス上でオプションで指定したコマンドを実行します。

例えば、`make run-dev service="django" command="bash"`と入力するとdjangoサービス上でbashを起動しdjangoサービス内で自由にコマンドを実行することが出来ます。

他にも`make run-dev service="mysql" command="bash"`で同様にmysqlサービス上でbashを起動できます。
これはmysql内のデータを確認したり直接mysqlのテーブルなどを操作したいときに使用します。

### make run-prod

本番環境においてオプションで指定したサービス上でオプションで指定したコマンドを実行します。

### make yarn-all

`django/package.json`内に記述した`all`コマンドを実行します。

make yarn-allで実行される動作は以下の内容から構成されます。

- yarnのライブラリのインストール
- staticファイルとして収集する必要があるライブラリのコピー
- webpackによるjavascript, cssファイルなどのbuild
- collect staticコマンドによるstaticファイルの収集（`make collect-static`で実行しているものと同様の動作です。）

### make webpack-watch

webpackのbuildをwatchモードで実行します。  
通常のbuildではbuild後そのまま終了しますが、watchモードではファイルの監視モードに以降しファイルに変更が生じるとその部分を自動で再ビルドしてくれます。  
開発作業を行っている際にはこちらのモードで自動的にbuildさせたほうが便利な場面は多いと思います。

collect-staticまでは自動では実行しないので、`make collect-static`を手動で実行しブラウザに反映させてください。

## 編集操作と実行するコマンドの対応

### docker-compose.yml, DockerfileなどDocker関連のファイルを編集した時

`make build` を実行してコンテナを再構築する必要がある。

### pythonのライブラリを新規導入し`requirement.txt`に変更が発生した場合、Linuxのライブラリを新規導入した場合

これらのライブラリのインストールはDockerfile内の処理で行っているので`make build`を実行してコンテナの再構築が必要

### `settings.py`を修正した場合

Djangoの再起動が必要なので`make restart-[dev or prod]`でコンテナを再起動する。

### Modelのフィールドを追加、編集した場合

`make makemigrations`でmigrationファイルを作成、`make migrate`でMySQLに適用する。

### js, cssなどstaticファイルを編集した場合

`make yarn-all`でコンパイルやcollect-staticを行う。

### テンプレート内で翻訳対象の文章を追加した場合

`make makemessages`, `make compilemessages`で翻訳作業を行う  
詳細は [translate_manual.md](translate_manual.md) を参照
