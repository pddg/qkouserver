<!-- toc -->

# 起動・運用

2つのコマンドが含まれます．

```bash
$ cd path/to/qkouserver
$ python manage.py -h
usage: manage.py [-h] {qkoubot,stream} ...

QkouBot is an application for KIT students. This automatically collect and
redistribute information and cancellation of lectures. QkouBot detect update
of information and tweet it.

positional arguments:
  {qkoubot,stream}  sub commands help
    qkoubot         Start QkouBot command
    stream          Start stream processing

optional arguments:
  -h, --help        show this help message and exit
```

# 更新通知botとして起動

`qkoubot`コマンドを使用します．

## ヘルプメッセージ

```sh
$ cd path/to/qkouserver
$ python manage.py qkoubot -h
usage: manage.py qkoubot [-h] [-v] [-l {1,2,3}] [--ini INI]
                         [--file-log-enable] [--log-path LOG_PATH] [-t]
                         [--without-failure]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Default logging output is above WARNING level to
                        stderr. If this option enabled, logging output is
                        above INFO level to stdout by default.You can change
                        its level using `-l` or `--log-level` option.
  -l {1,2,3}, --log-level {1,2,3}
                        Choose a log level. 1: debug, 2: info, 3: warning.
                        Default value is 2
  --ini INI             Read `*.ini` file and overwrite environment variables.
  --file-log-enable     Enable logging to `*.log` file. These files are save
                        into `log` directory by default.
  --log-path LOG_PATH   Specify location of `*.log` file.
  -t, --tweet           Enable tweet update of any information.
  --without-failure     Tweet update of information, but do not tweet login
                        failure information.
```

## 各種オプションについて

* `-h`, `--help`<br>
ヘルプメッセージの表示．
* `-v`, `--verbose`<br>
詳細情報を標準出力に出力．デフォルトのログレベルは`INFO`．
* `-l`, `--log-level`<br>
出力ログレベルの変更．引数を1~3のうちから一つとる．1: `DEBUG`, 2: `INFO`, 3: `WARNING`．それぞれそのレベル以上の情報を出力する．DEBUGで全てのログを出力することになる．
* `--ini`<br>
`.ini`ファイルへのパスを指定．
* `--file-log-enable`<br>
`.log`ファイルへのログ出力を行う．デフォルトではリポジトリ中の`log`ディレクトリに`debug.log`と`error.log`を出力．それぞれ2MBずつでログローテートを行い，順に`.log.1`，`.log.2`と拡張子が付けられ最大5個分蓄積される．
* `--log-path`<br>
引数を一つとり，ログファイルの出力先ディレクトリを指定．末尾が`/`にならないよう注意．
* `-t`, `--tweet`<br>
ツイート機能の有効化．なお，機能の有効無効問わず現在はTwitterAppの認証情報が必要となる．
* `--without-failure`<br>
ツイート機能を有効化した際，デフォルトではログイン試行やパースに失敗すると障害情報検知ツイートを行う．このオプションを有効にすると，障害情報をツイートしなくなる．

## iniファイルを使用する場合

`.ini`ファイルは4つのセクションから成ります．全てが要求されるわけではありません．不要なものはコメントアウトしても問題ありませんが，Twitter認証情報及び，シボレス認証情報は必須となります．  
セクション名・キー名が間違っている場合エラーを出力します．

### mysqlセクション

```ini
[mysql]
MYSQL_USERNAME=MySQLのユーザ名
MYSQL_PASSWORD=MySQLのパスワード
MYSQL_HOST=MySQLサーバのホスト名
MYSQL_DATABASE_NAME=MySQLのデータベース名
```

### shibbolethセクション

```ini
[shibboleth]
SHIBBOLETH_USERNAME=bから始まるログインに使用する学生番号
SHIBBOLETH_PASSWORD=上記のパスワード
```

### twitterセクション

```ini
[twitter]
CONSUMER_KEY=コンシューマキー
CONSUMER_SECRET=コンシューマシークレット
ACCESS_TOKEN=アクセストークン
ACCESS_SECRET=アクセスシークレット
```

### otherセクション

```ini
[other]
TESTING=テスト実行フラグ．trueまたはfalse．
SCRAPING_INTERVAL=スクレイピング間隔．デフォルトは300（秒）
LOGIN_FAILURE_TWEET_INTERVAL=ログイン失敗時の障害情報ツイートの間隔．デフォルトは1800（秒）
DAILY_TWEET_HOUR=毎日の休講ツイートの時刻．デフォルトは7．
SQLITE_PATH=SQLiteデータベースファイルへのパス．デフォルトは`path/to/qkouserver/data`．指定したパス以下にsqlite.dbとして作成される．
LOG_LOCATION=ログファイルの出力先ディレクトリ．デフォルトは`path/to/qkouserver/log`．
```

