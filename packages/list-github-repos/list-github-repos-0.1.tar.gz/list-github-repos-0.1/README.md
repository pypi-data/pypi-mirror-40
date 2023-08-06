# list-github-repos

`list-github-repos` is a utility that lists the repos from a GitHub profile. The `-f` option produces JSON or CSV with the repository descriptions.

```shell
$> list-github-repos -u knadh -s modified -o desc
2019-01-03T17:14:02Z      source               https://github.com/knadh/stuffbin
2019-01-03T16:55:57Z      source, archived     https://github.com/knadh/niltalk
2018-12-27T08:17:57Z      fork                 https://github.com/knadh/zgok
2018-12-05T06:59:28Z      source               https://github.com/knadh/localStorageDB
2018-12-03T12:58:20Z      fork                 https://github.com/knadh/goyesql
2018-11-29T08:10:56Z      source               https://github.com/knadh/git-bars
2018-11-05T07:09:25Z      source               https://github.com/knadh/sql-jobber
2018-11-05T06:41:57Z      source               https://github.com/knadh/ml2en
2018-09-01T12:20:10Z      source               https://github.com/knadh/go-get-youtube
2018-08-29T13:25:37Z      fork                 https://github.com/knadh/simplesessions
2018-06-15T00:24:36Z      source               https://github.com/knadh/xmlutils.py
2018-04-23T13:55:52Z      source               https://github.com/knadh/simplemysql
2018-04-13T11:50:07Z      fork                 https://github.com/knadh/gnatsd
2018-01-15T11:11:36Z      source               https://github.com/knadh/bigreddy
2017-01-05T11:11:34Z      fork                 https://github.com/knadh/gencode
2016-11-23T13:20:35Z      source               https://github.com/knadh/tinytabs
2016-06-14T06:38:15Z      source               https://github.com/knadh/jsonconfig
2015-03-19T09:11:47Z      source               https://github.com/knadh/chunkedreader
2014-11-21T05:21:11Z      fork                 https://github.com/knadh/pdoc
2014-08-13T10:30:27Z      source               https://github.com/knadh/tinyprogressbar
2013-11-08T06:31:44Z      source               https://github.com/knadh/tinytooltip
2013-08-08T07:30:25Z      source               https://github.com/knadh/jqdialog
2013-06-13T07:15:07Z      fork                 https://github.com/knadh/Chart.js
2013-06-04T09:11:06Z      source               https://github.com/knadh/csssprite
2013-05-21T17:27:00Z      source               https://github.com/knadh/datuk
2013-05-18T11:05:49Z      source               https://github.com/knadh/mlphone
2013-05-15T14:46:29Z      source               https://github.com/knadh/simpleplanner
2013-05-15T14:37:57Z      source               https://github.com/knadh/boastmachine
2013-03-05T06:41:45Z      source               https://github.com/knadh/stringvalidator.py
2011-10-15T22:31:15Z      source               https://github.com/knadh/ctunes
```

## Install
`pip install list-github-repos`

See `list-github-repos --help` for options

