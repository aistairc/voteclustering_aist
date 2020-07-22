# 多言語対応の手順

Django内に存在するi18nという多言語機能を利用します。

1. DjangoのTempleteファイル内でi18nをロードし、翻訳したい文章をtransタグで囲みます。

```html
{% load i18n %}
{% trans '翻訳する文章' %}
```

- jsファイルやviewなどの中でも翻訳を設定することは可能です。
  - 詳しくは https://docs.djangoproject.com/ja/2.2/topics/i18n/ を参照してください。
  - jsについてはTemplate内のscriptタグ内に連想配列で翻訳を設定して、jsから連想配列を読み込む方が実装上は簡単です。

2. 翻訳対象に設定した文章を検出し翻訳用のテキストファイルを生成します。

```
$ make makemessages
```

3. `django/アプリ名/locale/en/LC_MESSAGES/*.po`に翻訳用のテキストファイルが生成されます。
- `msgid`が翻訳対象の文章なので、これに対応する訳を記述していきます。

```
msgid "翻訳する文章"
msgstr "A translated sentence"
```

4. 訳の記述後、.poファイルから翻訳用のバイナリファイル.moを生成します。

```
$ make compilemessages
```

