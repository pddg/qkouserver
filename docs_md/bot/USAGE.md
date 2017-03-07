# 起動・運用

<!-- toc -->

# 更新通知botとして起動

準備中…

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

# UserStreamを処理するbotとして起動

準備中…

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
