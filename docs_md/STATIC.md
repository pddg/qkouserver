# static.py

QkouServerのルートディレクトリに存在する各種設定項目のファイルです．

<!-- toc -->

## 共通項目

### ディレクトリ

* `BASE_DIR` : QkouServerディレクトリまでの絶対パス．
* `PRJ_DIR` : QkouServerディレクトリのあるディレクトリまでの絶対パス．現在使用していない．
* `SQLITE_DIR_PATH` : SQLiteのデータベースファイルを格納するディレクトリへのパス．．デフォルトは`BASE_DIR`．環境変数`SQLITE_DIR_PATH`に対応．
* `SQLITE_PATH` : SQLiteのデータベースを作製する場所を`SQLITE_DIR_PATH`を元に指定している．

### MySQL

* `USE_MYSQL` : MySQLを使用するかどうか．デフォルトは`False`．環境変数`USE_MYSQL`に対応．
* `MYSQL_USERNAME` : MySQLのユーザ名．環境変数`MYSQL_USERNAME`に対応．
* `MYSQL_PASSWORD` : MySQLのログインパスワード．環境変数`MYSQL_PASSWORD`に対応．
* `MYSQL_HOST` : MySQLサーバのホスト名．環境変数`MYSQL_HOST`に対応．
* `MYSQL_DATABASE_NAME` : MySQL上のデータベースの名前．環境変数`MYSQL_DATABASE_NAME`に対応．
* `MYSQL_PATH` : 上記の変数から生成されたMySQLへのパスの文字列．どれか一つでもかけている場合`None`となり，代わりに自動的に`SQLITE_PATH`が用いられる．

### models

テンプレート文字列の修正は多くの場合，クラスの`__str__()`メソッドの改変が必要となります．

#### <s>共通項目</s>

* <s>`UNDEFINED` : 学務課掲載情報において値の記載がないもの．デフォルトは"-"．</s>
* <s>`UNKNOWN` : プログラムの仕様上，満たすことの出来ない項目を埋める値．デフォルトは"不明"．</s>
* <s>`INTENSIVE` : 集中講義の曜日項目を満たす値．デフォルトは"集中"．</s>

#### `models.Info`

* `LEC_INFO_ID_TEMPLATE` : ツイート時に付加されるハッシュタグ．デフォルトは" #lec{id}"．
* `LEC_INFO_TEMPLATE` : 文字列化時のテンプレート．デフォルトは以下．

```text
講義名：{subject}
講師名：{teacher}
時限：{week} {period}限
概要：{abstract}
詳細：{detail}
```

#### `models.Cancel`

* `LEC_CANCEL_ID_TEMPLATE` : ツイート時に付加されるハッシュタグ．デフォルトは" #cancel{id}"
* `LEC_CANCEL_TEMPLATE` : 文字列化時のテンプレート．デフォルトは以下．

```text
講義名：{subject}
講師名：{teacher}
休講日：{str_day}
時限：{week} {period}限
概要：{abstract}
```

#### `models.News`

* `NEWS_ID_TEMPLATE` : ツイート時に付加されるハッシュタグ．デフォルトは" #news{id}"
* `NEWS_TEMPLATE_WITH_LINK` : リンクが文中に存在した場合の文字列化時のテンプレート．デフォルトは以下．

```text
掲載日：{str_first}
詳細：{detail}
リンク：{link}
```

* `NEWS_TEMPLATE_WITHOUT_LINK` : リンクが文中に存在しない場合の文字列化時のテンプレート．デフォルトは以下．

```text
掲載日：{str_first}
詳細：{detail}
```

#### `models.SeverErrorLog`

* `LOGIN_FAILURE_START_MSG` : 障害発生時のメッセージテンプレート．デフォルトは以下．

```text
[障害検知]
障害検知時刻：{created_at}
現在，学務課ホームページへのログインができない，または情報が正常に取得できないエラーが発生しています．
```

* `LOGIN_FAILURE_CONTINUE_MSG` : 障害継続時のメッセージテンプレート．デフォルトは以下．

```text
[障害継続中]
障害検知時刻: {created_at}
最終確認時刻: {last_confirmed}
学務課ホームページへログインできない，または情報が正常に取得できないエラーが継続中です．
```

* `LOGIN_FAILURE_END_MSG` : 障害復旧時のメッセージテンプレート．デフォルトは以下．

```text
[障害復旧]
障害検知時刻: {created_at}
復旧確認時刻: {fixed_at}
"学務課ホームページへのログイン及び情報の取得に成功しました．
```

## Bot機能関連項目

### Twitter

Botとしてつぶやくために必須な項目．現在，つぶやきを有効にしない場合でも必須（要改善）．

