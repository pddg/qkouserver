<!-- toc -->

# 環境

検証済みバージョンはPython 3.5.2です．最低でもpython 3.5以上が推奨です．  

## 外部モジュール

* beautifulsoup4
* lxml
* nose
* oauthlib
* requests
* requests-oauthlib
* six
* SQLAlchemy
* tweepy

## IDE

JetbrainsのPyCharmがオススメです．Community版でも問題ありませんが，学生は無料でProfessional版を入手できます．

# 開発環境の構築

Python 3.5以上，Git，及びPyCharmがインストール済みであるとします．

## Windows

### 1. Pythonの仮想環境を構築

```dosbatch
C:¥> cd C:¥User¥<ユーザ名>¥PycharmProjects
~¥PycharmProjects> python -m venv qkou
~¥PycharmProjects> cd qkouserver
# 仮想環境の有効化
~¥qkouserver> Scripts¥activate
(qkou) ~¥qkouserver> where python
C:¥User¥<ユーザ名>¥PycharmProjects¥qkouserver¥bin¥python
# 仮想環境の無効化
(qkou) ~¥qkouserver> deactivate
~¥qkouserver>
```

### 2. PyCharmからPythonインタプリタを指定

1. 新規プロジェクトを作成し，ディレクトリ名を`qkouserver`とする
2. pythonインタプリタの指定から`Add local`を選択し，`C:¥User¥<ユーザ名>¥PycharmProjects¥qkouserver¥bin¥python`を指定．
3. OK

### 3. Githubからクローン

```dospatch
C:¥> cd C:¥User¥<ユーザ名>¥PycharmProjects¥qkouserver
~¥qkouserver> git clone https://github.com/pddg/qkouserver.git src
```

PyCharmからプロジェクトディレクトリ中のsrcを右クリック，ルートディレクトリとしてマーク．

### 4. ライブラリのインストール

```dospatch
~¥qkouserver> Scripts¥activate
(qkou) ~¥qkouserver> where pip
C:¥User¥<ユーザ名>¥PycharmProjects¥qkouserver¥bin¥pip
(qkou) ~¥qkouserver> cd src
(qkou) ~¥src> pip install -r requirements.txt
```

#### lxmlのインストールに失敗する場合

VisualStudioなどがインストールされている環境ではインストールに失敗することがあります．その場合，有志の方が作成されたパッケージをインストールします．

1. [http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml)にアクセス
2. `lxml‑3.7.3‑cp35‑cp35m‑win32.whl`または`lxml‑3.7.3‑cp35‑cp35m‑win_amd64.whl`をプロジェクトディレクトリにダウンロード
3. 仮想環境を有効化して`pip install <ダウンロードしたパッケージ名>`

### 5. テスト

```bash
(qkou) $ nosetests
...............
----------------------------------------------------------------------
Ran 15 tests in 2.555s

OK
```

## Mac

Homebrew及びPyCharmはインストール済みであるとします．

### 1. Pythonの仮想環境を構築

pyenvのインストール

```bash
$ brew install pyenv pyenv-virtualenv
```

`.bashrc`の有効化とpyenvの有効化

```bash
$ vim ~/.bash_profile
if [ -f ~/.bashrc ] ; then
	. ~/.bashrc
fi
$ vim ~/.bashrc
export PYENV_ROOT=/usr/local/var/pyenv
export PATH=$PATH:$PYENV_ROOT/bin
if which pyenv > /dev/null; then eval "$(pyenv init -)"; fi
if which pyenv-virtualenv-init > /dev/null;
  then eval "$(pyenv virtualenv-init -)";
fi
$ source ~/.bashrc
```

仮想環境の構築

```bash
$ pyenv install 3.5.2
$ pyenv virtualenv 3.5.2 qkou
$ mkdir ~/PycharmProjects/qkouserver
$ cd ~/PycharmProjects/qkouserver
$ pyenv local qkou
(qkou) $ which python
/usr/local/var/pyenv/versions/qkou/bin/python
```

### 2. PyCharmからPythonインタプリタを指定

1. 新規プロジェクトを作成し，ディレクトリ名を`qkouserver`とする
2. pythonインタプリタの指定から`Add local`を選択し，`/usr/local/var/pyenv/versions/qkou/bin/python`を指定．
3. OK

### 3. Githubからクローン

```bash
$ git clone https://github.com/pddg/qkouserver.git ~/PycharmProjects/qkouserver
```

### 4. ライブラリのインストール

```bash
$ cd ~/PycharmProjects/qkouserver
(qkou) $ pip install -r requirements.txt
```

### 5. テスト

```bash
(qkou) $ nosetests
...............
----------------------------------------------------------------------
Ran 15 tests in 2.555s

OK
```

# 運用環境の構築

運用はLinux環境においてDocker使用を想定しています．Dockerを使用しない場合，開発環境の構築と同様にPythonの仮想環境を構築して運用してください．

## Ubuntu

Docker，およびdocker-composeはインストール済みであるとします．

### 1. イメージをpull

```bash
$ docker pull pddg/qkouserver:latest
$ docker run --rm pddg/qkouserver:latest
usage: manage.py [-h] {qkoubot,stream} ...

QkouBot and QkouAPI is the application for KIT students. These are
automatically collect and redistribute information and cancellation of
lecture. QkouBot detect update of information and tweet it.

positional arguments:
  {qkoubot,stream}  sub commands help
    qkoubot         Start QkouBot command
    stream          Start stream processing
```

### 2. Twitterの認証情報や学生番号等を入力

`docker-compose.yml`を置くディレクトリを適当に決めます．今回はユーザのホームディレクトリ以下に`containers/qkoubot`を作成します．

```bash
$ mkdir containers/qkoubot
$ mkdir data
$ mkdir bot_log
$ mkdir stream_log
$ curl https://raw.githubusercontent.com/pddg/qkouserver/master/config.ini.sample > data/config.ini
$ vim data/config.ini
```

### 3. docker-compose.ymlを記述

```bash
$ vim docker-compose.yml
```

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

### 4. 起動

```bash
$ docker-compose up -d
```

一回目の試行ではツイート機能は無効になっています．一度データベースを作成すると，以降停止するまでデータの更新・ツイートを継続します．

### 二回目以降の起動

`docker-compose.yml`においてqkoubotに環境変数を追加します．

```yaml
# 省略
  qkoubot:
  # 省略
  environment:
    INITIALIZE: "false"
# 省略
```

これにより最初の実行時からツイートが有効化されます．

## コンテナのビルド

リポジトリに既に`Dockerfile`が含まれています．ベースイメージは`alpine:3.5`です．

```bash
$ git clone https://github.com/pddg/qkouserver.git qkouserver
$ docker build ./qkouserver
```