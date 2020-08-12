# 開発環境の構築

## 実行手順

#### リポジトリのクローン
```sh
$ git clone https://github.com/aistairc/voteclustering_aist.git
$ cd voteclustering_aist
```
- **環境設定用ファイルである.env, container.envを用意して、それぞれ `/django/.env`, `/container.env`に配置**

#### データベースの構築
```sh
$ make migrate
```

#### スーパーユーザーの設定（Adminページに入る際に必要）
```sh
$ make create-superuser username=admin email=admin@example.com
```

#### Dockerの起動
```sh
$ make up-dev
```

#### 動作確認
`http://localhost/admin/`にアクセスし，Adminページにログインできれば成功


## モデルに更新を行う際の更新手順

1. `django/AIST_survey/models/...` から更新対象となるモデルが存在するクラスを書き換え
1. `django/AIST_survey/admin.py`から`[クラス名]Admin`クラス内のfieldsetsやlist_display，fieldsなどAdminページのフィールドに関わる項目を更新
    - 新たにモデルを追加した際は対応するクラスを`[クラス名]Admin`のクラス名でクラスを作成すること
        - Adminページにおけるモデルやフィールドの表示に必要となる
1. [manage_ERD_manual.md](manage_ERD_manual.md)を確認しながらER図を更新
1. `django/AIST_survey/admin.py`から`EnqueteAdmin`クラス内の`import_enquete_setting_view`関数内に該当するフィールドを受け取る処理の追加
1. `$ make makemigrations`でマイグレーションファイルを作成
1. `$ make migrate`でマイグレート


## 自動テスト

#### ユーザに権限を付与
```sh
$ docker-compose exec mysql mysql -u root -p -e "grant all privileges on *.* to voteclustering@'%'; flush privileges;"
```

#### テストの実行
```sh
$ docker-compose run --rm django python3 manage.py test
```