* `CONSUMER_KEY` : Twitter Appのコンシューマーキー．環境変数`CONSUMER_KEY`に対応．
* `CONSUMER_SECRET` : Twitter Appのコンシューマーシークレット．環境変数`CONSUMER_SECRET`に対応．
* `ACCESS_TOKEN` : Twitter Appのアクセストークン．環境変数`ACCESS_TOKEN`に対応．
* `ACCESS_SECRET` : Twitter Appのアクセスシークレット．環境変数`ACCESS_SECRET`に対応．

### Shibboleth認証

学務課webサイトにログインするためのユーザ名とパスワード．データ取得に必須．

* `SHIBBOLETH_USERNAME` : ユーザ名．環境変数`SHIBBOLETH_USERNAME`に対応．
* `SHIBBOLETH_PASSWORD` : パスワード．環境変数`SHIBBOLETH_PASSWORD`に対応．

### URL

* <s>`SYLLABUS_URL` : シラバスのURL．"http://www.syllabus.kit.ac.jp/"</s>
* `LEC_INFO_URL` : 授業関係連絡のURL．"https://portal.student.kit.ac.jp/ead/?c=lecture_information"
* `LEC_CANCEL_URL` : 休講情報のURL．"https://portal.student.kit.ac.jp/ead/?c=lecture_cancellation"
* `NEWS_URL` : 最新情報のURL．"https://portal.student.kit.ac.jp/"

### <s>シラバス</s>

* <s>`EXCEPTION_TITLES` : シラバスの科目名の命名規則の例外．通常クラス名が科目名の後ろに付けられるが，英語タイトルの科目名では半角スペースを挟む．</s>

 ```python
 ["English", "Reading", "Writing", "Basic", "Speaking", "Learning",
"Advanced", "Intermediate", "Acquisition", "Communication"]
```

* <s>`EXPIRE_ON` : シラバスデータの更新頻度．数字で指定．30を指定すると30日に一回データを更新する．</s>

### 定期更新プロセス

* `SCRAPING_INTERVAL` : データ取得の間隔の最低値（秒）．実際にはこれに処理時間が足される．環境変数`SCRAPING_INTERVAL`に対応．デフォルトは300．
* `LOGIN_FAILURE_TWEET_INTERVAL` : ログイン試行に失敗したとき，検知時と復旧時以外，障害が継続しているときに何分おきにツイートを行うかの間隔（秒）．
環境変数`LOGIN_FAILURE_TWEET_INTERVAL`に対応．デフォルトは1800．
* `DAILY_TWEET_HOUR` : 本日の休講ツイートをする時間を数値で指定．7ならば7時にツイートを行う．環境変数`DAILY_TWEET_HOUR`に対応．デフォルトは7．
* `TODAY_CANCEL_TEMPLATE` : 本日の休講ツイートのテンプレート文字列．

```text
{date} 本日の休講
{titles}"
```

* `TODAY_CANCEL_TEMPLATE_CONTINUE` : 一つの本日の休講ツイートに収まりきらなかった場合に続けてツイートされるテンプレート文字列．

```text
{date} 本日の休講 続き
{titles}
```

* `TODAY_IS_HOLIDAY_TEMPLATE`  : 祝日であった場合，休講情報ではなく何の日であるかをツイートする．

```text
{date} 今日は{holiday_name}の日です．{msg}
```

* `HOLIDAY_MSG_ARRAY` : 祝日であった場合の追加のメッセージ．この中からランダムに一つ選ばれる．

```python
["レポートや課題は終わりましたか？有意義な祝日をお過ごしください．",
"進捗どうですか？",
"今日くらいはこのbotもお休みをいただいても良いですか？まぁダメですよね．",
"ところでこのbotはPythonというプログラミング言語で書かれています．せっかくの休日ですし新しいことを始めてみては？"]
```

* `TESTING` : テスト実行であることを示すフラグ．環境変数`TESTING`に対応．デフォルトは`False`．
このフラグを建てると`Ctrl + C`で終了時にデータベースの中身を消去する．

* `INITIALIZE` : 初回実行フラグ．環境変数`INITIALIZE`に対応．デフォルトは`True`．このプロセスは必ず初回実行時のツイートを無効にするため，
一度終了させた後，次回の初回実行時に更新がツイートされない．`False`を与えることでツイートを行うようになる．

### ストリーム処理プロセス

* `REPLY_ACTION_REGEX` : 反応するリプライを抽出する正規表現

```text
".*(詳し|くわし).*"
```

* `THERE_IS_NO_INFORMATION_MSG` : 問い合わせた情報の`is_deleted`が`True`であった場合，又は問い合わせ内容が存在しなかった場合に返されるメッセージ．

```text
お問い合わせされた情報は現在存在しません．
```

* `DATABASE_ERROR_MSG` : 問い合わせた情報の取得に失敗したときに返されるメッセージ．

```text
DBエラーです．管理者までご連絡ください．
```