## .iniファイルを使用しない場合

環境変数から与えることが出来ます．この方法は環境変数に値を追加する必要があり，どのアプリケーションが利用する環境変数とコンフリクトするか分からないのでDockerコンテナでの使用のみ推奨します．

### docker runする場合

#### -eオプション

```bash
$ docker run --name qkoubot -e SHIBBOLETH_USERNAME=ユーザ名 \
    -e SHIBBOLETH_PASSWORD=パスワード \
    -e CONSUMER_KEY=コンシューマキー \
    -e CONSUMER_SECRET=コンシューマシークレット \
    -e ACCESS_TOKEN=アクセストークン \
    -e ACCESS_SECRET=アクセスシークレット \
    pddg/qkouserver:latest qkoubot -v -t
```

#### --env-fileオプション

`.env`ファイルを作成する．

```bash
$ touch .env
$ vim .env
```

`キー=値形式`で記述．  
リファレンス： http://docs.docker.jp/compose/env-file.html

```bash
SHIBBOLETH_USERNAME=bから始まるログインに使用する学生番号
SHIBBOLETH_PASSWORD=上記のパスワード
CONSUMER_KEY=コンシューマキー
CONSUMER_SECRET=コンシューマシークレット
ACCESS_TOKEN=アクセストークン
ACCESS_SECRET=アクセスシークレット
```

`--env-file`オプションで指定．

```bash
$ docker run --name qkoubot --env-file .env \
    pddg/qkouserver:latest qkoubot -v -t
```

### docker-composeを使用する場合

同様に`environment`セクションで直接環境変数を指定，または`env_file`セクションで`.env`ファイルを指定し，`docker-compose.yml`と同じ階層に`.env`ファイルを作成します．

# UserStreamを処理するbotとして起動

`stream`コマンドを使用．

## ヘルプメッセージ

```sh
$ cd path/to/qkouserver
$ python manage.py stream -h
usage: manage.py stream [-h] [-v] [-l {1,2,3}] [--ini INI] [--file-log-enable]
                        [--log-path LOG_PATH]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Default logging output is above WARNING level to
                        stderr. If this option enabled, logging output is
                        above INFO level to stdout by default.You can change
                        its level using `-l` or `--log-level` option.
  -l {1,2,3}, --log-level {1,2,3}
                        Choose a log level. 1: debug, 2: info, 3: warning.
                        Default value is 2
  --ini INI             Read `*.ini` file and overwrite environment variables.
  --file-log-enable     Enable logging to `*.log` file. These files are save
                        into `log` directory by default.
  --log-path LOG_PATH   Specify location of `*.log` file.
```

## 各種オプションについて

全て`qkoubot`コマンドに準ずる．

## iniファイルを使用する場合

`qkoubot`コマンドの時と同様．

## iniファイルを使用しない場合

`qkoubot`コマンドの時と同様．

## SQLiteを使用している場合

`qkoubot`においてMySQLではなくSQLiteを使用している場合，データベースファイルを`qkoubot`コンテナと`stream`コンテナで共有させる必要があります．  

以下のように`docker-compose.yml`の`volumes`セクションでコンテナの`/data`ディレクトリにホストのディレクトリをマウントする，または`docker run`コマンドで指定する必要があります．

```yaml
version: "2"
services:
  qkoubot:
    container_name: qkoubot
    image: pddg/qkouserver:latest
    volumes:
      - ./data:/data
      - ./bot_log:/srv/qkouserver/log
    command: qkoubot -v -t --ini /data/config.ini --file-log-enable
    restart: always
  qkoustream:
    container_name: qkoustream
    image: pddg/qkouserver:latest
    volumes:
      - ./data:/data
      - ./stream_log:/srv/qkouserver/log
        tag: qkoustream
    restart: always
    command: stream -v --ini /data/config.ini --file-log-enable
```

### 排他制御について

上記のようにSQLiteデータベースのファイルをプロセス間で共有すると，おそらく（期待される動作としては）ファイルごとロック，つまり，qkoubotのプロセスが書き込みをする間，streamプロセスはいかなる読み込みも出来ないはずです．  

これは厳密に検証したわけでは無く，仕様上おそらくそうだろうという憶測で書いています．現状botの動作はそれほど遅いモノでも無く，それほど頻繁にuserstreamからのアクセスが来るわけでも内のでSQLiteでも良いとしていますが，心配ならばMySQLを使用するべきでしょう．

ただしSQLiteにおいても複数プロセス間での処理は適切に行われるはずであり，それほど問題は無いと言えるかも知れません．
